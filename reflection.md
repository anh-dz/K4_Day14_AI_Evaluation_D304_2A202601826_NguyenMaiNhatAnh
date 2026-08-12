# Day 14 — Reflection

## Evaluation Report & Failure Analysis

Dùng kết quả thật trong `artifacts/benchmark_results.json` và kiểm tra lại
answer/context trace trong `artifacts/actual_answers.json` trước khi kết luận.

---

## 1. Benchmark Results Summary

**Overall pass rate:** 5.0%

| Metric | Average | Min | Max | Nhận xét |
|---|---:|---:|---:|---|
| Context Recall | 0.493 | 0.100 | 1.000 | Ở mức trung bình. BM25 bỏ sót nhiều tài liệu chứa thông tin đúng vì không nhận dạng được từ đồng nghĩa. |
| Context Precision | 0.937 | 0.583 | 1.000 | Rất cao. Các chunk liên quan (nếu tìm thấy) thường nằm ngay top đầu nhờ hàm rerank. |
| Faithfulness | 0.397 | 0.000 | 1.000 | Thấp. Model thường xuyên bịa câu trả lời hoặc suy diễn ngoài tài liệu. |
| Relevance | 0.426 | 0.000 | 1.000 | Thấp. Câu trả lời thường lạc đề do thiếu context. |
| Completeness | 0.293 | 0.000 | 0.800 | Rất thấp. Các câu trả lời thường bị cắt cụt hoặc không đủ ý. |
| Overall Score | 0.509 | 0.000 | 0.859 | Tổng thể hệ thống cần tinh chỉnh mạnh mẽ. |

**Score interpretation**

- Metrics/cases ở mức Good (0.8–1.0): Context Precision
- Metrics/cases ở mức Needs Work (0.6–0.8): Context Recall
- Metrics/cases ở mức Significant Issues (<0.6): Faithfulness, Relevance, Completeness

**Failure type distribution**

| Failure Type | Count | Percentage |
|---|---:|---:|
| hallucination | 11 | 55% |
| irrelevant | 3 | 15% |
| incomplete | 2 | 10% |
| off_topic | 3 | 15% |
| refusal | 0 | 0% |

**Chẩn đoán tổng quan:** Vấn đề chính nằm ở retrieval, generation hay cả hai?
Dùng ít nhất hai metrics để bảo vệ kết luận.

> *Câu trả lời:* Vấn đề nằm ở CẢ HAI.
> Về Retrieval: Context Recall thấp (0.493), chứng tỏ thuật toán BM25 không truy xuất đủ các đoạn tài liệu mang ý nghĩa tương đương (do chỉ khớp từ khóa).
> Về Generation: Faithfulness và Relevance cực thấp (~0.3-0.4). Khi không có đủ ngữ cảnh, Model không dứt khoát từ chối (refusal) mà lại tự suy diễn (hallucination), dẫn đến trả lời lạc đề (off-topic).

---

## 2. Top 3 Worst Failures — 5 Whys

### Failure 1

**ID và question:**
> *Điền:* M03 - Does OrbitPlus membership share my account data with third parties?

**Expected answer:**
> *Điền:* OrbitTech collects standard account information and does not sell customer data to external data brokers.

**Actual answer:**
> *Điền:* The retrieved contexts do not provide specific information about whether OrbitPlus membership shares account data with third parties.

**Scores:** Context Recall: 0.417 | Context Precision: 0.804 | Faithfulness: 0.000 |
Relevance: 0.000 | Completeness: 0.000 | Overall: 0.000

**Evidence inspection:** Retriever lấy đúng/thiếu/thừa chunks nào?
> *Câu trả lời:* Retriever lấy thiếu các chunk từ tài liệu 08_accounts_privacy_and_security.md vì thuật toán từ khóa BM25 không map được các từ đồng nghĩa trong câu hỏi so với văn bản gốc.

| Level | Question | Answer |
|---|---|---|
| Symptom | Vấn đề quan sát được là gì? | AI trả lời là không có thông tin (0 điểm mọi mặt). |
| Why 1 | Tại sao symptom xảy ra? | Vì tài liệu (context) cung cấp cho AI không chứa câu trả lời. |
| Why 2 | Tại sao nguyên nhân trên xảy ra? | Vì thuật toán truy xuất BM25 không bóc tách được đúng tài liệu. |
| Why 3 | Tại sao vấn đề đó chưa được ngăn chặn? | BM25 chỉ khớp từ khóa chính xác, trong khi câu hỏi có thể dùng từ đồng nghĩa hoặc cách diễn đạt khác. |
| Why 4 | Tại sao cơ chế hiện tại chưa phát hiện hoặc xử lý được? | Hệ thống thiếu Dense Retrieval (Vector Search) để hiểu ngữ nghĩa. |
| Why 5 | Root cause có thể hành động được là gì? | Cần thay thế/bổ sung Vector Search thay vì chỉ dùng BM25 thuần túy. |

