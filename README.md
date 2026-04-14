# 🏁 Race Finder — Neurosymbolic Race Condition Detector for Microservices

A **hybrid neurosymbolic verifier** that detects distributed data-race conditions in Spring Boot microservice architectures. It combines rigorous static analysis (Phase 1) with LLM-powered semantic verification (Phase 2) to eliminate false positive fatigue and surface only real concurrency vulnerabilities.

---

## 📖 Overview

In microservice architectures, distributed transactions (Saga pattern) lack strict isolation, making them susceptible to concurrency bugs — Check-Then-Act, Read-Modify-Write, and Lost Update anomalies. **Race Finder** provides an automated CI/CD guardrail to detect these before production.

### Two-Phase Pipeline

```
Source Code ──▶ Phase 1 (Static) ──▶ Phase 2 (Neural) ──▶ Verified Report
                Method of Maps        Gemini Pro + 
                                      Multi-Strategy Pruning
```

| Phase | Description |
|-------|-------------|
| **Phase 1** | Static analysis using JavaParser. Maps API endpoints → services → repositories → entities. Detects interference where concurrent accesses conflict ($W(T_1) \cap (R(T_2) \cup W(T_2)) \neq \emptyset$). |
| **Phase 2** | LLM-driven semantic verification using Google Gemini Pro. A three-layer pruning cascade (static heuristics → self-consistency voting → confidence-weighted filtering) eliminates false positives without requiring labeled data. |

---

## 🔬 Phase 1: Method of Maps Static Analyzer (Java)

### How It Works

| Step | Component | Description |
|------|-----------|-------------|
| **1** | `RepositoryAnalyzer` | Scans for Spring Data repository interfaces (`JpaRepository`, `CrudRepository`, `MongoRepository`, etc.) and maps them to their managed entities. |
| **2** | `ServiceAnalyzer` | **NEW** — Bridges controllers to repositories by tracing `@Service` classes. Maps service methods to the entity operations they perform. |
| **3** | `EndpointAnalyzer` | Identifies REST endpoints (`@GetMapping`, `@PostMapping`, etc.) and traces entity accesses through both direct repo calls and service delegation. |
| **4** | `DistributedLockAnalyzer` | Detects lock-protected entity accesses: `synchronized`, `@Transactional(SERIALIZABLE)`, `ReentrantLock`, Redisson `RLock`, Spring `LockRegistry`. |
| **5** | `AsyncBoundaryAnalyzer` | Detects async execution boundaries: `@KafkaListener`, `@RabbitListener`, `@Async`, `@Scheduled`, `@EventListener`. These become additional concurrent access paths. |
| **6** | `InterferenceEngine` | Pairwise interference detection across all endpoints + async boundaries. Deduplicates results and checks lock protection status. |
| **7** | `SarifGenerator` | Outputs SARIF 2.1.0 report with severity levels, rule definitions, line numbers, and protection status. |

### Severity Levels

| Severity | Rule ID | Condition |
|----------|---------|-----------|
| **CRITICAL** | `RACE-WW-001` | Both endpoints **write** to the same entity (Write-Write) |
| **HIGH** | `RACE-RW-001` | One endpoint **reads** while another **writes** (Read-Write) |

### Protection Status

| Status | Meaning |
|--------|---------|
| `UNPROTECTED` | No concurrency control detected |
| `PARTIALLY_PROTECTED` | One endpoint has lock protection, the other doesn't |
| `FULLY_PROTECTED` | Both endpoints are lock-protected |

---

## 🧠 Phase 2: LLM Verification & Multi-Strategy Pruning (Python)

### Three-Layer Pruning Cascade

Since no labeled data exists for RLHF training, Race Finder uses a **three-layer pruning cascade** that progressively eliminates false positives:

#### Layer 1: Static Heuristic Pruning
Rule-based elimination using code pattern analysis (no LLM needed):

| Rule | Description | Action |
|------|-------------|--------|
| **Lock-Protected** | Entity wrapped in `lock.tryLock()`..`unlock()`, `@Transactional(SERIALIZABLE)` | Suppress |
| **Idempotent Read-Only** | Both accesses are `findBy*` / `getBy*` with no side effects | Demote |
| **Optimistic Locking** | Entity class has `@Version` field | Demote |
| **Event-Sourced** | Entity access goes through `@Aggregate` / `@EventHandler` | Suppress |
| **Same-Controller Internal** | Both endpoints in same class, one calls the other | Demote |
| **Synchronized Access** | Method/block is `synchronized` | Suppress |

#### Layer 2: LLM Self-Consistency Voting
- Sends each candidate to **Gemini Pro N times** (default N=3) with temperature > 0
- Takes **majority vote**: if ≥⌈N/2⌉+1 passes agree, that verdict wins
- Agreement ratio as natural confidence metric (no labeled data needed)

#### Layer 3: Confidence-Weighted Filtering

```
final_score = (0.4 × static_score) + (0.6 × llm_agreement_score)
```

| Score Range | Verdict | Action |
|-------------|---------|--------|
| ≥ 0.7 | `TRUE_POSITIVE` | Confirmed race — report |
| 0.4 – 0.7 | `NEEDS_REVIEW` | Flag for human review |
| < 0.4 | `FALSE_POSITIVE` | Suppress from report |

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Java** | 11+ | Static analysis runtime |
| **Maven** | 3.x | Build tool |
| **JavaParser** | 3.25.10 | Java source code AST parsing |
| **Picocli** | 4.7.5 | CLI argument parsing |
| **Gson** | 2.10.1 | SARIF JSON generation |
| **Python** | 3.9+ | LLM verification pipeline |
| **Google Gemini Pro** | Latest | Semantic race verification |
| **Pydantic** | 2.x | Structured LLM output validation |
| **javalang** | 0.13.0 | Java code slicing for LLM context |
| **Rich** | 13.x | Terminal UI and tables |

