package com.research.staticanalysis.analyzer;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.AnnotationExpr;
import com.github.javaparser.ast.expr.MemberValuePair;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NormalAnnotationExpr;
import com.github.javaparser.ast.expr.SingleMemberAnnotationExpr;
import com.research.staticanalysis.model.Endpoint;
import com.research.staticanalysis.model.EntityUsage;
import com.research.staticanalysis.model.EntityUsage.AccessType;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Stream;

/**
 * Detects asynchronous execution boundaries that create implicit
 * concurrent access paths beyond REST endpoints.
 * 
 * Recognized patterns:
 * - @KafkaListener / KafkaTemplate.send()
 * - @RabbitListener / RabbitTemplate.convertAndSend()
 * - @Async methods
 * - @Scheduled methods
 * - @EventListener methods
 * - CompletableFuture.supplyAsync() / ExecutorService.submit()
 */
public class AsyncBoundaryAnalyzer {

    private final Map<String, String> dataMap;
    private final Map<String, Map<String, List<EntityUsage>>> serviceMap;

    public AsyncBoundaryAnalyzer(Map<String, String> dataMap,
                                  Map<String, Map<String, List<EntityUsage>>> serviceMap) {
        this.dataMap = dataMap;
        this.serviceMap = serviceMap;
    }

