# Day 14 — Exercises

## AI Evaluation & Benchmarking · Lab Worksheet

**Thời gian làm bài:** 14:15–17:00

**Domain:** OrbitTech Store Customer Support

Điền trực tiếp câu trả lời vào file này. Golden dataset 20 QA được viết một lần
duy nhất trong `golden_dataset.json`, không chép lại toàn bộ vào Markdown.

---

Từ 14:15–14:30, cài môi trường và chạy baseline tests theo `guide_lab.md`.

---

## Part 1 — Warm-up (14:30–14:45)

### Exercise 1.1 — RAGAS Metric Thresholds

Theo bài giảng:

- 0.8–1.0: Good — monitor, maintain.
- 0.6–0.8: Needs work — analyze failures, iterate.
- Dưới 0.6: Significant issues — investigate.

Với từng metric, xác định khi nào score thấp có thể chấp nhận và khi nào là
critical.

| Metric | Acceptable Low Score Scenario | Critical Low Score Scenario | Action Required |
|---|---|---|---|
| Faithfulness | Context thiếu chi tiết nhỏ, nhưng LLM vẫn suy luận đúng facts | Hallucination, bịa đặt thông tin sai lệch hoàn toàn so với context | Cần investigate ngay lập tức (cải thiện prompt grounding) |
| Answer Relevance | Câu trả lời kèm theo giao tiếp lịch sự (chào hỏi) làm giảm overlap | Câu trả lời hoàn toàn lạc đề (off-topic) hoặc không hiểu ý người dùng | Cải thiện intent routing hoặc kiểm tra lại retriever |
| Context Recall | Câu hỏi về kiến thức chung không thực sự cần proprietary context | Thiếu thông tin cốt lõi (vd: policy mới nhất) để trả lời đúng | Cải thiện retriever (tăng top_k, sửa chunking) |
| Context Precision | Chunk đúng nằm ở vị trí 2-3 thay vì top 1, nhưng vẫn trong context window | Chunk đúng nằm quá xa (vd: rank 20), bị context window cắt mất | Thêm reranker hoặc fine-tune embedding model |
| Completeness | Trả lời ngắn gọn, đúng trọng tâm nhưng thiếu vài chi tiết phụ | Bỏ sót các bước quan trọng trong hướng dẫn (incomplete) | Tăng generation max tokens hoặc sửa prompt để trả lời chi tiết hơn |

### Exercise 1.2 — Bias trong LLM-as-a-Judge

Ba bias thường gặp:

- Position bias: judge ưu tiên answer xuất hiện trước.
- Verbosity bias: judge ưu tiên answer dài hơn.
- Self-preference: judge ưu tiên output giống chính model đó.

**Câu 1: Thiết kế experiment phát hiện position bias với ít nhất hai conditions.**

> *Câu trả lời:* Đưa 2 câu trả lời A và B cho LLM Judge chấm. Ở condition 1, đặt A trước B. Ở condition 2, đảo ngược vị trí đặt B trước A. Nếu Judge luôn chọn câu xuất hiện đầu tiên bất kể nội dung, chứng tỏ có position bias.

**Câu 2: Làm thế nào giảm verbosity bias bằng rubric design?**

> *Câu trả lời:* Trong rubric, cần thêm tiêu chí "Conciseness" (Ngắn gọn, súc tích) và ghi rõ điểm trừ nếu câu trả lời lan man, dài dòng không cần thiết.

**Câu 3: Tại sao cần calibrate LLM judge với human labels?**

> *Câu trả lời:* Vì LLM có thể có những bias riêng (như self-preference) hoặc không hiểu đúng sắc thái domain cụ thể. Calibrate với human labels giúp đảm bảo tiêu chuẩn của LLM đồng nhất với định hướng kinh doanh và góc nhìn của con người.

### Exercise 1.3 — Evaluation trong CI/CD

**Câu 1: Chọn threshold để block deployment.**

| Metric | Threshold | Lý do |
|---|---:|---|
| Faithfulness | 0.8 | Rất quan trọng để tránh hallucination, đảm bảo độ tin cậy của agent |
| Answer Relevance | 0.7 | Cho phép linh hoạt một chút với cách user đặt câu hỏi hoặc agent chào hỏi |
| Completeness | 0.7 | Trả lời thiếu một chút vẫn tốt hơn là trả lời sai, nhưng không được quá thấp |

**Câu 2: Khi nào dùng offline evaluation, online evaluation và human review?**

> *Câu trả lời:* 
> - **Offline evaluation**: Dùng trong quá trình phát triển (CI/CD) để test trước khi deploy, đánh giá prompt/model mới trên golden dataset.
> - **Online evaluation**: Dùng khi hệ thống đã live, chạy trên real traffic để monitor chất lượng liên tục, detect data drift hoặc edge cases.
> - **Human review**: Dùng để tạo golden dataset, calibrate LLM judge, hoặc xử lý các edge cases/high-stakes cases (như liên quan y tế, tài chính).

---

## Part 2 — Core Coding (14:45–15:40)

