package com.research.staticanalysis.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Endpoint {
    private String className;
    private String methodName;
    private String httpPath;
    private String httpMethod; // GET, POST, PUT, DELETE
    private String sourceFile; // absolute path to the .java file
    private List<EntityUsage> usages = new ArrayList<>();

    public void addUsage(EntityUsage usage) {
        this.usages.add(usage);
    }

    public boolean writesTo(String entityName) {
        return usages.stream()
               .anyMatch(u -> u.getEntityName().equals(entityName) && u.isWrite());
    }

    public boolean readsFrom(String entityName) {
        return usages.stream()
               .anyMatch(u -> u.getEntityName().equals(entityName) && !u.isWrite());
    }

    // --- Getters and Setters ---
    public String getMethodName() { return methodName; }
    public List<EntityUsage> getUsages() { return usages; }
    public void setClassName(String className) { this.className = className; }
    public void setMethodName(String methodName) { this.methodName = methodName; }
    public void setHttpPath(String httpPath) { this.httpPath = httpPath; }
    public String getClassName() { return className; }
    public String getHttpPath() { return httpPath; }
    public String getHttpMethod() { return httpMethod; }
    public void setHttpMethod(String httpMethod) { this.httpMethod = httpMethod; }
    public String getSourceFile() { return sourceFile; }
    public void setSourceFile(String sourceFile) { this.sourceFile = sourceFile; }

    /**
     * Returns a unique identifier for this endpoint: "ClassName.methodName"
     */
    public String getQualifiedName() {
        return className + "." + methodName;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Endpoint endpoint = (Endpoint) o;
        return Objects.equals(className, endpoint.className) &&
               Objects.equals(methodName, endpoint.methodName);
    }

    @Override
    public int hashCode() {
        return Objects.hash(className, methodName);
    }

    @Override
    public String toString() {
        return httpMethod + " " + httpPath + " (" + className + "." + methodName + ")";
    }
}
