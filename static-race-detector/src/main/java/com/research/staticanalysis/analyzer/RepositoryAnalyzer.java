package com.research.staticanalysis.analyzer;

import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.utils.SourceRoot;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

public class RepositoryAnalyzer {

    // Maps Repository Class Name -> Entity Class Name
    // Example: "OrderRepository" -> "Order"
    public Map<String, String> analyze(File root) {
        Map<String, String> dataMap = new HashMap<>();
        SourceRoot sourceRoot = new SourceRoot(root.toPath());

        try {
            sourceRoot.parse("", (localPath, absolutePath, result) -> {
                if (result.isSuccessful() && result.getResult().isPresent()) {
                    analyzeCompilationUnit(result.getResult().get(), dataMap);
                }
                return SourceRoot.Callback.Result.DONT_SAVE;
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
        return dataMap;
    }

    private void analyzeCompilationUnit(CompilationUnit cu, Map<String, String> dataMap) {
        cu.findAll(ClassOrInterfaceDeclaration.class).forEach(cid -> {
            if (cid.isInterface()) {
                for (ClassOrInterfaceType extendedType : cid.getExtendedTypes()) {
                    // Check if it extends a Spring Data interface
                    if (isSpringDataRepository(extendedType.getNameAsString())) {
                        // Extract the generic type argument <Entity, ID>
                        if (extendedType.getTypeArguments().isPresent()) {
                            var typeArgs = extendedType.getTypeArguments().get();
                            if (!typeArgs.isEmpty()) {
                                String entityName = typeArgs.get(0).asString();
                                dataMap.put(cid.getNameAsString(), entityName);
                                System.out.println("  [MAP] " + cid.getNameAsString() + " manages entity " + entityName);
                            }
                        }
                    }
                }
            }
        });
    }

    private boolean isSpringDataRepository(String name) {
        return name.equals("JpaRepository") || 
               name.equals("CrudRepository") ||
               name.equals("MongoRepository") ||
               name.equals("PagingAndSortingRepository");
    }
}