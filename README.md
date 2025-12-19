# Timeline Engine Specification – Temporal Logic Framework (Task 4)

## 1. Objective

The Timeline Engine provides **time‑reasoning** over the ZCPP regulatory document.
It answers questions like:

- “Is Rule X active on date Y?”  
- “When does obligation Z become required?”  
- “What is the deadline for action A if event B occurred on date C?”

It is designed to handle:

- Absolute dates (e.g., “May 15, 2096”).  
- Relative offsets (“45 days after Presidential Certification”, “within 30 days of quarter end”). 
- Conditional dates (“upon Presidential Certification”).
- Recurring events (annual renewal, quarterly filings).  
- Grace periods and retention windows (30 days, 6 months, 10 years).  
- The hidden trap: Topic 22’s effective date depends on Topic 12, which depends on certification that has not occurred.

The core implementation lives in `timeline_engine.py` as the `TimelineEngine` class.

---

## 2. Data Model

The engine models rules and events as nodes with dependencies and offsets:


Key ideas:

- **CERT** represents Presidential Certification, whose date may be unknown (`None`).
- Each rule has:
  - `depends_on`: another node (e.g., `CERT` or `"12"`).  
  - `offset_days`: number of days after its dependency becomes effective.  
- This structure forms a small dependency graph:  
  `CERT → 12 → 22` and `CERT → PROTO`.

---

## 3. Core Methods

### 3.1 set_certification_date


- Allows scenarios where certification has not occurred (`None`) or occurred on a concrete date (e.g., `"2096-08-01"`).

### 3.2 effective_date(key)



- Allows scenarios where certification has not occurred (`None`) or occurred on a concrete date (e.g., `"2096-08-01"`).

### 3.2 effective_date(key)


- Resolves effective dates by **recursively walking dependencies** and adding offsets.  
- If any dependency’s date is `None`, the result is `None` (pending).

### 3.3 is_active_on(key, date_str)


Answers: “Is Rule X active on date Y?” with an explicit reason.

### 3.4 deadline_from_event


Used for questions like:  
“What’s the deadline for Form ZC‑Q if the quarter ends on 2096‑09‑30?” → `2096‑10‑30`.

---

## 4. Hidden Trap Handling (Topic 22)

Document logic:

- Topic 12: effective “upon Presidential Certification.”  
- Topic 22: effective “45 days after Topic 12 takes effect.”  
- Certification has not occurred yet in the current scenario.

Engine behavior:


Thus:

- Topic 22’s effective date is **not computable**; it is **pending indefinitely**.  
- Any “Is Topic 22 active on date Y?” query returns `active = False` with a dependency‑chain explanation.

This directly satisfies the hidden trap requirement.

---

## 5. Example Temporal Queries

The engine is consistent with `temporal_queries.json`, for example:

- Protocol active on 2096‑07‑01 with no certification → inactive, pending.  
- Topic 12 effective date if certification is 2096‑10‑10 → 2096‑10‑10.  
- Topic 22 effective date if certification is 2096‑10‑10 → 2096‑11‑24 (45 days after Topic 12).  
- ZC‑Q deadline if quarter ends 2096‑09‑30 → 2096‑10‑30 (30‑day grace).

---

## 6. Integration with Agentic Pipeline

The engine is embedded into an agentic pipeline via tools:

- Tool `extract_temporal_expressions` builds `temporal_expressions.csv` from `input.txt` (regex‑based temporal NER).
- Tool `temporal_status_engine` wraps `TimelineEngine` methods to answer natural‑language temporal questions (Topic 22 trap, deadlines, activation checks).  
- A LangChain agent orchestrates these tools, providing an AI interface over deterministic temporal logic.

The engine therefore acts as the **source of truth** for all time computations, while the agent layer handles orchestration and explanation.
