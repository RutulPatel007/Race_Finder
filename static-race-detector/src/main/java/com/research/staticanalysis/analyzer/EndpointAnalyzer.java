package com.research.staticanalysis.analyzer;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.AnnotationExpr;
import com.github.javaparser.ast.expr.MemberValuePair;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.SingleMemberAnnotationExpr;
import com.github.javaparser.ast.expr.NormalAnnotationExpr;
import com.research.staticanalysis.model.Endpoint;
import com.research.staticanalysis.model.EntityUsage;
import com.research.staticanalysis.model.EntityUsage.AccessType;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Stream;

/**
 * Scans for REST controller endpoints and traces their entity accesses
 * through both direct repository calls and service-layer delegation.
 */
public class EndpointAnalyzer {

    // repo class name -> entity name
    private final Map<String, String> dataMap;

    // service class name -> { method name -> usages }
    private final Map<String, Map<String, List<EntityUsage>>> serviceMap;

    public EndpointAnalyzer(Map<String, String> dataMap,
                            Map<String, Map<String, List<EntityUsage>>> serviceMap) {
        this.dataMap = dataMap;
        this.serviceMap = serviceMap;
    }

    public List<Endpoint> analyze(File root) {
        List<Endpoint> endpoints = new ArrayList<>();
        System.out.println("Scanning for Endpoints in: " + root.getAbsolutePath());

        try (Stream<Path> paths = Files.walk(root.toPath())) {
            paths.filter(p -> p.toString().endsWith(".java"))
                .forEach(path -> {
                     try {
                         CompilationUnit cu = StaticJavaParser.parse(path);
                         findEndpoints(cu, endpoints, path.toString());
                     } catch (Exception e) {
                         // Ignore parsing errors
                     }
                 });
        } catch (Exception e) {
            e.printStackTrace();
        }
        return endpoints;
    }

    private void findEndpoints(CompilationUnit cu, List<Endpoint> endpoints, String filePath) {
        cu.findAll(ClassOrInterfaceDeclaration.class).forEach(cid -> {
            if (cid.getAnnotationByName("RestController").isPresent() || 
                cid.getAnnotationByName("Controller").isPresent()) {
                
                // Extract class-level base path from @RequestMapping
                String basePath = extractClassBasePath(cid);
                
                // Build field name -> type map for this controller
                Map<String, String> fieldTypeMap = buildFieldTypeMap(cid);
                
                cid.getMethods().forEach(method -> {
                    String httpMethod = getHttpMethod(method);
                    if (httpMethod != null) {
                        Endpoint endpoint = new Endpoint();
                        endpoint.setClassName(cid.getNameAsString());
                        endpoint.setMethodName(method.getNameAsString());
                        endpoint.setSourceFile(filePath);
                        endpoint.setHttpMethod(httpMethod);
                        endpoint.setHttpPath(basePath + extractMethodPath(method));
                        
                        // Trace entity accesses through two tiers
                        traceDirectRepoCalls(method, endpoint, fieldTypeMap, filePath);
                        traceServiceDelegation(method, endpoint, fieldTypeMap, filePath);
                        
                        if (!endpoint.getUsages().isEmpty()) {
                            endpoints.add(endpoint);
                            System.out.println("  [EP] " + endpoint);
                        }
                    }
                });
            }
        });
    }

    /**
     * Extract base path from class-level @RequestMapping annotation.
     */
    private String extractClassBasePath(ClassOrInterfaceDeclaration cid) {
        Optional<AnnotationExpr> ann = cid.getAnnotationByName("RequestMapping");
        if (ann.isPresent()) {
            return extractPathFromAnnotation(ann.get());
        }
        return "";
    }

    /**
     * Build a map of fieldName -> fieldTypeName for all fields in this class.
     * Used for resolving method call scopes to their types.
     */
    private Map<String, String> buildFieldTypeMap(ClassOrInterfaceDeclaration cid) {
        Map<String, String> fieldTypeMap = new HashMap<>();
        for (FieldDeclaration field : cid.getFields()) {
            String fieldType = field.getElementType().asString();
            field.getVariables().forEach(v -> {
                fieldTypeMap.put(v.getNameAsString(), fieldType);
            });
        }
        return fieldTypeMap;
    }

    /**
     * Determine the HTTP method from the annotation on a handler method.
     * Returns null if this isn't a request handler.
     */
    private String getHttpMethod(MethodDeclaration method) {
        if (method.getAnnotationByName("GetMapping").isPresent()) return "GET";
        if (method.getAnnotationByName("PostMapping").isPresent()) return "POST";
        if (method.getAnnotationByName("PutMapping").isPresent()) return "PUT";
        if (method.getAnnotationByName("DeleteMapping").isPresent()) return "DELETE";
        if (method.getAnnotationByName("PatchMapping").isPresent()) return "PATCH";
        if (method.getAnnotationByName("RequestMapping").isPresent()) {
            // Try to extract method from @RequestMapping(method = RequestMethod.GET)
            AnnotationExpr ann = method.getAnnotationByName("RequestMapping").get();
            if (ann instanceof NormalAnnotationExpr) {
                for (MemberValuePair pair : ((NormalAnnotationExpr) ann).getPairs()) {
                    if (pair.getNameAsString().equals("method")) {
                        String val = pair.getValue().toString();
                        if (val.contains("GET")) return "GET";
                        if (val.contains("POST")) return "POST";
                        if (val.contains("PUT")) return "PUT";
                        if (val.contains("DELETE")) return "DELETE";
                        if (val.contains("PATCH")) return "PATCH";
                    }
                }
            }
            return "REQUEST"; // fallback for bare @RequestMapping
        }
        return null;
    }

