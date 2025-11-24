package com.research.staticanalysis.analyzer;

import com.research.staticanalysis.model.Endpoint;
import com.research.staticanalysis.model.EntityUsage;
import com.research.staticanalysis.model.RaceCandidate;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class InterferenceEngine {

    public List<RaceCandidate> detectRaces(List<Endpoint> endpoints) {
        List<RaceCandidate> races = new ArrayList<>();
        
        // Group endpoints by the Entity they access
        Map<String, List<Endpoint>> entityAccessMap = new HashMap<>();

        for (Endpoint ep : endpoints) {
            for (EntityUsage usage : ep.getUsages()) {
                entityAccessMap.computeIfAbsent(usage.getEntityName(), k -> new ArrayList<>()).add(ep);
            }
        }

        // Iterate through entities to find conflicts
        for (Map.Entry<String, List<Endpoint>> entry : entityAccessMap.entrySet()) {
            String entity = entry.getKey();
            List<Endpoint> accessors = entry.getValue();

            // Naive O(N^2) comparison for the pair-wise interference matrix
            for (int i = 0; i < accessors.size(); i++) {
                for (int j = i + 1; j < accessors.size(); j++) {
                    Endpoint e1 = accessors.get(i);
                    Endpoint e2 = accessors.get(j);

                    // Check if they are different endpoints
                    if (e1.equals(e2)) continue;

                    boolean e1Writes = e1.writesTo(entity);
                    boolean e2Writes = e2.writesTo(entity);

                    // RACE CONDITION: (Write-Write) or (Read-Write)
                    if (e1Writes || e2Writes) {
                        RaceCandidate race = new RaceCandidate();
                        race.setEntity(entity);
                        race.setEndpoint1(e1);
                        race.setEndpoint2(e2);
                        race.setSeverity(e1Writes && e2Writes? "CRITICAL" : "HIGH");
                        race.setDescription("Potential " + race.getSeverity() + " race on entity " + entity + 
                                          ". Endpoints " + e1.getMethodName() + " and " + e2.getMethodName() + 
                                          " access it concurrently with at least one WRITE.");
                        races.add(race);
                    }
                }
            }
        }
        return races;
    }
}