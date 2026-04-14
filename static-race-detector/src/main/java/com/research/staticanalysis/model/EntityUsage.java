package com.research.staticanalysis.model;

public class EntityUsage {

    public enum AccessType {
        READ, WRITE
    }

    private String entityName;
    private AccessType accessType;
    private int lineNumber;
    private String sourceFile;

    public EntityUsage(String entityName, AccessType accessType, int lineNumber) {
        this.entityName = entityName;
        this.accessType = accessType;
        this.lineNumber = lineNumber;
    }

    public EntityUsage(String entityName, AccessType accessType, int lineNumber, String sourceFile) {
        this(entityName, accessType, lineNumber);
        this.sourceFile = sourceFile;
    }

    public String getEntityName() { return entityName; }
    public AccessType getAccessType() { return accessType; }
    public int getLineNumber() { return lineNumber; }
    public String getSourceFile() { return sourceFile; }
    public void setSourceFile(String sourceFile) { this.sourceFile = sourceFile; }

    public boolean isWrite() {
        return accessType == AccessType.WRITE;
    }

    @Override
    public String toString() {
        return accessType + "(" + entityName + ") at line " + lineNumber;
    }
}