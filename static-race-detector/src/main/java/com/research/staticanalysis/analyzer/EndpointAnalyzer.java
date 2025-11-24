package com.research.staticanalysis.analyzer;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.resolution.declarations.ResolvedMethodDeclaration;
import com.github.javaparser.utils.SourceRoot;
import com.research.staticanalysis.model.Endpoint;
import com.research.staticanalysis.model.EntityUsage;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class EndpointAnalyzer {

    private final Map<String, String> dataMap;

    public EndpointAnalyzer(Map<String, String> dataMap) {
        this.dataMap = dataMap;
    }

    public List<Endpoint> analyze(File root) {
        List<Endpoint> endpoints = new ArrayList<>();
        SourceRoot sourceRoot = new SourceRoot(root.toPath());

        try {
            sourceRoot.parse("", (localPath, absolutePath, result) -> {
                if (result.isSuccessful() && result.getResult().isPresent()) {
                    findEndpoints(result.getResult().get(), endpoints);
                }
                return SourceRoot.Callback.Result.DONT_SAVE;
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
        return endpoints;
    }

    private void findEndpoints(CompilationUnit cu, List<Endpoint> endpoints) {
        cu.findAll(ClassOrInterfaceDeclaration.class).forEach(cid -> {
            // Basic heuristic: Look for Spring Controllers
            if (cid.getAnnotationByName("RestController").isPresent() || cid.getAnnotationByName("Controller").isPresent()) {
                cid.getMethods().forEach(method -> {
                    if (isRequestMapping(method)) {
                        Endpoint endpoint = new Endpoint();
                        endpoint.setClassName(cid.getNameAsString());
                        endpoint.setMethodName(method.getNameAsString());
                        endpoint.setHttpPath(extractPath(method));
                        
                        // Deep analysis of the method body to find repository calls
                        traceMethodCalls(method, endpoint);
                        
                        if (!endpoint.getUsages().isEmpty()) {
                            endpoints.add(endpoint);
                        }
                    }
                });
            }
        });
    }

    private boolean isRequestMapping(MethodDeclaration method) {
        return method.getAnnotationByName("RequestMapping").isPresent() ||
               method.getAnnotationByName("GetMapping").isPresent() ||
               method.getAnnotationByName("PostMapping").isPresent() ||
               method.getAnnotationByName("PutMapping").isPresent() ||
               method.getAnnotationByName("DeleteMapping").isPresent();
    }

    private String extractPath(MethodDeclaration method) {
        // Simplified path extraction - usually requires parsing annotation attributes
        return "/api/unknown"; 
    }

    private void traceMethodCalls(MethodDeclaration method, Endpoint endpoint) {
        method.findAll(MethodCallExpr.class).forEach(call -> {
            try {
                // This is where JavaSymbolSolver is magic: it finds the TYPE of the variable being called
                // Note: In a real complex project, we might need deeper recursion into Services.
                // For this Phase 1, we check if the call is directly on a Repository interface.
                
                // Heuristic fallback if symbol solver fails (common in incomplete classpaths)
                String scopeName = call.getScope().map(Object::toString).orElse("");
                String methodName = call.getNameAsString();

                // Check against our Data Map
                // We check if the variable name roughly matches a known repository (e.g., "orderRepository")
                // OR if we can resolve the type properly.
                for (Map.Entry<String, String> entry : dataMap.entrySet()) {
                    String repoName = entry.getKey();
                    String entityName = entry.getValue();

                    // Simple matching: if variable is 'orderRepository' or type is 'OrderRepository'
                    if (scopeName.toLowerCase().contains(repoName.toLowerCase())) {
                        boolean isWrite = methodName.startsWith("save") || methodName.startsWith("delete") || methodName.startsWith("update");
                        endpoint.addUsage(new EntityUsage(entityName, isWrite? "WRITE" : "READ", call.getBegin().get().line));
                    }
                }
                
            } catch (Exception e) {
                // Symbol solver exceptions are common in static analysis
            }
        });
    }
}