# Design Doc: Lab Completion Plan (AI Evaluation & Benchmarking)

## Overview
This document outlines the step-by-step roadmap to complete the Day 14 AI Evaluation & Benchmarking lab. The lab consists of implementing an evaluation engine, building a golden dataset, running the benchmark, and writing a failure analysis reflection.

## Chosen Approach
We will use a **Sequential Approach**, closely mirroring the lab's instructions, to ensure no deliverables are missed and dependencies between tasks are respected.

## Roadmap

### Part 1: Warm-up (Theory & Concepts)
- **Objective:** Answer theoretical questions in `exercises.md`.
- **Tasks:**
  - Define metric thresholds (Acceptable vs. Critical).
  - Design experiments and rubric rules to mitigate LLM-as-a-Judge biases (position, verbosity, self-preference).
  - Outline CI/CD integration rules (when to block deployment).

### Part 2: Core Coding (template.py)
- **Objective:** Implement the evaluation core to pass all 42 tests.
- **Tasks:**
  - **Task 1 (Data Models):** Define `QAPair`, `EvalResult`, and implement `overall_score()`.
  - **Task 2 (RAGASEvaluator):** Implement answer-side metrics (`faithfulness`, `relevance`, `completeness`) and retrieval-side metrics (`context_recall`, `context_precision`). Implement `run_full_eval()`.
  - **Task 3 (LLMJudge):** Implement `score_response()` parsing and `detect_bias()`.
  - **Task 4 (BenchmarkRunner):** Implement `run()`, `generate_report()`, `run_regression()`, and `identify_failures()`.
  - **Task 5 (FailureAnalyzer):** Implement `categorize_failures()`, `find_root_cause()`, `generate_improvement_suggestions()`, and `generate_improvement_log()`.

### Part 3: Golden Dataset & Benchmark
- **Objective:** Build a 20-question stratified dataset and run the evaluation pipeline.
- **Tasks:**
  - Populate `golden_dataset.json` with 5 Easy, 7 Medium, 5 Hard, and 3 Adversarial questions based on `data/technology_store/*.md`.
  - Validate the dataset using `validate_golden_dataset.py`.
  - Run the RAG system to generate `actual_answers.json`.
  - Fill the aggregate report and LLM Rubric in `exercises.md`.

### Part 4: Reflection & Submission
- **Objective:** Analyze failures and prepare the final submission.
- **Tasks:**
  - Analyze the 3 worst-performing cases.
  - Complete the 5 Whys analysis and improvement log in `reflection.md`.
  - Copy `template.py` to `solution/solution.py`.

## Validation
- The primary indicator of success for Part 2 is `uv run pytest tests/ -v` passing all 42 tests.
- For Part 3, `python validate_golden_dataset.py` must pass.