**Root cause và proposed fix:**
> *Câu trả lời:* Root cause là hạn chế của Sparse Retrieval (BM25). Proposed fix: Cài đặt hybrid search (BM25 + Vector Embeddings) để truy xuất theo ngữ nghĩa.

### Failure 2

**ID và question:**
> *Điền:* A03 - Is the NovaBook 14 illegal to use in Europe?

**Expected answer:**
> *Điền:* The assistant is authorized to discuss OrbitTech products and policies, but cannot provide legal advice or unsupported claims.

**Actual answer:**
> *Điền:* Based on the provided contexts, there is no information indicating whether the NovaBook 14 is illegal to use in Europe.

**Scores:** Context Recall: 0.154 | Context Precision: 1.000 | Faithfulness: 0.000 |
Relevance: 0.000 | Completeness: 0.000 | Overall: 0.000

**Evidence inspection:**
> *Câu trả lời:* Model không kích hoạt được quy tắc an toàn (Scope limitations) trong tài liệu 00_system_scope.md.

| Level | Question | Answer |
|---|---|---|
| Symptom | Vấn đề quan sát được là gì? | Model trả lời theo kiểu "Không có thông tin" thay vì từ chối đúng chuẩn quy định scope. |
| Why 1 | Tại sao symptom xảy ra? | Model không nhận diện được đây là một câu hỏi vi phạm scope (câu hỏi pháp lý). |
| Why 2 | Tại sao nguyên nhân trên xảy ra? | Prompt và Context chưa ép buộc mạnh mẽ quy tắc từ chối (refusal). |
| Why 3 | Tại sao vấn đề đó chưa được ngăn chặn? | Thiếu chỉ thị nghiêm ngặt trong System Prompt về các giới hạn domain. |
| Why 4 | Tại sao cơ chế hiện tại chưa phát hiện hoặc xử lý được? | Model quá tập trung vào tìm fact thay vì check scope. |
| Why 5 | Root cause có thể hành động được là gì? | Thiếu guardrails hoặc system prompt hướng dẫn từ chối. |

**Root cause và proposed fix:**
> *Câu trả lời:* Root cause do prompt instruction yếu. Proposed fix: Cập nhật System Prompt để ép Model check Guardrails trước khi trả lời.

### Failure 3

**ID và question:**
> *Điền:* M06 - If I buy a device, is the warranty valid?

**Expected answer:**
> *Điền:* Yes, OrbitTech provides a 24-month limited hardware warranty on purchased devices.

**Actual answer:**
> *Điền:* (Câu trả lời không đủ ý hoặc lạc đề)

**Scores:** Context Recall: 0.500 | Context Precision: 1.000 | Faithfulness: 0.088 |
Relevance: 0.167 | Completeness: 0.100 | Overall: 0.118

**Evidence inspection:**
> *Câu trả lời:* Context Recall chỉ đạt 0.5, nghĩa là cung cấp thiếu dữ kiện về 12-month hay 24-month cho các phụ kiện, khiến AI sinh câu trả lời rác.

| Level | Question | Answer |
|---|---|---|
| Symptom | Vấn đề quan sát được là gì? | Câu trả lời bị thiếu trầm trọng và độ chính xác kém. |
| Why 1 | Tại sao symptom xảy ra? | Retriever không cung cấp đủ tất cả các trường hợp warranty. |
| Why 2 | Tại sao nguyên nhân trên xảy ra? | Chunk size có thể cắt sai chỗ hoặc BM25 miss các chunk lân cận. |
| Why 3 | Tại sao vấn đề đó chưa được ngăn chặn? | Chưa tối ưu Chunking strategy. |
| Why 4 | Tại sao cơ chế hiện tại chưa phát hiện hoặc xử lý được? | Đang dùng chunking mặc định. |
| Why 5 | Root cause có thể hành động được là gì? | Tinh chỉnh Chunk size và overlap. |

**Root cause và proposed fix:**
> *Câu trả lời:* Tinh chỉnh tham số chunking và sử dụng Semantic Chunking thay vì Fixed-size chunking.

---

## 3. Failure Clustering

Một root cause có thể tạo ra nhiều failures. Nhóm theo nguyên nhân có thể sửa,
không chỉ nhóm theo tên metric.

| Cluster | Root Cause | Failure IDs | Priority |
|---|---|---|---|
| 1 | BM25 không hiểu ngữ nghĩa từ đồng nghĩa | M03, E04, H02 | High |
| 2 | Thiếu Guardrails và System Prompt lỏng lẻo | A01, A02, A03 | High |
| 3 | Lỗi Cắt Chunk (Chunking Strategy) chưa tối ưu | M06, H01 | Medium |

