package com.research.staticanalysis.model;

public class EntityUsage {
    private String entityName;
    private String accessType; // READ or WRITE
    private int lineNumber;

    public EntityUsage(String entityName, String accessType, int lineNumber) {
        this.entityName = entityName;
        this.accessType = accessType;
        this.lineNumber = lineNumber;
    }
    public String getEntityName() { return entityName; }
    public String getAccessType() { return accessType; }
}