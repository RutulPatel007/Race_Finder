"""
Code Slicer: Extracts method bodies and class fields from Java source files.
Uses javalang for Java parsing to produce code slices for LLM verification.
"""
import os
import re
from typing import Optional
from models import CodeSlice


def extract_code_slice(file_path: str, class_name: str, method_name: str = None,
                       line_number: int = 0) -> Optional[CodeSlice]:
    """
    Extract a code slice from a Java source file.
    
    Attempts javalang parsing first for accuracy, falls back to regex-based
    extraction if parsing fails (common with partial/broken source files).
    """
    if not os.path.exists(file_path):
        # Try to find the file by searching relative to source root
        return None

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            source = f.read()
    except Exception:
        return None

    # Try javalang-based extraction first
    slice_result = _extract_with_javalang(source, class_name, method_name)
    if slice_result:
        slice_result.file_path = file_path
        slice_result.line_number = line_number
        return slice_result

    # Fallback: regex-based extraction
    return _extract_with_regex(source, file_path, class_name, method_name, line_number)


def _extract_with_javalang(source: str, class_name: str, method_name: str = None) -> Optional[CodeSlice]:
    """Use javalang to parse and extract method body and class fields."""
    try:
        import javalang
        tree = javalang.parse.parse(source)
    except Exception:
        return None

    lines = source.split('\n')

    for _, cls_decl in tree.filter(javalang.tree.ClassDeclaration):
        if cls_decl.name != class_name:
            continue

        # Extract class fields
        fields = []
        for field in cls_decl.fields:
            if hasattr(field, 'position') and field.position:
                line_idx = field.position.line - 1
                if 0 <= line_idx < len(lines):
                    fields.append(lines[line_idx].strip())

        class_fields = '\n'.join(fields)

        # Extract specific method or return all methods
        if method_name:
            for method in cls_decl.methods:
                if method.name == method_name and hasattr(method, 'position') and method.position:
                    method_source = _extract_method_block(lines, method.position.line - 1)
                    return CodeSlice(
                        class_name=class_name,
                        method_name=method_name,
                        method_source=method_source,
                        class_fields=class_fields
                    )

    return None


def _extract_with_regex(source: str, file_path: str, class_name: str,
                         method_name: str = None, line_number: int = 0) -> Optional[CodeSlice]:
    """
    Fallback regex-based extraction when javalang parsing fails.
    Finds the method by name and extracts the full body using brace matching.
    """
    lines = source.split('\n')

    # Extract fields: lines with @Autowired or common field patterns
    field_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (stripped.startswith("@Autowired") or 
            stripped.startswith("private ") and not stripped.startswith("private void") and
            not stripped.startswith("private static") and "(" not in stripped):
            # Include annotation line above if it's @Autowired
            field_lines.append(stripped)
            # Also grab the next line if current is @Autowired
            if stripped.startswith("@Autowired") and i + 1 < len(lines):
                field_lines.append(lines[i + 1].strip())

    class_fields = '\n'.join(list(dict.fromkeys(field_lines)))  # deduplicate preserving order

    if method_name:
        # Find the method declaration line
        method_start = None
        for i, line in enumerate(lines):
            # Match method declarations like: public ResponseEntity<X> methodName(
            if method_name in line and ('public ' in line or 'private ' in line or 
                                         'protected ' in line or '@Override' in lines[max(0, i-1)]):
                # Verify it's a method declaration, not a call
                if re.search(rf'\b{re.escape(method_name)}\s*\(', line):
                    method_start = i
                    break

        if method_start is not None:
            method_source = _extract_method_block(lines, method_start)
            return CodeSlice(
                class_name=class_name,
                method_name=method_name,
                method_source=method_source,
                class_fields=class_fields,
                file_path=file_path,
                line_number=line_number
            )

    # If no specific method found but we have a line number, extract surrounding context
    if line_number > 0 and line_number <= len(lines):
        start = max(0, line_number - 15)
        end = min(len(lines), line_number + 15)
        context = '\n'.join(lines[start:end])
        return CodeSlice(
            class_name=class_name,
            method_name=method_name or "unknown",
            method_source=context,
            class_fields=class_fields,
            file_path=file_path,
            line_number=line_number
        )

    return None


def _extract_method_block(lines: list, start_line: int) -> str:
    """
    Extract a complete method body by counting braces from the start line.
    Returns the full method source including signature and body.
    """
    brace_count = 0
    found_opening = False
    method_lines = []

    for i in range(start_line, len(lines)):
        line = lines[i]
        method_lines.append(line)

        for char in line:
            if char == '{':
                brace_count += 1
                found_opening = True
            elif char == '}':
                brace_count -= 1

        if found_opening and brace_count == 0:
            break

    return '\n'.join(method_lines)


def find_source_file(source_root: str, class_name: str) -> Optional[str]:
    """
    Find a Java source file by class name within the source root.
    Searches recursively for ClassName.java.
    """
    target = class_name + ".java"
    for root, dirs, files in os.walk(source_root):
        # Skip test directories
        if '/test/' in root or '/tests/' in root:
            continue
        for f in files:
            if f == target:
                return os.path.join(root, f)
    return None