    /**
     * Returns a list of "virtual endpoints" representing async entry points
     * that access database entities. These are fed into the InterferenceEngine
     * alongside REST endpoints.
     */
    public List<Endpoint> analyze(File root) {
        List<Endpoint> asyncEndpoints = new ArrayList<>();
        System.out.println("Scanning for Async Boundaries...");

        try (Stream<Path> paths = Files.walk(root.toPath())) {
            paths.filter(p -> p.toString().endsWith(".java"))
                .forEach(path -> {
                    try {
                        CompilationUnit cu = StaticJavaParser.parse(path);
                        findAsyncBoundaries(cu, asyncEndpoints, path.toString());
                    } catch (Exception e) {
                        // Ignore
                    }
                });
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("  [ASYNC] Found " + asyncEndpoints.size() + " async boundaries with DB access.");
        return asyncEndpoints;
    }

    private void findAsyncBoundaries(CompilationUnit cu, List<Endpoint> asyncEndpoints, String filePath) {
        cu.findAll(ClassOrInterfaceDeclaration.class).forEach(cid -> {
            if (cid.isInterface()) return;

            String className = cid.getNameAsString();

            // Build field type map for entity resolution
            Map<String, String> fieldToRepoType = new HashMap<>();
            Map<String, String> fieldTypeMap = new HashMap<>();
            for (FieldDeclaration field : cid.getFields()) {
                String fieldType = field.getElementType().asString();
                field.getVariables().forEach(v -> {
                    fieldTypeMap.put(v.getNameAsString(), fieldType);
                    if (dataMap.containsKey(fieldType)) {
                        fieldToRepoType.put(v.getNameAsString(), fieldType);
                    }
                });
            }

            for (MethodDeclaration method : cid.getMethods()) {
                String asyncType = detectAsyncType(method);
                if (asyncType == null) continue;

                // Trace entity accesses in this async method
                List<EntityUsage> usages = traceEntityAccesses(method, fieldToRepoType, fieldTypeMap, filePath);
                if (!usages.isEmpty()) {
                    Endpoint ep = new Endpoint();
                    ep.setClassName(className);
                    ep.setMethodName(method.getNameAsString());
                    ep.setSourceFile(filePath);
                    ep.setHttpMethod(asyncType); // e.g., "KAFKA", "ASYNC", "SCHEDULED"
                    ep.setHttpPath(extractAsyncPath(method, asyncType));

                    for (EntityUsage u : usages) {
                        ep.addUsage(u);
                    }

                    asyncEndpoints.add(ep);
                    System.out.println("  [ASYNC] " + asyncType + " " + className + "." + method.getNameAsString() +
                                       " accesses " + usages.size() + " entities");
                }
            }
        });
    }

    /**
     * Returns the async type annotation on this method, or null if not async.
     */
    private String detectAsyncType(MethodDeclaration method) {
        if (method.getAnnotationByName("KafkaListener").isPresent()) return "KAFKA";
        if (method.getAnnotationByName("RabbitListener").isPresent()) return "RABBIT";
        if (method.getAnnotationByName("Async").isPresent()) return "ASYNC";
        if (method.getAnnotationByName("Scheduled").isPresent()) return "SCHEDULED";
        if (method.getAnnotationByName("EventListener").isPresent()) return "EVENT";
        if (method.getAnnotationByName("StreamListener").isPresent()) return "STREAM";
        return null;
    }

    /**
     * Extracts the topic/queue name from async annotations.
     */
    private String extractAsyncPath(MethodDeclaration method, String asyncType) {
        String annotationName;
        if ("KAFKA".equals(asyncType)) annotationName = "KafkaListener";
        else if ("RABBIT".equals(asyncType)) annotationName = "RabbitListener";
        else if ("SCHEDULED".equals(asyncType)) annotationName = "Scheduled";
        else if ("EVENT".equals(asyncType)) annotationName = "EventListener";
        else if ("STREAM".equals(asyncType)) annotationName = "StreamListener";
        else annotationName = null;

        if (annotationName != null) {
            Optional<AnnotationExpr> ann = method.getAnnotationByName(annotationName);
            if (ann.isPresent()) {
                AnnotationExpr a = ann.get();
                if (a instanceof SingleMemberAnnotationExpr) {
                    return ((SingleMemberAnnotationExpr) a).getMemberValue().toString().replace("\"", "");
                }
                if (a instanceof NormalAnnotationExpr) {
                    for (MemberValuePair pair : ((NormalAnnotationExpr) a).getPairs()) {
                        if (pair.getNameAsString().equals("topics") ||
                            pair.getNameAsString().equals("queues") ||
                            pair.getNameAsString().equals("value") ||
                            pair.getNameAsString().equals("cron")) {
                            return pair.getValue().toString().replace("\"", "");
                        }
                    }
                }
            }
        }
        return "@" + asyncType.toLowerCase();
    }

    private List<EntityUsage> traceEntityAccesses(MethodDeclaration method,
                                                    Map<String, String> fieldToRepoType,
                                                    Map<String, String> fieldTypeMap,
                                                    String filePath) {
        List<EntityUsage> usages = new ArrayList<>();

        method.findAll(MethodCallExpr.class).forEach(call -> {
            try {
                String scopeName = call.getScope().map(Object::toString).orElse("");
                String calledMethod = call.getNameAsString();
                int line = call.getBegin().map(p -> p.line).orElse(0);

                // Direct repository calls
                if (fieldToRepoType.containsKey(scopeName)) {
                    String repoType = fieldToRepoType.get(scopeName);
                    String entity = dataMap.get(repoType);
                    if (entity != null) {
                        usages.add(new EntityUsage(entity, ServiceAnalyzer.classifyAccess(calledMethod), line, filePath));
                    }
                }

                // Service-delegated calls
                String fieldType = fieldTypeMap.get(scopeName);
                if (fieldType != null && !fieldToRepoType.containsKey(scopeName)) {
                    // Look up service in serviceMap
                    Map<String, List<EntityUsage>> methodUsages = findServiceMethods(fieldType);
                    if (methodUsages != null && methodUsages.containsKey(calledMethod)) {
                        for (EntityUsage svcUsage : methodUsages.get(calledMethod)) {
                            usages.add(new EntityUsage(svcUsage.getEntityName(), svcUsage.getAccessType(), line, filePath));
                        }
                    }
                }
            } catch (Exception e) { }
        });

        return usages;
    }

    private Map<String, List<EntityUsage>> findServiceMethods(String fieldType) {
        // Try exact match
        Map<String, List<EntityUsage>> result = serviceMap.get(fieldType);
        if (result != null) return result;

        // Try Impl suffix
        result = serviceMap.get(fieldType + "Impl");
        if (result != null) return result;

        // Try fuzzy match
        for (Map.Entry<String, Map<String, List<EntityUsage>>> entry : serviceMap.entrySet()) {
            String svcName = entry.getKey();
            if (svcName.startsWith(fieldType.replace("Service", "")) && svcName.endsWith("Impl")) {
                return entry.getValue();
            }
        }
        return null;
    }
}
