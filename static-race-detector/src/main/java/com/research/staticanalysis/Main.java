package com.research.staticanalysis;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.symbolsolver.JavaSymbolSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JavaParserTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.ReflectionTypeSolver;
import com.research.staticanalysis.analyzer.EndpointAnalyzer;
import com.research.staticanalysis.analyzer.InterferenceEngine;
import com.research.staticanalysis.analyzer.RepositoryAnalyzer;
import com.research.staticanalysis.model.RaceCandidate;
import com.research.staticanalysis.sarif.SarifGenerator;
import picocli.CommandLine;

import java.io.File;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.Callable;

@CommandLine.Command(name = "race-detector", mixinStandardHelpOptions = true, version = "1.0",
        description = "Detects static race conditions in Spring Boot Microservices.")
public class Main implements Callable<Integer> {

    @CommandLine.Parameters(index = "0", description = "Root directory of the microservices source code.")
    private File sourceRoot;

    public static void main(String args) {
        int exitCode = new CommandLine(new Main()).execute(args);
        System.exit(exitCode);
    }

    @Override
    public Integer call() throws Exception {
        System.out.println("Phase 1: Initializing 'Method of Maps' Static Analysis...");
        System.out.println("Source Root: " + sourceRoot.getAbsolutePath());

        // 1. Configure Symbol Solver (The "Brain" that understands types)
        CombinedTypeSolver combinedSolver = new CombinedTypeSolver();
        combinedSolver.add(new ReflectionTypeSolver()); // JDK classes
        // We assume a standard Maven multi-module layout, so we add the root
        // In a real scenario, we might iterate subdirectories to find src/main/java
        combinedSolver.add(new JavaParserTypeSolver(sourceRoot)); 
        
        JavaSymbolSolver symbolSolver = new JavaSymbolSolver(combinedSolver);
        StaticJavaParser.getConfiguration().setSymbolResolver(symbolSolver);

        // 2. Build the Data Map (Repositories -> Entities)
        RepositoryAnalyzer repoAnalyzer = new RepositoryAnalyzer();
        var dataMap = repoAnalyzer.analyze(sourceRoot);
        System.out.println("Data Map Built: Found " + dataMap.size() + " repositories.");

        // 3. Build the Endpoint Map (Controllers -> Repositories)
        EndpointAnalyzer endpointAnalyzer = new EndpointAnalyzer(dataMap);
        var endpointMap = endpointAnalyzer.analyze(sourceRoot);
        System.out.println("Endpoint Map Built: Found " + endpointMap.size() + " endpoints with DB access.");

        // 4. Calculate Interference (The "Race Detection")
        InterferenceEngine engine = new InterferenceEngine();
        List<RaceCandidate> races = engine.detectRaces(endpointMap);
        System.out.println("Analysis Complete. Found " + races.size() + " potential race conditions.");

        // 5. Generate Report
        SarifGenerator.generate(races, "race-report.sarif");
        
        return 0;
    }
}