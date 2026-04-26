# LLM Race Filter — GitHub Models Backend

Filters false positives from your static race detector's SARIF output.
Uses **GitHub Models API** — free, no install, no Ollama, no token expiry.

## Why GitHub Models?

| Requirement | GitHub Models |
|-------------|--------------|
| Free | ✅ Yes (150 req/day, no card) |
| No local install | ✅ Cloud API |
| No token expiry | ✅ PAT never expires unless you revoke |
| OpenAI-compatible | ✅ Drop-in |
| Lightweight model | ✅ Llama-3.1-8B, Phi-4, Phi-3-mini |
| Works on 604 races | ✅ ~30-50 API calls total |

---

## Setup (2 minutes)

### 1. Get a GitHub PAT

Go to: https://github.com/settings/tokens  
Click **"Generate new token (classic)"**  
Select scope: ✅ `models:read`  
Copy the token (starts with `ghp_`)

### 2. Set the token

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

Or pass it directly: `python filter_races.py ... --token ghp_xxx`

### 3. No pip install needed — pure Python stdlib

---

## Usage

```bash
# Validate parser first (no API calls)
python test_parser.py race-report.sarif

# Analyse all 604 races (~50 API calls, ~4 min)
python filter_races.py race-report.sarif

# Only CRITICAL races (163 races, ~20 API calls, ~2 min)
python filter_races.py race-report.sarif --severity CRITICAL

# Quick test — first 24 races only (2 API calls)
python filter_races.py race-report.sarif --top-n 24

# With source code for richer justifications
python filter_races.py race-report.sarif \
  --source-root ./examples/train-ticket

# Use a different model
python filter_races.py race-report.sarif \
  --model Phi-4

# Custom output paths
python filter_races.py race-report.sarif \
  --output results/filtered.json \
  --report results/report.md
```

---

## Available Models (all free low-tier, 150 req/day)

| Model | Speed | Quality | Best for |
|-------|-------|---------|----------|
| `Meta-Llama-3.1-8B-Instruct` | ⚡⚡⚡ | Good | Default, fastest |
| `Phi-4` | ⚡⚡ | Better | More nuanced reasoning |
| `Phi-3-mini-4k-instruct` | ⚡⚡⚡ | OK | Smallest, most conservative |
| `Phi-3.5-mini-instruct` | ⚡⚡⚡ | Good | Balanced |

---

## Token Budget Per API Call

```
System prompt  :  ~120 tokens
User (12 races):  ~480 tokens  (40 tokens × 12)
Response       :  ~360 tokens  (30 tokens × 12)
Total per call :  ~960 tokens  ← well under limits
```

With 604 races batched into groups of 12:
- **~50 API calls total** (well under 150/day limit)
- Each call uses ~1000 tokens, no risk of per-call token limits

---

## Output Files

### `filtered-races.json`
```json
[
  {
    "verdict": "REAL",
    "confidence": "HIGH",
    "risk_score": 9,
    "justification": "createNewOrder and payOrder both write Order.status without any lock, enabling lost updates.",
    "severity": "CRITICAL",
    "entity": "Order",
    "race_type": "WRITE_WRITE",
    "endpoint1": "POST /api/v1/orderservice/order (OrderController.createNewOrder)",
    "endpoint2": "GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)",
    "file": "./examples/train-ticket/ts-order-service/.../OrderController.java",
    "line": 50
  }
]
```

### `race-analysis-report.md`
- Summary table (REAL / FP / Uncertain)
- All real races sorted by risk score (highest first)
- LLM justification per race
- False positives with reasons
- Fix recommendations table

---

## How False Positive Detection Works

The model applies these rules (hardcoded in system prompt):

| Pattern | Verdict |
|---------|---------|
| Two WRITEs on same entity, no lock | REAL |
| createNewOrder + payOrder on Order | REAL (high risk) |
| GET read-only endpoint vs GET read-only | FALSE_POSITIVE |
| Endpoints partitioned by userId/orderId | FALSE_POSITIVE |
| Admin config endpoints (rare concurrency) | UNCERTAIN |
| TOCTOU: read-check before write | REAL |

---

## Rate Limits

GitHub free tier (no Copilot): **150 requests/day** for low-tier models.

If you hit 429, the client automatically waits and retries.  
To stay safe, use `--severity CRITICAL` to reduce calls by ~60%.

## Files

```
llm-race-filter/
├── filter_races.py    ← main entry point
├── github_client.py   ← API client, batching, rate limiting
├── sarif_parser.py    ← parse SARIF, group by entity
├── report_writer.py   ← write JSON + Markdown reports
└── test_parser.py     ← validate SARIF parsing (no API calls)
```
