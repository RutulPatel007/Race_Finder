package com.research.staticanalysis.analyzer;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.stmt.SynchronizedStmt;
import com.github.javaparser.ast.stmt.TryStmt;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Stream;

/**
 * Detects distributed locking patterns to identify race candidates
 * that are already protected by concurrency controls.
 * 
 * Recognized patterns:
 * - java.util.concurrent.locks.Lock (ReentrantLock, etc.)
 * - Spring's @Transactional(isolation = SERIALIZABLE)
 * - Redisson RLock / RedissonClient
 * - Spring Integration LockRegistry
 * - synchronized blocks/methods
 */
public class DistributedLockAnalyzer {

    private final Map<String, String> dataMap; // repo -> entity

    public DistributedLockAnalyzer(Map<String, String> dataMap) {
        this.dataMap = dataMap;
    }

    /**
     * @return Map of "className.methodName" -> set of entity names protected by locks
     */
    public Map<String, Set<String>> analyze(File root) {
        Map<String, Set<String>> lockMap = new HashMap<>();
        System.out.println("Scanning for Distributed Lock Patterns...");

        try (Stream<Path> paths = Files.walk(root.toPath())) {
            paths.filter(p -> p.toString().endsWith(".java"))
                .forEach(path -> {
                    try {
                        CompilationUnit cu = StaticJavaParser.parse(path);
                        analyzeCompilationUnit(cu, lockMap);
                    } catch (Exception e) {
                        // Ignore
                    }
                });
        } catch (Exception e) {
            e.printStackTrace();
        }

        int totalProtected = lockMap.values().stream().mapToInt(Set::size).sum();
        System.out.println("  [LOCK] Found " + lockMap.size() + " lock-protected methods covering " + totalProtected + " entity accesses.");
        return lockMap;
    }

    private void analyzeCompilationUnit(CompilationUnit cu, Map<String, Set<String>> lockMap) {
        cu.findAll(ClassOrInterfaceDeclaration.class).forEach(cid -> {
            if (cid.isInterface()) return;

            String className = cid.getNameAsString();

            // Check for lock-related fields (Lock, RLock, LockRegistry)
            Set<String> lockFieldNames = new HashSet<>();
            for (FieldDeclaration field : cid.getFields()) {
                String fieldType = field.getElementType().asString();
                if (isLockType(fieldType)) {
                    field.getVariables().forEach(v -> lockFieldNames.add(v.getNameAsString()));
                }
            }

            // Build field -> repo type map for entity resolution
            Map<String, String> fieldToRepoType = new HashMap<>();
            for (FieldDeclaration field : cid.getFields()) {
                String fieldType = field.getElementType().asString();
                if (dataMap.containsKey(fieldType)) {
                    field.getVariables().forEach(v -> fieldToRepoType.put(v.getNameAsString(), fieldType));
                }
            }

            for (MethodDeclaration method : cid.getMethods()) {
                String methodKey = className + "." + method.getNameAsString();
                Set<String> protectedEntities = new HashSet<>();

                // Pattern 1: @Transactional(isolation = Isolation.SERIALIZABLE)
                method.getAnnotationByName("Transactional").ifPresent(ann -> {
                    String annStr = ann.toString();
                    if (annStr.contains("SERIALIZABLE")) {
                        // All entities accessed in this method are protected
                        protectedEntities.addAll(getAccessedEntities(method, fieldToRepoType));
                    }
                });

                // Pattern 2: synchronized method
                if (method.isSynchronized()) {
                    protectedEntities.addAll(getAccessedEntities(method, fieldToRepoType));
                }

                // Pattern 3: synchronized blocks
                method.findAll(SynchronizedStmt.class).forEach(syncStmt -> {
                    protectedEntities.addAll(getAccessedEntitiesInNode(syncStmt, fieldToRepoType));
                });

                // Pattern 4: Lock field usage (lock.lock() / lock.tryLock() ... lock.unlock())
                if (!lockFieldNames.isEmpty()) {
                    method.findAll(MethodCallExpr.class).forEach(call -> {
                        String scope = call.getScope().map(Object::toString).orElse("");
                        String name = call.getNameAsString();
                        if (lockFieldNames.contains(scope) &&
                            (name.equals("lock") || name.equals("tryLock"))) {
                            // This method uses a distributed lock — protect all entity accesses
                            protectedEntities.addAll(getAccessedEntities(method, fieldToRepoType));
                        }
                    });
                }

                if (!protectedEntities.isEmpty()) {
                    lockMap.put(methodKey, protectedEntities);
                }
            }
        });
    }

    private boolean isLockType(String typeName) {
        return typeName.equals("Lock") ||
               typeName.equals("ReentrantLock") ||
               typeName.equals("ReadWriteLock") ||
               typeName.equals("ReentrantReadWriteLock") ||
               typeName.equals("RLock") ||
               typeName.equals("RedissonClient") ||
               typeName.equals("LockRegistry") ||
               typeName.equals("RedisLockRegistry") ||
               typeName.contains("Lock"); // Catch custom lock types
    }

    private Set<String> getAccessedEntities(MethodDeclaration method, Map<String, String> fieldToRepoType) {
        return getAccessedEntitiesInNode(method, fieldToRepoType);
    }

    private Set<String> getAccessedEntitiesInNode(com.github.javaparser.ast.Node node, Map<String, String> fieldToRepoType) {
        Set<String> entities = new HashSet<>();
        node.findAll(MethodCallExpr.class).forEach(call -> {
            String scope = call.getScope().map(Object::toString).orElse("");
            for (Map.Entry<String, String> entry : fieldToRepoType.entrySet()) {
                if (scope.equals(entry.getKey())) {
                    String entity = dataMap.get(entry.getValue());
                    if (entity != null) entities.add(entity);
                }
            }
        });
        return entities;
    }
}
