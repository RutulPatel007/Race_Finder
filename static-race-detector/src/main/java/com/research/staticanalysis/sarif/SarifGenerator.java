package com.research.staticanalysis.sarif;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.research.staticanalysis.model.EntityUsage;
import com.research.staticanalysis.model.RaceCandidate;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

/**
 * Generates a SARIF 2.1.0 compliant report with full location information,
 * severity differentiation, and rule definitions.
 */
public class SarifGenerator {

    public static void generate(List<RaceCandidate> candidates, String outputPath) {
        JsonObject sarif = new JsonObject();
        sarif.addProperty("$schema", "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json");
        sarif.addProperty("version", "2.1.0");

        JsonArray runs = new JsonArray();
        JsonObject run = new JsonObject();

        // Tool section with rule definitions
        JsonObject tool = new JsonObject();
        JsonObject driver = new JsonObject();
        driver.addProperty("name", "MethodOfMaps-Analyzer");
        driver.addProperty("version", "2.0.0");
        driver.addProperty("informationUri", "https://github.com/RutulPatel007/Race_Finder");

        JsonArray rules = new JsonArray();

        // RACE-001: Write-Write conflict
        JsonObject ruleWW = new JsonObject();
        ruleWW.addProperty("id", "RACE-WW-001");
        JsonObject shortDescWW = new JsonObject();
        shortDescWW.addProperty("text", "Write-Write data race across distributed endpoints");
        ruleWW.add("shortDescription", shortDescWW);
        JsonObject fullDescWW = new JsonObject();
        fullDescWW.addProperty("text", "Two distinct API endpoints or async handlers concurrently WRITE to the same database entity without distributed lock protection. This can cause lost updates, inconsistent state, or data corruption.");
        ruleWW.add("fullDescription", fullDescWW);
        JsonObject defaultConfigWW = new JsonObject();
        defaultConfigWW.addProperty("level", "error");
        ruleWW.add("defaultConfiguration", defaultConfigWW);
        rules.add(ruleWW);

        // RACE-002: Read-Write conflict
        JsonObject ruleRW = new JsonObject();
        ruleRW.addProperty("id", "RACE-RW-001");
        JsonObject shortDescRW = new JsonObject();
        shortDescRW.addProperty("text", "Read-Write data race across distributed endpoints");
        ruleRW.add("shortDescription", shortDescRW);
        JsonObject fullDescRW = new JsonObject();
        fullDescRW.addProperty("text", "One endpoint reads an entity while another concurrently writes to it without distributed lock protection. This is a Check-Then-Act (TOCTOU) vulnerability that can cause stale reads or incorrect business logic.");
        ruleRW.add("fullDescription", fullDescRW);
        JsonObject defaultConfigRW = new JsonObject();
        defaultConfigRW.addProperty("level", "warning");
        ruleRW.add("defaultConfiguration", defaultConfigRW);
        rules.add(ruleRW);

        driver.add("rules", rules);
        tool.add("driver", driver);
        run.add("tool", tool);

        // Results
        JsonArray results = new JsonArray();
        for (RaceCandidate race : candidates) {
            JsonObject result = new JsonObject();

            // Rule and severity
            boolean isWW = race.getRaceType() == RaceCandidate.RaceType.WRITE_WRITE;
            result.addProperty("ruleId", isWW ? "RACE-WW-001" : "RACE-RW-001");
            result.addProperty("level", isWW ? "error" : "warning");

            // Message
            JsonObject message = new JsonObject();
            message.addProperty("text", race.getDescription());
            result.add("message", message);

            // Primary location (endpoint 1)
            JsonArray locations = new JsonArray();
            locations.add(buildLocation(race.getEndpoint1(), race));
            result.add("locations", locations);

            // Related location (endpoint 2)
            JsonArray relatedLocations = new JsonArray();
            JsonObject relLoc = buildLocation(race.getEndpoint2(), race);
            relLoc.addProperty("id", 1);
            JsonObject relMsg = new JsonObject();
            relMsg.addProperty("text", "Second conflicting endpoint: " + race.getEndpoint2().getQualifiedName());
            relLoc.add("message", relMsg);
            relatedLocations.add(relLoc);
            result.add("relatedLocations", relatedLocations);

            // Properties (custom metadata)
            JsonObject properties = new JsonObject();
            properties.addProperty("entity", race.getEntity());
            properties.addProperty("raceType", race.getRaceType().name());
            properties.addProperty("protectionStatus", race.getProtectionStatus().name());
            properties.addProperty("endpoint1", race.getEndpoint1().toString());
            properties.addProperty("endpoint2", race.getEndpoint2().toString());
            result.add("properties", properties);

            results.add(result);
        }
        
        run.add("results", results);
        runs.add(run);
        sarif.add("runs", runs);

        try (FileWriter writer = new FileWriter(outputPath)) {
            Gson gson = new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create();
            gson.toJson(sarif, writer);
            System.out.println("Report written to: " + outputPath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static JsonObject buildLocation(com.research.staticanalysis.model.Endpoint endpoint,
                                             RaceCandidate race) {
        JsonObject location = new JsonObject();
        JsonObject physLoc = new JsonObject();
        JsonObject artifactLoc = new JsonObject();

        // Use real file path if available
        String uri = endpoint.getSourceFile() != null ? endpoint.getSourceFile() : 
                     endpoint.getClassName() + ".java";
        artifactLoc.addProperty("uri", uri);
        physLoc.add("artifactLocation", artifactLoc);

        // Add line number from the first shared entity usage for this endpoint
        for (EntityUsage usage : race.getSharedEntityUsages()) {
            if (usage.getLineNumber() > 0) {
                JsonObject region = new JsonObject();
                region.addProperty("startLine", usage.getLineNumber());
                physLoc.add("region", region);
                break;
            }
        }

        location.add("physicalLocation", physLoc);
        return location;
    }
}