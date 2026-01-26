package com.research.staticanalysis.analyzer;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.research.staticanalysis.model.Endpoint;
import com.research.staticanalysis.model.EntityUsage;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

public class EndpointAnalyzer {

    private final Map<String, String> dataMap;

    public EndpointAnalyzer(Map<String, String> dataMap) {
        this.dataMap = dataMap;
    }

    public List<Endpoint> analyze(File root) {
        List<Endpoint> endpoints = new ArrayList<>();
        System.out.println("Scanning for Endpoints in: " + root.getAbsolutePath());

        try (Stream<Path> paths = Files.walk(root.toPath())) {
            paths.filter(p -> p.toString().endsWith(".java"))
                .forEach(path -> {
                     try {
                         CompilationUnit cu = StaticJavaParser.parse(path);
                         findEndpoints(cu, endpoints);
                     } catch (Exception e) {
                         // Ignore parsing errors
                     }
                 });
        } catch (Exception e) {
            e.printStackTrace();
        }
        return endpoints;
    }

    private void findEndpoints(CompilationUnit cu, List<Endpoint> endpoints) {
        cu.findAll(ClassOrInterfaceDeclaration.class).forEach(cid -> {
            // Check for Controller annotations
            if (cid.getAnnotationByName("RestController").isPresent() || 
                cid.getAnnotationByName("Controller").isPresent()) {
                
                cid.getMethods().forEach(method -> {
                    if (isRequestMapping(method)) {
                        Endpoint endpoint = new Endpoint();
                        endpoint.setClassName(cid.getNameAsString());
                        endpoint.setMethodName(method.getNameAsString());
                        endpoint.setHttpPath(extractPath(method));
                        
                        traceMethodCalls(method, endpoint);
                        
                        if (!endpoint.getUsages().isEmpty()) {
                            endpoints.add(endpoint);
                            System.out.println("  " + endpoint.getMethodName() + " accesses " + endpoint.getUsages().size() + " entities.");
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
        return "/api/unknown"; 
    }

    private void traceMethodCalls(MethodDeclaration method, Endpoint endpoint) {
        method.findAll(MethodCallExpr.class).forEach(call -> {
            try {
                String scopeName = call.getScope().map(Object::toString).orElse("");
                String methodName = call.getNameAsString();

                for (Map.Entry<String, String> entry : dataMap.entrySet()) {
                    String repoName = entry.getKey();
                    String entityName = entry.getValue();

                    // Heuristic: Match variable name (e.g. "orderRepository") to Class Name ("OrderRepository")
                    // This handles the case where we assume variable names match types slightly loosely
                    if (scopeName.toLowerCase().contains(repoName.toLowerCase().replace("repository", ""))) {
                        boolean isWrite = methodName.startsWith("save") || 
                                          methodName.startsWith("delete") ||
                                          methodName.startsWith("update") ||
                                          methodName.startsWith("insert");
                        
                        endpoint.addUsage(new EntityUsage(entityName, isWrite? "WRITE" : "READ", call.getBegin().get().line));
                    }
                }
            } catch (Exception e) { }
        });
    }
}