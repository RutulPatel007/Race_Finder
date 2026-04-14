package com.research.staticanalysis.analyzer;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.research.staticanalysis.model.EntityUsage;
import com.research.staticanalysis.model.EntityUsage.AccessType;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Stream;

/**
 * Builds a Service Map: ServiceClassName -> { methodName -> List<EntityUsage> }
 * 
 * This bridges the gap between Controllers and Repositories.
 * Controllers call service methods; service methods call repository methods.
 * Without this layer, the EndpointAnalyzer misses most entity accesses.
 */
public class ServiceAnalyzer {

    // Maps repoClassName -> entityName (from RepositoryAnalyzer)
    private final Map<String, String> dataMap;

    // Result: serviceClassName -> { serviceMethodName -> List<EntityUsage> }
    private final Map<String, Map<String, List<EntityUsage>>> serviceMap = new HashMap<>();

    public ServiceAnalyzer(Map<String, String> dataMap) {
        this.dataMap = dataMap;
    }

    public Map<String, Map<String, List<EntityUsage>>> analyze(File root) {
        System.out.println("Scanning for Services in: " + root.getAbsolutePath());

        try (Stream<Path> paths = Files.walk(root.toPath())) {
            paths.filter(p -> p.toString().endsWith(".java"))
                .forEach(path -> {
                    try {
                        CompilationUnit cu = StaticJavaParser.parse(path);
                        analyzeCompilationUnit(cu, path.toString());
                    } catch (Exception e) {
                        // Ignore parsing errors for individual files
                    }
                });
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("  [SVC] Found " + serviceMap.size() + " service classes with repository access.");
        return serviceMap;
    }

    private void analyzeCompilationUnit(CompilationUnit cu, String filePath) {
        cu.findAll(ClassOrInterfaceDeclaration.class).forEach(cid -> {
            // Check if this class is a @Service or @Component
            boolean isService = cid.getAnnotationByName("Service").isPresent() ||
                                cid.getAnnotationByName("Component").isPresent();
            
            // Also check for ServiceImpl pattern (implements a service interface)
            if (!isService && !cid.isInterface()) {
                for (var impl : cid.getImplementedTypes()) {
                    if (impl.getNameAsString().endsWith("Service")) {
                        isService = true;
                        break;
                    }
                }
            }

            if (!isService) return;

            // Build a field name -> repo type map for this class
            // e.g. "contactsRepository" -> "ContactsRepository"
            Map<String, String> fieldToRepoType = new HashMap<>();
            for (FieldDeclaration field : cid.getFields()) {
                String fieldType = field.getElementType().asString();
                // Check if this field type is a known repository
                if (dataMap.containsKey(fieldType)) {
                    field.getVariables().forEach(v -> {
                        fieldToRepoType.put(v.getNameAsString(), fieldType);
                    });
                }
            }

            if (fieldToRepoType.isEmpty()) return;

            // Now trace each method in this service class
            String serviceClassName = cid.getNameAsString();
            Map<String, List<EntityUsage>> methodMap = new HashMap<>();

            for (MethodDeclaration method : cid.getMethods()) {
                List<EntityUsage> usages = traceServiceMethod(method, fieldToRepoType, filePath);
                if (!usages.isEmpty()) {
                    methodMap.put(method.getNameAsString(), usages);
                }
            }

            if (!methodMap.isEmpty()) {
                serviceMap.put(serviceClassName, methodMap);
            }
        });
    }

    private List<EntityUsage> traceServiceMethod(MethodDeclaration method,
                                                   Map<String, String> fieldToRepoType,
                                                   String filePath) {
        List<EntityUsage> usages = new ArrayList<>();

        method.findAll(MethodCallExpr.class).forEach(call -> {
            try {
                String scopeName = call.getScope().map(Object::toString).orElse("");
                String methodName = call.getNameAsString();

                // Check if the scope matches a known repository field
                for (Map.Entry<String, String> entry : fieldToRepoType.entrySet()) {
                    String fieldName = entry.getKey();
                    String repoType = entry.getValue();

                    if (scopeName.equals(fieldName)) {
                        String entityName = dataMap.get(repoType);
                        AccessType accessType = classifyAccess(methodName);
                        int line = call.getBegin().map(p -> p.line).orElse(0);
                        usages.add(new EntityUsage(entityName, accessType, line, filePath));
                    }
                }
            } catch (Exception e) {
                // Skip problematic method calls
            }
        });

        return usages;
    }

    /**
     * Classifies a repository method call as READ or WRITE.
     * Covers standard Spring Data method naming conventions.
     */
    static AccessType classifyAccess(String methodName) {
        // Write operations
        if (methodName.startsWith("save") ||
            methodName.startsWith("delete") ||
            methodName.startsWith("remove") ||
            methodName.startsWith("update") ||
            methodName.startsWith("insert") ||
            methodName.startsWith("create") ||
            methodName.startsWith("put") ||
            methodName.startsWith("merge") ||
            methodName.startsWith("persist") ||
            methodName.startsWith("flush") ||
            methodName.equals("saveAndFlush") ||
            methodName.equals("saveAll") ||
            methodName.equals("deleteAll") ||
            methodName.equals("deleteById") ||
            methodName.equals("deleteAllById") ||
            methodName.equals("deleteInBatch") ||
            methodName.equals("deleteAllInBatch")) {
            return AccessType.WRITE;
        }
        // Everything else is a read
        return AccessType.READ;
    }
}
