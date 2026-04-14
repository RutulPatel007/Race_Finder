package com.research.staticanalysis.model;

import java.util.ArrayList;
import java.util.List;

public class RaceCandidate {

    public enum RaceType {
        WRITE_WRITE, READ_WRITE
    }

    public enum ProtectionStatus {
        UNPROTECTED, PARTIALLY_PROTECTED, FULLY_PROTECTED
    }

    private String entity;
    private Endpoint endpoint1;
    private Endpoint endpoint2;
    private String severity; // CRITICAL or HIGH
    private RaceType raceType;
    private String description;
    private ProtectionStatus protectionStatus = ProtectionStatus.UNPROTECTED;
    private List<EntityUsage> sharedEntityUsages = new ArrayList<>();

    // --- Getters and Setters ---
    public String getEntity() { return entity; }
    public void setEntity(String entity) { this.entity = entity; }

    public Endpoint getEndpoint1() { return endpoint1; }
    public void setEndpoint1(Endpoint endpoint1) { this.endpoint1 = endpoint1; }

    public Endpoint getEndpoint2() { return endpoint2; }
    public void setEndpoint2(Endpoint endpoint2) { this.endpoint2 = endpoint2; }

    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { this.severity = severity; }

    public RaceType getRaceType() { return raceType; }
    public void setRaceType(RaceType raceType) { this.raceType = raceType; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public ProtectionStatus getProtectionStatus() { return protectionStatus; }
    public void setProtectionStatus(ProtectionStatus protectionStatus) { this.protectionStatus = protectionStatus; }

    public List<EntityUsage> getSharedEntityUsages() { return sharedEntityUsages; }
    public void setSharedEntityUsages(List<EntityUsage> sharedEntityUsages) {
        this.sharedEntityUsages = sharedEntityUsages;
    }
    public void addSharedUsage(EntityUsage usage) {
        this.sharedEntityUsages.add(usage);
    }
}