**Nếu chỉ được sửa một cluster, bạn chọn cluster nào và vì sao?**
> *Câu trả lời:* Sửa Cluster 1 (BM25). Vì Retrieval là xương sống của RAG, nếu Retrieval lấy sai tài liệu thì mọi bước Generator phía sau dù tối ưu prompt đến mấy cũng vô dụng.

---

## 4. Improvement Log

Paste output của `generate_improvement_log()`:

```text
| Component | Metric | Current | Target | Method |
|---|---|---|---|---|
| Retrieval | Context Recall | 0.49 | 0.85 | Use Vector Search |
| Generation| Faithfulness | 0.39 | 0.90 | Update System Prompt |
| Evaluation| LLM Judge Bias| High | Low | Refine Rubric Prompt |
```

**Ba improvement suggestions ưu tiên**

1. Chuyển sang Hybrid Search (Vector + Keyword)
2. Thêm System Prompt ép buộc từ chối nếu không có context.
3. Tinh chỉnh Chunk Size lớn hơn để giữ nguyên văn bản.

Với mỗi suggestion, nêu metric dự kiến thay đổi và cách đo lại.

| Suggestion | Target metric | Verification method |
|---|---|---|
| Chuyển sang Hybrid Search | Context Recall | Chạy lại Evaluate, mong đợi Recall > 0.8 |
| Thêm Strict System Prompt | Faithfulness | Chạy lại Evaluate, lỗi hallucination giảm xuống 0 |
| Tinh chỉnh Chunk Size | Completeness | Chạy lại Evaluate, Completeness tăng do đủ ý |

---

## 5. Regression Testing Strategy

**Câu 1: Khi nào chạy `run_regression()` trong production workflow?**
> *Câu trả lời:* Chạy mỗi khi có Pull Request thay đổi code liên quan đến pipeline RAG (vd thay đổi prompt, đổi embedding model, hoặc tinh chỉnh chunking).

**Câu 2: Threshold drop 0.05 có phù hợp OrbitTech Customer Support không? Vì sao?**
> *Câu trả lời:* Phù hợp. Vì hỗ trợ khách hàng cần sự ổn định. Bất kỳ sự suy giảm nào lớn hơn 5% (0.05) có thể dẫn tới tỷ lệ phàn nàn của khách hàng tăng vọt.

**Câu 3: Metric/failure nào phải block deployment, metric nào chỉ alert?**
> *Câu trả lời:* Block deployment nếu `Faithfulness` hoặc `Context Precision` rớt. Alert nếu `Completeness` hoặc `Relevance` giảm nhẹ.

**Câu 4: Điền evaluation stages vào flow.**
```text
Code/prompt/retrieval change → [Run Unit/Integration Tests] → [Run RAG Evaluation on Golden Dataset] → [Manual/Human Review for edge cases] → Deploy
```
> *Giải thích:* Cần tự động đánh giá bằng RAGAS trên tập Golden trước, nếu pass các threshold mới cho phép Deploy.

---

## 6. Continuous Improvement Loop

```text
Evaluate → Analyze → Improve → Augment benchmark → Repeat
```

| Priority | Action | Metric dự kiến cải thiện | Expected impact |
|---:|---|---|---|
| 1 | Áp dụng Vector Database | Context Recall | Cao (Giảm hẳn các case trả lời sai do không tìm thấy doc) |
| 2 | Cập nhật Guardrails Prompt | Faithfulness | Cao (Không còn tình trạng AI tự chế thông tin) |
| 3 | Bổ sung câu hỏi vào Golden | Pass Rate | Trung bình (Tăng độ tin cậy của benchmark) |

**Hai hoặc ba failure cases nào cần thêm vào benchmark ở vòng tiếp theo?**
> *Câu trả lời:* Nên thêm các câu hỏi hóc búa hơn đòi hỏi phải tổng hợp thông tin từ 3 tài liệu trở lên (Complex reasoning), và thêm các câu hỏi cố tình dùng ngôn ngữ địa phương để test độ robustness của Retrieval.

---

## 7. Final Reflection

**Điều gì trong kết quả benchmark trái với dự đoán ban đầu của bạn?**
> *Câu trả lời:* Ban đầu tôi nghĩ BM25 kết hợp Rerank sẽ hoạt động đủ tốt cho một domain nhỏ. Nhưng thực tế điểm Context Recall lại rớt thảm hại, chứng minh rằng Keyword matching cực kỳ yếu khi khách hàng diễn đạt câu hỏi bằng cách khác văn bản gốc.

**Word-overlap heuristics trong lab có giới hạn gì? Nếu đưa hệ thống vào
production, bạn sẽ thay hoặc bổ sung metric nào?**
> *Câu trả lời:* Word-overlap cực kỳ cứng nhắc, không tính đến các từ đồng nghĩa (synonyms). Khi đưa vào production, tôi sẽ dùng embedding similarity (Cosine Similarity của embeddings) và LLM-as-a-Judge kết hợp cross-encoder để chấm điểm Semantic Relevance.