Hoàn thiện các TODO bắt buộc trong `template.py`.

### Task 1 — Data Models

- `QAPair`: question, expected answer, gold context, metadata và retrieved contexts.
- `EvalResult`: answer-side scores, optional retrieval scores, pass/failure fields.
- `overall_score()`: trung bình Faithfulness, Relevance và Completeness.

### Task 2 — RAGASEvaluator

Answer-side:

- `evaluate_faithfulness(answer, context)`
- `evaluate_relevance(answer, question)`
- `evaluate_completeness(answer, expected)`

Retrieval-side:

- `evaluate_context_recall(contexts, expected)`
- `evaluate_context_precision(contexts, expected)`

Full pipeline:

- `run_full_eval(..., contexts=None)` luôn tính ba answer metrics.
- Nếu có `contexts`, tính và lưu thêm Context Recall và Context Precision.
- Retrieval scores không làm thay đổi `overall_score()` và pass rule gốc.

### Task 3 — LLMJudge

- `score_response(question, answer, rubric)`
- `detect_bias(scores_batch)`

### Task 4 — BenchmarkRunner

- `run(qa_pairs, agent_fn, evaluator)`
- `generate_report(results)`
- `run_regression(new_results, baseline_results)`
- `identify_failures(results, threshold)`

`BenchmarkRunner.run()` phải truyền `pair.retrieved_contexts` vào
`run_full_eval()`. Report phải có average của hai retrieval metrics.

### Task 5 — FailureAnalyzer

- `categorize_failures(failures)`
- `find_root_cause(failure)`
- `generate_improvement_suggestions(failures)`
- `generate_improvement_log(failures, suggestions)`

Kiểm tra:

```bash
pytest tests/ -v
```

`rerank_by_overlap()` là TODO bonus của Exercise 3.5. Test tương ứng được skip
nếu bạn chưa làm bonus.

---

## Part 3 — Golden Dataset & Real Benchmark (15:40–16:35)

### Exercise 3.1 — Build the Golden Dataset

Thiết kế và validate dataset theo Mục 5–6 trong `guide_lab.md`. Nội dung 20 QA
được điền trực tiếp trong `golden_dataset.json`; phần dưới chỉ ghi lại kết quả
và quyết định thiết kế, không chép lại toàn bộ QA.

**Kết quả dataset**

| Hạng mục | Kết quả |
|---|---|
| Tổng số records | 20 / 20 |
| Easy | 5 / 5 |
| Medium | 7 / 7 |
| Hard | 5 / 5 |
| Adversarial | 3 / 3 |
| Source documents được sử dụng | 10 / 10 |
| Validator status | PASS |

**Ba case đại diện cho quyết định thiết kế**

| ID | Difficulty | Source document(s) | Vì sao case phù hợp với difficulty/attack type? |
|---|---|---|---|
| E01 | Easy | 01_product_catalog.md | Trực tiếp hỏi thông tin cơ bản về một sản phẩm duy nhất. |
| M01 | Medium | 06_warranty_policy.md, 01_product_catalog.md | Đòi hỏi tổng hợp thông tin thời gian bảo hành từ 2 nguồn tài liệu khác nhau. |
| A01 | Adversarial | 00_system_scope.md | Đặt câu hỏi lạc đề (thời tiết) để kiểm tra khả năng bám sát Scope của hệ thống. |

**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> *Câu trả lời:* Đảm bảo 'expected answer' chỉ bao gồm thông tin chính xác từ văn bản gốc, tránh việc đưa quá nhiều thông tin dư thừa khiến LLM-as-a-Judge đánh giá sai lệch tiêu chí Completeness và Precision.

**Xác nhận:**

- [x] Mọi claim trong expected answer đều có evidence hỗ trợ.
- [x] Không có questions trùng ý và không dùng kiến thức ngoài corpus.
- [x] `python validate_golden_dataset.py` báo `PASS`.

### Exercise 3.2 — Benchmark Run

Chạy:

```bash
python domain_assistant.py
python evaluate_answers.py
```

Copy bảng terminal vào đây hoặc điền từ `artifacts/benchmark_results.json`.

| ID | Question (short) | Ctx Recall | Ctx Precision | Faithfulness | Relevance | Completeness | Overall | Passed? | Failure Type |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| E01 | | | | | | | | | |
| E02 | | | | | | | | | |
| E03 | | | | | | | | | |
| E04 | | | | | | | | | |
| E05 | | | | | | | | | |
| M01 | | | | | | | | | |
| M02 | | | | | | | | | |
| M03 | | | | | | | | | |
| M04 | | | | | | | | | |
| M05 | | | | | | | | | |
| M06 | | | | | | | | | |
| M07 | | | | | | | | | |
| H01 | | | | | | | | | |
| H02 | | | | | | | | | |
| H03 | | | | | | | | | |
| H04 | | | | | | | | | |
| H05 | | | | | | | | | |
| A01 | | | | | | | | | |
| A02 | | | | | | | | | |
| A03 | | | | | | | | | |

