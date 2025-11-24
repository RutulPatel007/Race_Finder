package com.research.staticanalysis.sarif;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.research.staticanalysis.model.RaceCandidate;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class SarifGenerator {
    public static void generate(List<RaceCandidate> candidates, String outputPath) {
        JsonObject sarif = new JsonObject();
        sarif.addProperty("$schema", "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json");
        sarif.addProperty("version", "2.1.0");

        JsonArray runs = new JsonArray();
        JsonObject run = new JsonObject();
        JsonObject tool = new JsonObject();
        JsonObject driver = new JsonObject();
        driver.addProperty("name", "MethodOfMaps-Analyzer");
        tool.add("driver", driver);
        run.add("tool", tool);

        JsonArray results = new JsonArray();
        for (RaceCandidate race : candidates) {
            JsonObject result = new JsonObject();
            result.addProperty("ruleId", "RACE-001");
            result.addProperty("level", "error");
            
            JsonObject message = new JsonObject();
            message.addProperty("text", race.getDescription());
            result.add("message", message);

            // Add location information (simplified for demo)
            JsonArray locations = new JsonArray();
            JsonObject location = new JsonObject();
            JsonObject physLoc = new JsonObject();
            JsonObject artifactLoc = new JsonObject();
            artifactLoc.addProperty("uri", race.getEndpoint1().getClassName() + ".java"); 
            physLoc.add("artifactLocation", artifactLoc);
            location.add("physicalLocation", physLoc);
            locations.add(location);
            
            result.add("locations", locations);
            results.add(result);
        }
        
        run.add("results", results);
        runs.add(run);
        sarif.add("runs", runs);

        try (FileWriter writer = new FileWriter(outputPath)) {
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            gson.toJson(sarif, writer);
            System.out.println("Report written to: " + outputPath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}