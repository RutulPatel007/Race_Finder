// mvn clean package
// java -jar target/static-race-detector-1.0-SNAPSHOT.jar ./train-ticket
package com.research.staticanalysis;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.symbolsolver.JavaSymbolSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JavaParserTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.ReflectionTypeSolver;
import com.research.staticanalysis.analyzer.*;
import com.research.staticanalysis.model.Endpoint;
import com.research.staticanalysis.model.EntityUsage;
import com.research.staticanalysis.model.RaceCandidate;
import com.research.staticanalysis.sarif.SarifGenerator;
import picocli.CommandLine;

import java.io.File;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.Callable;

@CommandLine.Command(name = "race-detector", mixinStandardHelpOptions = true, version = "2.0",
        description = "Detects static race conditions in Spring Boot Microservices using the Method of Maps.")
public class Main implements Callable<Integer> {

    @CommandLine.Parameters(index = "0", description = "Root directory of the microservices source code.")
    private File sourceRoot;

    @CommandLine.Option(names = {"-o", "--output"}, description = "Output SARIF file path", defaultValue = "race-report.sarif")
    private String outputPath;

    @CommandLine.Option(names = {"--skip-extensions"}, description = "Skip lock detection and async boundary analysis")
    private boolean skipExtensions;

    @CommandLine.Option(names = {"-v", "--verbose"}, description = "Enable verbose output")
    private boolean verbose;

    public static void main(String[] args) {
        int exitCode = new CommandLine(new Main()).execute(args);
        System.exit(exitCode);
    }

    @Override
    public Integer call() throws Exception {
        System.out.println("╔══════════════════════════════════════════════════════════════╗");
        System.out.println("║     Race Finder — Neurosymbolic Static Race Detector v2.0   ║");
        System.out.println("║     Phase 1: Method of Maps Analysis                        ║");
        System.out.println("╚══════════════════════════════════════════════════════════════╝");
        System.out.println();
        System.out.println("Source Root: " + sourceRoot.getAbsolutePath());
        System.out.println();

        // 1. Configure Symbol Solver
        CombinedTypeSolver combinedSolver = new CombinedTypeSolver();
        combinedSolver.add(new ReflectionTypeSolver());
        combinedSolver.add(new JavaParserTypeSolver(sourceRoot)); 
        
        JavaSymbolSolver symbolSolver = new JavaSymbolSolver(combinedSolver);
        StaticJavaParser.getConfiguration().setSymbolResolver(symbolSolver);

        // ──────────── Step 1: Repository Analysis ────────────
        System.out.println("─── Step 1/5: Building Data Map (Repository → Entity) ───");
        RepositoryAnalyzer repoAnalyzer = new RepositoryAnalyzer();
        var dataMap = repoAnalyzer.analyze(sourceRoot);
        System.out.println("✓ Data Map Built: Found " + dataMap.size() + " repositories.\n");

        // ──────────── Step 2: Service Analysis ────────────
        System.out.println("─── Step 2/5: Building Service Map (Service → Repository) ───");
        ServiceAnalyzer serviceAnalyzer = new ServiceAnalyzer(dataMap);
        var serviceMap = serviceAnalyzer.analyze(sourceRoot);

        int totalServiceMethods = serviceMap.values().stream()
            .mapToInt(m -> m.size()).sum();
        System.out.println("✓ Service Map Built: " + serviceMap.size() + 
                           " services, " + totalServiceMethods + " methods with DB access.\n");

        // ──────────── Step 3: Endpoint Analysis ────────────
        System.out.println("─── Step 3/5: Building Endpoint Map (Controller → Entity) ───");
        EndpointAnalyzer endpointAnalyzer = new EndpointAnalyzer(dataMap, serviceMap);
        var endpointMap = endpointAnalyzer.analyze(sourceRoot);
        System.out.println("✓ Endpoint Map Built: Found " + endpointMap.size() + " endpoints with DB access.\n");

        // ──────────── Step 4: Extension Analysis (Optional) ────────────
        Map<String, Set<String>> lockMap = null;
        List<Endpoint> asyncEndpoints = List.of();

        if (!skipExtensions) {
            System.out.println("─── Step 4/5: Extension Analysis (Lock + Async Detection) ───");
            
            DistributedLockAnalyzer lockAnalyzer = new DistributedLockAnalyzer(dataMap);
            lockMap = lockAnalyzer.analyze(sourceRoot);

            AsyncBoundaryAnalyzer asyncAnalyzer = new AsyncBoundaryAnalyzer(dataMap, serviceMap);
            asyncEndpoints = asyncAnalyzer.analyze(sourceRoot);
            System.out.println();
        } else {
            System.out.println("─── Step 4/5: Skipped (--skip-extensions) ───\n");
        }

        // ──────────── Step 5: Interference Detection ────────────
        System.out.println("─── Step 5/5: Calculating Interference Matrix ───");
        InterferenceEngine engine = new InterferenceEngine(lockMap);
        List<RaceCandidate> races = engine.detectRaces(endpointMap, asyncEndpoints);

        // ──────────── Summary ────────────
        long critical = races.stream()
            .filter(r -> "CRITICAL".equals(r.getSeverity())).count();
        long high = races.stream()
            .filter(r -> "HIGH".equals(r.getSeverity())).count();
        long unprotected = races.stream()
            .filter(r -> r.getProtectionStatus() == RaceCandidate.ProtectionStatus.UNPROTECTED).count();
        long partiallyProtected = races.stream()
            .filter(r -> r.getProtectionStatus() == RaceCandidate.ProtectionStatus.PARTIALLY_PROTECTED).count();
        long fullyProtected = races.stream()
            .filter(r -> r.getProtectionStatus() == RaceCandidate.ProtectionStatus.FULLY_PROTECTED).count();

        System.out.println();
        System.out.println("╔══════════════════════════════════════════════════════════════╗");
        System.out.println("║                     Analysis Summary                        ║");
        System.out.println("╠══════════════════════════════════════════════════════════════╣");
        System.out.printf("║  Total Races Found:          %-30d ║%n", races.size());
        System.out.printf("║  CRITICAL (Write-Write):     %-30d ║%n", critical);
        System.out.printf("║  HIGH (Read-Write):          %-30d ║%n", high);
        System.out.println("╠══════════════════════════════════════════════════════════════╣");
        System.out.printf("║  Unprotected:                %-30d ║%n", unprotected);
        System.out.printf("║  Partially Protected:        %-30d ║%n", partiallyProtected);
        System.out.printf("║  Fully Protected:            %-30d ║%n", fullyProtected);
        System.out.println("╚══════════════════════════════════════════════════════════════╝");

        if (verbose && !races.isEmpty()) {
            System.out.println("\n─── Detailed Results ───");
            for (int i = 0; i < races.size(); i++) {
                RaceCandidate r = races.get(i);
                System.out.printf("[%d] %s | %s | Entity: %s%n", i + 1, r.getSeverity(), 
                                  r.getProtectionStatus(), r.getEntity());
                System.out.printf("    EP1: %s%n", r.getEndpoint1());
                System.out.printf("    EP2: %s%n", r.getEndpoint2());
            }
        }

        // Generate SARIF Report
        SarifGenerator.generate(races, outputPath);
        
        return 0;
    }
}