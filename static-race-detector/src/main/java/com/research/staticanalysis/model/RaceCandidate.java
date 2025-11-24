package com.research.staticanalysis.model;

public class RaceCandidate {
    private String entity;
    private Endpoint endpoint1;
    private Endpoint endpoint2;
    private String severity;
    private String description;
    // Getters and Setters
    public String getEntity() {
        return entity;
    }
    public void setEntity(String entity) {
        this.entity = entity;
    }
    public Endpoint getEndpoint1() {
        return endpoint1;
    }
    public void setEndpoint1(Endpoint endpoint1) {
        this.endpoint1 = endpoint1;
    }
    public Endpoint getEndpoint2() {
        return endpoint2;
    }
    public void setEndpoint2(Endpoint endpoint2) {
        this.endpoint2 = endpoint2;
    }
    public String getSeverity() {
        return severity;
    }
    public void setSeverity(String severity) {
        this.severity = severity;
    }
    public String getDescription() {
        return description;
    }
    public void setDescription(String description) {
        this.description = description;
    }

}