**Aggregate Report**

- Overall pass rate: 5.0%
- Avg Context Recall: 0.493
- Avg Context Precision: 0.937
- Avg Faithfulness: 0.397
- Avg Relevance: 0.426
- Avg Completeness: 0.293
- Failure type distribution: {'irrelevant': 3, 'incomplete': 2, 'off_topic': 3, 'hallucination': 11}

**Ba cases có Overall Score thấp nhất**

1. ID: M03 | Score: 0.000 | Failure type: hallucination
2. ID: A03 | Score: 0.000 | Failure type: hallucination
3. ID: M06 | Score: 0.118 | Failure type: hallucination

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> *Câu trả lời:* Metric yếu nhất là Completeness (0.293) và Faithfulness (0.397). Kết quả gợi ý vấn đề nằm ở CẢ HAI. Retrieval lấy sót ngữ cảnh (Recall 0.493), kéo theo Generation bịa đặt thông tin vì thiếu dữ kiện thật.

### Exercise 3.3 — LLM-as-a-Judge Rubric Design

Thiết kế rubric domain-specific cho OrbitTech Customer Support. Mỗi mức phải
đủ cụ thể để hai người chấm độc lập có thể hiểu giống nhau.

Chọn 3–5 dimensions:

- [x] Correctness
- [x] Completeness
- [x] Relevance
- [x] Evidence/citation
- [x] Actionability
- [x] Safety/privacy
- [x] Tone/clarity
- [x] Dimension khác: __________

| Score | Tiêu chí domain-specific | Ví dụ response |
|---:|---|---|
| 5 | | |
| 4 | | |
| 3 | | |
| 2 | | |
| 1 | | |

**Ba edge cases khó chấm**

| Edge Case | Tại sao khó chấm? | Rubric xử lý thế nào? |
|---|---|---|
| | | |
| | | |
| | | |

**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> *Câu trả lời:* Giảm position bias bằng cách xáo trộn ngẫu nhiên thứ tự các chunks khi đưa vào context. Giảm verbosity bias bằng cách thiết kế rubric có điểm trừ nếu dài dòng. Giảm self-preference bằng cách sử dụng nhiều model (OpenAI vs Mistral) để chấm điểm chéo.

### Exercise 3.4 — Framework Comparison (Bonus +10)

Chỉ làm sau khi hoàn thành 3.1–3.3. Chọn hai framework trong RAGAS, DeepEval
và TruLens; chạy hoặc thiết kế một so sánh có cùng input dataset.

| Tiêu chí | Framework 1: ____ | Framework 2: ____ |
|---|---|---|
| Setup complexity | | |
| Metrics available | | |
| CI/CD integration | | |
| Kết quả trên cùng dataset | | |
| Insight rút ra | | |

- Scores có nhất quán không?
- Framework nào strict hơn và vì sao?
- Hai framework có tìm ra cùng failure cases không?

> *Phân tích:*

### Exercise 3.5 — Retrieval Reranking (Bonus +5)

Mục tiêu: kiểm tra việc đổi thứ tự chunks có tăng Context Precision mà không
thay đổi Context Recall hay không.

1. Chọn ít nhất 5 cases từ `artifacts/actual_answers.json`.
2. Tính Context Recall và Context Precision trước rerank.
3. Implement `rerank_by_overlap()` hoặc một reranker khác.
4. Rerank cùng tập chunks, không thêm hoặc xóa chunk.
5. Tính lại hai metrics và giải thích kết quả.

| ID | Recall before | Recall after | Precision before | Precision after | Delta Precision |
|---|---:|---:|---:|---:|---:|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| **Avg** | | | | | |

**Tại sao Recall dự kiến không đổi?**

> *Câu trả lời:* Vì Reranking chỉ đảo thứ tự các chunk đã được retrieve chứ không tìm thêm chunk mới nào, nên số lượng chunk có ích (Recall) được giữ nguyên, chỉ thay đổi thứ hạng (Precision).

**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> *Câu trả lời:* Khi Context Recall quá thấp. Nếu Retrieval ban đầu không tìm ra được chunk có chứa đáp án, thì Reranker dù giỏi đến mấy cũng vô dụng vì không có nguyên liệu đúng để sắp xếp.

---

## Part 4 — Reflection (16:35–16:50)

Hoàn thành `reflection.md` bằng kết quả thật từ Exercise 3.2.

---

## Completion Checklist

Hoàn thành kiểm tra cuối trong khoảng 16:50–17:00.

- [x] Tất cả required tests pass.
 - [x] `golden_dataset.json` validate thành công.
 - [x] Exercise 3.1 hoàn thành trong file JSON và bảng kết quả phía trên.
 - [x] Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.
 - [x] Exercise 3.3 có rubric 1–5 và bias controls.
 - [x] `reflection.md` có ba failure analyses và regression strategy.
 - [x] Đã copy `template.py` thành `solution/solution.py`.
 - [x] Exercise 3.4 và 3.5 chỉ làm nếu chọn bonus.