---

## 🚀 Getting Started

### Prerequisites

- **Java 11** or later
- **Apache Maven 3.x**
- **Python 3.9+** (for Phase 2)
- **Google API Key** (for Gemini Pro, optional — static-only mode available)

### Phase 1: Build & Run Static Analyzer

```bash
cd static-race-detector
mvn clean package

# Run against any Spring Boot microservice project:
java -jar target/static-race-detector-1.0-SNAPSHOT.jar <path-to-source>

# With verbose output:
java -jar target/static-race-detector-1.0-SNAPSHOT.jar <path-to-source> -v

# Skip extension analysis (lock/async detection):
java -jar target/static-race-detector-1.0-SNAPSHOT.jar <path-to-source> --skip-extensions
```

### Phase 2: Run LLM Verification Pipeline

```bash
cd static-race-detector/llm-verifier

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Full pipeline with Gemini Pro:
export GOOGLE_API_KEY='your-gemini-api-key'
python main.py --sarif ../race-report.sarif --source ../train-ticket

# Static pruning only (no API key needed):
python main.py --sarif ../race-report.sarif --source ../train-ticket --static-only

# Custom thresholds and cost control:
python main.py --sarif ../race-report.sarif --source ../train-ticket \
    --tp-threshold 0.8 --review-threshold 0.5 --max-candidates 50
```

### Example Output

```
╔══════════════════════════════════════════════════════════════╗
║                     Analysis Summary                        ║
╠══════════════════════════════════════════════════════════════╣
║  Total Races Found:          604                            ║
║  CRITICAL (Write-Write):     163                            ║
║  HIGH (Read-Write):          441                            ║
╠══════════════════════════════════════════════════════════════╣
║  Unprotected:                604                            ║
║  Partially Protected:        0                              ║
║  Fully Protected:            0                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📁 Project Structure

```
Race_Finder/
├── README.md
├── Race_Finder.pdf                              # Research paper
└── static-race-detector/
    ├── pom.xml                                  # Maven build
    ├── race-report.sarif                        # Phase 1 SARIF output
    ├── src/main/java/com/research/staticanalysis/
    │   ├── Main.java                            # CLI entry point
    │   ├── analyzer/
    │   │   ├── RepositoryAnalyzer.java          # Repo → Entity mapping
    │   │   ├── ServiceAnalyzer.java             # Service → Repo tracing (NEW)
    │   │   ├── EndpointAnalyzer.java            # Endpoint → Entity tracing
    │   │   ├── InterferenceEngine.java          # Pairwise race detection
    │   │   ├── DistributedLockAnalyzer.java     # Lock detection (NEW)
    │   │   └── AsyncBoundaryAnalyzer.java       # Async boundary detection (NEW)
    │   ├── model/
    │   │   ├── Endpoint.java                    # REST endpoint model
    │   │   ├── EntityUsage.java                 # Entity access model
    │   │   └── RaceCandidate.java               # Detected race model
    │   └── sarif/
    │       └── SarifGenerator.java              # SARIF 2.1.0 report
    │
    ├── llm-verifier/                            # Phase 2 (Python)
    │   ├── requirements.txt
    │   ├── config.py                            # Gemini API + prompts
    │   ├── models.py                            # Pydantic models
    │   ├── sarif_parser.py                      # SARIF input parser
    │   ├── code_slicer.py                       # Java code extraction
    │   ├── llm_verifier.py                      # Gemini Pro client
    │   ├── main.py                              # CLI entry point
    │   └── pruning/
    │       ├── static_pruner.py                 # Layer 1: Heuristic rules
    │       ├── self_consistency.py              # Layer 2: Voting
    │       └── confidence_filter.py             # Layer 3: Final scoring
    │
    └── # Bundled test subject applications:
        ├── train-ticket/                        # 40+ microservices
        ├── ftgo-application/                    # FTGO food delivery
        ├── spring-petclinic-microservices/       # PetClinic microservices
        ├── flowing-retail/                      # Event-driven retail
        ├── Axon-trader/                         # CQRS trading platform
        └── eventuate-tram-examples-customers-and-orders/
```

---

## 📄 SARIF Report Format

Phase 1 outputs SARIF 2.1.0 with two rule definitions:

```json
{
  "ruleId": "RACE-WW-001",
  "level": "error",
  "message": { "text": "Potential CRITICAL race on entity [Order]..." },
  "locations": [{ "physicalLocation": { "artifactLocation": { "uri": "/path/to/file.java" }, "region": { "startLine": 42 } } }],
  "relatedLocations": [{ "id": 1, "message": { "text": "Second conflicting endpoint" }, "physicalLocation": { ... } }],
  "properties": { "entity": "Order", "raceType": "WRITE_WRITE", "protectionStatus": "UNPROTECTED" }
}
```

Phase 2 enriches the SARIF with verification verdicts:

```json
{
  "ruleId": "VERIFIED-RACE",
  "level": "error",
  "properties": {
    "verdict": "TRUE_POSITIVE",
    "confidence": 0.85,
    "static_score": 1.0,
    "llm_agreement": 1.0,
    "race_pattern": "Check-Then-Act",
    "mitigation": "Use distributed lock or @Transactional(isolation=SERIALIZABLE)"
  }
}
```

---

## 🧪 Bundled Test Applications

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
