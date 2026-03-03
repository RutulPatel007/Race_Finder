# 🏁 Race Finder — Static Race Condition Detector for Spring Boot Microservices

A static analysis tool that detects potential **data-race conditions** across Spring Boot microservice endpoints. It uses the **"Method of Maps"** approach to identify concurrent API endpoints that perform conflicting Read/Write or Write/Write operations on the same database entity — without ever running the application.

---

## 📖 Overview

In microservice architectures, multiple API endpoints can concurrently access the same database entity through different services. When at least one of those accesses is a **write**, a data-race condition can occur, leading to inconsistent state, lost updates, or corrupt data.

**Race Finder** performs the following analysis pipeline:

```
Source Code → Repository Map → Endpoint Map → Interference Detection → SARIF Report
```

| Phase | Component | Description |
|-------|-----------|-------------|
| **1** | `RepositoryAnalyzer` | Scans all Java files and builds a **Data Map** — mapping Spring Data repository interfaces (e.g., `JpaRepository`, `CrudRepository`, `MongoRepository`) to the entities they manage. |
| **2** | `EndpointAnalyzer` | Identifies REST controller endpoints (annotated with `@RequestMapping`, `@GetMapping`, `@PostMapping`, etc.) and traces which repositories (and therefore entities) each endpoint accesses. |
| **3** | `InterferenceEngine` | Performs pairwise interference analysis across all endpoints. If two distinct endpoints access the **same entity** and at least one performs a **WRITE**, a race candidate is flagged. |
| **4** | `SarifGenerator` | Outputs all detected race candidates as a **SARIF 2.1.0** report for integration with CI/CD and code-scanning tools (e.g., GitHub Code Scanning, VS Code SARIF Viewer). |

### Severity Levels

| Severity | Condition |
|----------|-----------|
| **CRITICAL** | Both endpoints **write** to the same entity (Write-Write conflict) |
| **HIGH** | One endpoint **reads** while another **writes** to the same entity (Read-Write conflict) |

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Java** | 17 | Language runtime |
| **Maven** | 3.x | Build tool |
| **JavaParser** | 3.25.10 | Java source code parsing and AST analysis |
| **Picocli** | 4.7.5 | CLI argument parsing |
| **Gson** | 2.10.1 | JSON/SARIF report generation |

---

## 🚀 Getting Started

### Prerequisites

- **Java 17** or later
- **Apache Maven 3.x**

### Build

```bash
cd static-race-detector
mvn clean package
```

This produces a self-contained uber JAR at:

```
static-race-detector/target/static-race-detector-1.0-SNAPSHOT.jar
```

### Run

```bash
java -jar target/static-race-detector-1.0-SNAPSHOT.jar <path-to-microservice-source>
```

**Example** — Analyze the bundled `train-ticket` application:

```bash
java -jar target/static-race-detector-1.0-SNAPSHOT.jar ./train-ticket
```

### Output

The tool prints analysis progress to stdout and writes a `race-report.sarif` file in the current directory:

```
Phase 1: Initializing 'Method of Maps' Static Analysis...
Source Root: /path/to/train-ticket
Data Map Built: Found 12 repositories.
Endpoint Map Built: Found 37 endpoints with DB access.
Analysis Complete. Found 5 potential race conditions.
Report written to: race-report.sarif
```

---

## 📁 Project Structure

```
Race_Finder/
├── README.md
├── Race_Finder.pdf                          # Research paper / documentation
└── static-race-detector/
    ├── pom.xml                              # Maven build configuration
    ├── race-report.sarif                    # Sample SARIF output
    ├── src/main/java/com/research/staticanalysis/
    │   ├── Main.java                        # CLI entry point
    │   ├── analyzer/
    │   │   ├── RepositoryAnalyzer.java      # Phase 1: Repository → Entity mapping
    │   │   ├── EndpointAnalyzer.java        # Phase 2: Endpoint → Repository tracing
    │   │   └── InterferenceEngine.java      # Phase 3: Pairwise race detection
    │   ├── model/
    │   │   ├── Endpoint.java                # REST endpoint model
    │   │   ├── EntityUsage.java             # Entity access (READ/WRITE) model
    │   │   └── RaceCandidate.java           # Detected race condition model
    │   └── sarif/
    │       └── SarifGenerator.java          # Phase 4: SARIF 2.1.0 report generator
    │
    ├── # Bundled test subject applications:
    ├── train-ticket/                        # Train ticket booking microservices
    ├── ftgo-application/                    # FTGO food delivery microservices
    ├── spring-petclinic-microservices/       # Spring PetClinic (microservices variant)
    ├── flowing-retail/                      # Flowing Retail event-driven microservices
    ├── Axon-trader/                         # Axon Framework trading application
    └── eventuate-tram-examples-customers-and-orders/
```

---

## 📄 SARIF Report Format

The output follows the [SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html) standard. Each detected race is reported with:

- **Rule ID**: `RACE-001`
- **Level**: `error`
- **Message**: Description of the conflicting endpoints and shared entity
- **Location**: Source file of the first endpoint involved

```json
{
  "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
  "version": "2.1.0",
  "runs": [{
    "tool": { "driver": { "name": "MethodOfMaps-Analyzer" } },
    "results": [{
      "ruleId": "RACE-001",
      "level": "error",
      "message": {
        "text": "Potential CRITICAL race on entity Order. Endpoints createOrder and cancelOrder access it concurrently with at least one WRITE."
      },
      "locations": [{ "physicalLocation": { "artifactLocation": { "uri": "OrderController.java" } } }]
    }]
  }]
}
```

---

## 🧪 Bundled Test Applications

The following open-source microservice applications are included as test subjects for analysis:

| Application | Description |
|-------------|-------------|
| [train-ticket](https://github.com/FudanSELab/train-ticket) | Large-scale train ticket booking system with 40+ microservices |
| [ftgo-application](https://github.com/microservices-patterns/ftgo-application) | Food delivery app from *Microservices Patterns* by Chris Richardson |
| [spring-petclinic-microservices](https://github.com/spring-petclinic/spring-petclinic-microservices) | Classic Spring PetClinic decomposed into microservices |
| [flowing-retail](https://github.com/berndruecker/flowing-retail) | Event-driven retail workflow demonstration |
| [Axon-trader](https://github.com/AxonFramework/Axon-trader) | CQRS/Event Sourcing trading platform built with Axon Framework |
| [eventuate-tram-examples](https://github.com/eventuate-tram/eventuate-tram-examples-customers-and-orders) | Eventuate Tram saga-based customers & orders example |

---

## 📝 License

This project is developed for **academic research purposes**.
