package com.research.staticanalysis.model;

import java.util.ArrayList;
import java.util.List;

public class Endpoint {
    private String className;
    private String methodName;
    private String httpPath;
    private List<EntityUsage> usages = new ArrayList<>();

    public void addUsage(EntityUsage usage) {
        this.usages.add(usage);
    }

    public boolean writesTo(String entityName) {
        return usages.stream()
               .anyMatch(u -> u.getEntityName().equals(entityName) && u.getAccessType().equals("WRITE"));
    }
    
    // Getters, Setters, equals(), hashCode()
    public String getMethodName() { return methodName; }
    public List<EntityUsage> getUsages() { return usages; }
    public void setClassName(String className) { this.className = className; }
    public void setMethodName(String methodName) { this.methodName = methodName; }
    public void setHttpPath(String httpPath) { this.httpPath = httpPath; }
    public String getClassName() { return className; }
    public String getHttpPath() { return httpPath; }
    
}