    /**
     * Extracts the path value from a method-level mapping annotation.
     */
    private String extractMethodPath(MethodDeclaration method) {
        String[] annotations = {"GetMapping", "PostMapping", "PutMapping", 
                                "DeleteMapping", "PatchMapping", "RequestMapping"};
        for (String annName : annotations) {
            Optional<AnnotationExpr> ann = method.getAnnotationByName(annName);
            if (ann.isPresent()) {
                return extractPathFromAnnotation(ann.get());
            }
        }
        return "";
    }

    /**
     * Extracts path string from an annotation expression.
     * Handles: @GetMapping("/orders"), @RequestMapping(value="/orders"), @GetMapping(path="/orders")
     */
    private String extractPathFromAnnotation(AnnotationExpr ann) {
        if (ann instanceof SingleMemberAnnotationExpr) {
            String val = ((SingleMemberAnnotationExpr) ann).getMemberValue().toString();
            return cleanPath(val);
        }
        if (ann instanceof NormalAnnotationExpr) {
            for (MemberValuePair pair : ((NormalAnnotationExpr) ann).getPairs()) {
                if (pair.getNameAsString().equals("value") || pair.getNameAsString().equals("path")) {
                    return cleanPath(pair.getValue().toString());
                }
            }
        }
        // Marker annotation with no value: @GetMapping
        return "";
    }

    private String cleanPath(String raw) {
        // Remove quotes, braces (for array values), extra whitespace
        return raw.replace("\"", "").replace("{", "").replace("}", "").trim();
    }

    /**
     * Tier 1: Direct repository calls within the controller method.
     * Checks if the scope of a method call matches a field whose type is a known repository.
     */
    private void traceDirectRepoCalls(MethodDeclaration method, Endpoint endpoint,
                                       Map<String, String> fieldTypeMap, String filePath) {
        method.findAll(MethodCallExpr.class).forEach(call -> {
            try {
                String scopeName = call.getScope().map(Object::toString).orElse("");
                String calledMethod = call.getNameAsString();

                // Check if the scope is a field whose type is a known repository
                String fieldType = fieldTypeMap.get(scopeName);
                if (fieldType != null && dataMap.containsKey(fieldType)) {
                    String entityName = dataMap.get(fieldType);
                    AccessType accessType = ServiceAnalyzer.classifyAccess(calledMethod);
                    int line = call.getBegin().map(p -> p.line).orElse(0);
                    endpoint.addUsage(new EntityUsage(entityName, accessType, line, filePath));
                }
            } catch (Exception e) { }
        });
    }

    /**
     * Tier 2: Service-delegated calls.
     * If a controller method calls a service method, look up the service method
     * in the serviceMap to find transitive entity accesses.
     */
    private void traceServiceDelegation(MethodDeclaration method, Endpoint endpoint,
                                         Map<String, String> fieldTypeMap, String filePath) {
        method.findAll(MethodCallExpr.class).forEach(call -> {
            try {
                String scopeName = call.getScope().map(Object::toString).orElse("");
                String calledMethod = call.getNameAsString();

                // Check if scope is a field whose type is a known service
                String fieldType = fieldTypeMap.get(scopeName);
                if (fieldType != null) {
                    // Look for this service type in the serviceMap
                    // Try exact match first, then try Impl suffix pattern
                    Map<String, List<EntityUsage>> methodUsages = serviceMap.get(fieldType);
                    if (methodUsages == null) {
                        methodUsages = serviceMap.get(fieldType + "Impl");
                    }
                    // Also try: if field type is "ContactsService", service class might be "ContactsServiceImpl"
                    if (methodUsages == null) {
                        for (Map.Entry<String, Map<String, List<EntityUsage>>> entry : serviceMap.entrySet()) {
                            String svcName = entry.getKey();
                            // Match: ContactsServiceImpl implements ContactsService
                            if (svcName.startsWith(fieldType.replace("Service", "")) &&
                                svcName.endsWith("Impl")) {
                                methodUsages = entry.getValue();
                                break;
                            }
                            // Match: interface name equals field type
                            if (svcName.equals(fieldType)) {
                                methodUsages = entry.getValue();
                                break;
                            }
                        }
                    }

                    if (methodUsages != null && methodUsages.containsKey(calledMethod)) {
                        List<EntityUsage> transitiveUsages = methodUsages.get(calledMethod);
                        for (EntityUsage svcUsage : transitiveUsages) {
                            // Propagate the usage to the endpoint with the controller's call site line
                            int line = call.getBegin().map(p -> p.line).orElse(0);
                            endpoint.addUsage(new EntityUsage(
                                svcUsage.getEntityName(),
                                svcUsage.getAccessType(),
                                line,
                                filePath
                            ));
                        }
                    }
                }
            } catch (Exception e) { }
        });
    }
}