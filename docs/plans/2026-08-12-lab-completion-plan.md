# Lab Completion Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Implement the evaluation core, build the golden dataset, run benchmarks, and complete the analysis exercises for the Day 14 AI Evaluation Lab.

**Architecture:** We will implement the classes in `template.py` (Data Models, RAGASEvaluator, LLMJudge, BenchmarkRunner, FailureAnalyzer) step by step, ensuring tests pass. Then we will complete `golden_dataset.json` and the markdown files (`exercises.md`, `reflection.md`).

**Tech Stack:** Python, Pytest, JSON, Markdown

---

### Task 1: Complete Warm-up Exercises

**Files:**
- Modify: `exercises.md`

**Step 1: Write answers for Part 1 (Exercises 1.1 to 1.3)**
- Add thresholds for RAGAS metrics.
- Add answers for bias mitigation and CI/CD rules.

**Step 2: Commit**
```bash
git add exercises.md
git commit -m "docs: complete warm-up exercises"
```

---

### Task 2: Implement Data Models (Task 1)

**Files:**
- Modify: `template.py`

**Step 1: Implement QAPair, EvalResult, and overall_score()**
- Define fields for `QAPair`.
- Define fields for `EvalResult`.
- Implement `overall_score` as average of faithfulness, relevance, completeness.

**Step 2: Verify tests for Data Models pass**
Run: `uv run pytest tests/ -v -k "TestEvalResultOverallScore"`
Expected: PASS

**Step 3: Commit**
```bash
git add template.py
git commit -m "feat: implement QAPair and EvalResult data models"
```

---

### Task 3: Implement RAGASEvaluator (Task 2)

**Files:**
- Modify: `template.py`

**Step 1: Implement Answer-side and Retrieval-side metrics**
- Implement `evaluate_faithfulness`, `evaluate_relevance`, `evaluate_completeness`.
- Implement `evaluate_context_recall`, `evaluate_context_precision`.
- Implement `run_full_eval`.

**Step 2: Verify tests for RAGASEvaluator pass**
Run: `uv run pytest tests/ -v -k "TestRAGASEvaluator or TestContextMetrics or TestRetrievalMetricWiring"`
Expected: PASS

**Step 3: Commit**
```bash
git add template.py
git commit -m "feat: implement RAGAS evaluator metrics"
```

---

### Task 4: Implement LLMJudge and BenchmarkRunner (Tasks 3 & 4)

**Files:**
- Modify: `template.py`

**Step 1: Implement LLMJudge and BenchmarkRunner methods**
- Implement `LLMJudge.score_response` and `detect_bias`.
- Implement `BenchmarkRunner.run`, `generate_report`, `run_regression`, `identify_failures`.

**Step 2: Verify tests pass**
Run: `uv run pytest tests/ -v -k "TestLLMJudge or TestBenchmarkRunner or TestRunRegression"`
Expected: PASS

**Step 3: Commit**
```bash
git add template.py
git commit -m "feat: implement LLMJudge and BenchmarkRunner"
```

---

### Task 5: Implement FailureAnalyzer (Task 5)

**Files:**
- Modify: `template.py`

**Step 1: Implement FailureAnalyzer methods**
- Implement `categorize_failures`, `find_root_cause`, `generate_improvement_suggestions`, `generate_improvement_log`.

**Step 2: Verify tests pass**
Run: `uv run pytest tests/ -v -k "TestFailureAnalyzer or TestGenerateImprovementLog"`
Expected: PASS

**Step 3: Verify all tests pass**
Run: `uv run pytest tests/ -v`
Expected: 42 passed

**Step 4: Commit**
```bash
git add template.py
git commit -m "feat: implement FailureAnalyzer and pass all tests"
```

---

### Task 6: Build Golden Dataset and Run RAG (Task 6)

**Files:**
- Modify: `golden_dataset.json`
- Test: `validate_golden_dataset.py`

**Step 1: Create Golden Dataset**
- Fill in 20 QA pairs (5 Easy, 7 Medium, 5 Hard, 3 Adversarial).

**Step 2: Validate Dataset**
Run: `python validate_golden_dataset.py`
Expected: PASS

**Step 3: Run Benchmark**
Run: 
```bash
python domain_assistant.py
python evaluate_answers.py
```
Expected: artifacts/actual_answers.json and artifacts/benchmark_results.json created.

**Step 4: Commit**
```bash
git add golden_dataset.json artifacts/
git commit -m "data: create golden dataset and run benchmark"
```

---

### Task 7: Complete Lab Exercises and Reflection (Task 6 cont.)

**Files:**
- Modify: `exercises.md`, `reflection.md`, `solution/solution.py`

**Step 1: Fill markdown files**
- Complete Exercise 3.1, 3.2, 3.3 in `exercises.md`.
- Fill `reflection.md` with 3 worst-performing cases.
- Copy `template.py` to `solution/solution.py`.

**Step 2: Commit**
```bash
cp template.py solution/solution.py
git add exercises.md reflection.md solution/solution.py
git commit -m "docs: complete exercises and reflection"
```
