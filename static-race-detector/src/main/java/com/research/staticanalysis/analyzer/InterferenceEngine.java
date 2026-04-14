package com.research.staticanalysis.analyzer;

import com.research.staticanalysis.model.Endpoint;
import com.research.staticanalysis.model.EntityUsage;
import com.research.staticanalysis.model.RaceCandidate;
import com.research.staticanalysis.model.RaceCandidate.ProtectionStatus;
import com.research.staticanalysis.model.RaceCandidate.RaceType;

import java.util.*;

public class InterferenceEngine {

    // lockMap: "className.methodName" -> set of protected entity names
    private Map<String, Set<String>> lockMap = new HashMap<>();

    public InterferenceEngine() {}

    public InterferenceEngine(Map<String, Set<String>> lockMap) {
        this.lockMap = (lockMap != null) ? lockMap : new HashMap<>();
    }

    public List<RaceCandidate> detectRaces(List<Endpoint> endpoints) {
        return detectRaces(endpoints, Collections.emptyList());
    }

    /**
     * Detects race conditions by pairwise comparison of endpoints (including async boundaries).
     * Deduplicates results and checks lock protection.
     */
    public List<RaceCandidate> detectRaces(List<Endpoint> endpoints, List<Endpoint> asyncEndpoints) {
        List<RaceCandidate> races = new ArrayList<>();
        Set<String> seenPairs = new HashSet<>();

        // Combine REST endpoints and async boundaries into one list
        List<Endpoint> allEndpoints = new ArrayList<>(endpoints);
        allEndpoints.addAll(asyncEndpoints);

        // Group endpoints by the entity they access
        Map<String, List<Endpoint>> entityAccessMap = new HashMap<>();
        for (Endpoint ep : allEndpoints) {
            for (EntityUsage usage : ep.getUsages()) {
                entityAccessMap.computeIfAbsent(usage.getEntityName(), k -> new ArrayList<>()).add(ep);
            }
        }

        // Pairwise interference detection
        for (Map.Entry<String, List<Endpoint>> entry : entityAccessMap.entrySet()) {
            String entity = entry.getKey();
            List<Endpoint> accessors = entry.getValue();

            for (int i = 0; i < accessors.size(); i++) {
                for (int j = i + 1; j < accessors.size(); j++) {
                    Endpoint e1 = accessors.get(i);
                    Endpoint e2 = accessors.get(j);

                    // Skip self-pairs (same endpoint)
                    if (e1.equals(e2)) continue;

                    // Deduplication: normalize the pair key
                    String pairKey = buildPairKey(e1, e2, entity);
                    if (seenPairs.contains(pairKey)) continue;
                    seenPairs.add(pairKey);

                    boolean e1Writes = e1.writesTo(entity);
                    boolean e2Writes = e2.writesTo(entity);

                    // Race condition: W-W or R-W
                    if (e1Writes || e2Writes) {
                        RaceCandidate race = new RaceCandidate();
                        race.setEntity(entity);
                        race.setEndpoint1(e1);
                        race.setEndpoint2(e2);

                        // Set race type
                        if (e1Writes && e2Writes) {
                            race.setRaceType(RaceType.WRITE_WRITE);
                            race.setSeverity("CRITICAL");
                        } else {
                            race.setRaceType(RaceType.READ_WRITE);
                            race.setSeverity("HIGH");
                        }

                        // Check lock protection
                        ProtectionStatus protection = checkProtection(e1, e2, entity);
                        race.setProtectionStatus(protection);

                        // Collect shared entity usages from both endpoints
                        collectSharedUsages(race, e1, e2, entity);

                        race.setDescription(String.format(
                            "Potential %s race on entity [%s]. Endpoints %s (%s) and %s (%s) " +
                            "access it concurrently with at least one WRITE. Protection: %s.",
                            race.getSeverity(), entity,
                            e1.getMethodName(), e1.getHttpMethod(),
                            e2.getMethodName(), e2.getHttpMethod(),
                            protection
                        ));

                        races.add(race);
                    }
                }
            }
        }

        // Sort: CRITICAL first, then UNPROTECTED first
        races.sort((a, b) -> {
            int sevCmp = severityOrder(a.getSeverity()) - severityOrder(b.getSeverity());
            if (sevCmp != 0) return sevCmp;
            return protectionOrder(a.getProtectionStatus()) - protectionOrder(b.getProtectionStatus());
        });

        return races;
    }

    private String buildPairKey(Endpoint e1, Endpoint e2, String entity) {
        String q1 = e1.getQualifiedName();
        String q2 = e2.getQualifiedName();
        // Normalize order so (A,B,entity) == (B,A,entity)
        if (q1.compareTo(q2) > 0) {
            String tmp = q1; q1 = q2; q2 = tmp;
        }
        return q1 + "::" + q2 + "::" + entity;
    }

    private ProtectionStatus checkProtection(Endpoint e1, Endpoint e2, String entity) {
        boolean e1Protected = isProtected(e1, entity);
        boolean e2Protected = isProtected(e2, entity);
        if (e1Protected && e2Protected) return ProtectionStatus.FULLY_PROTECTED;
        if (e1Protected || e2Protected) return ProtectionStatus.PARTIALLY_PROTECTED;
        return ProtectionStatus.UNPROTECTED;
    }

    private boolean isProtected(Endpoint ep, String entity) {
        String key = ep.getClassName() + "." + ep.getMethodName();
        Set<String> protectedEntities = lockMap.get(key);
        return protectedEntities != null && protectedEntities.contains(entity);
    }

    private void collectSharedUsages(RaceCandidate race, Endpoint e1, Endpoint e2, String entity) {
        for (EntityUsage u : e1.getUsages()) {
            if (u.getEntityName().equals(entity)) {
                race.addSharedUsage(u);
            }
        }
        for (EntityUsage u : e2.getUsages()) {
            if (u.getEntityName().equals(entity)) {
                race.addSharedUsage(u);
            }
        }
    }

    private int severityOrder(String severity) {
        return "CRITICAL".equals(severity) ? 0 : 1;
    }

    private int protectionOrder(ProtectionStatus status) {
        if (status == ProtectionStatus.UNPROTECTED) return 0;
        if (status == ProtectionStatus.PARTIALLY_PROTECTED) return 1;
        return 2; // FULLY_PROTECTED
    }
}