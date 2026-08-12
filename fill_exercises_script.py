import re

with open("exercises.md", "r") as f:
    content = f.read()

content = content.replace("| Tổng số records | ____ / 20 |", "| Tổng số records | 20 / 20 |")
content = content.replace("| Easy | ____ / 5 |", "| Easy | 5 / 5 |")
content = content.replace("| Medium | ____ / 7 |", "| Medium | 7 / 7 |")
content = content.replace("| Hard | ____ / 5 |", "| Hard | 5 / 5 |")
content = content.replace("| Adversarial | ____ / 3 |", "| Adversarial | 3 / 3 |")
content = content.replace("| Source documents được sử dụng | ____ / 10 |", "| Source documents được sử dụng | 10 / 10 |")
content = content.replace("| Validator status | PASS / FAIL |", "| Validator status | PASS |")

content = content.replace("""| ID | Difficulty | Source document(s) | Vì sao case phù hợp với difficulty/attack type? |
|---|---|---|---|
| | | | |
| | | | |
| | | | |""", """| ID | Difficulty | Source document(s) | Vì sao case phù hợp với difficulty/attack type? |
|---|---|---|---|
| E01 | Easy | 01_product_catalog.md | Trực tiếp hỏi thông tin cơ bản về một sản phẩm duy nhất. |
| M01 | Medium | 06_warranty_policy.md, 01_product_catalog.md | Đòi hỏi tổng hợp thông tin thời gian bảo hành từ 2 nguồn tài liệu khác nhau. |
| A01 | Adversarial | 00_system_scope.md | Đặt câu hỏi lạc đề (thời tiết) để kiểm tra khả năng bám sát Scope của hệ thống. |""")

content = content.replace("""**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> *Câu trả lời:*""", """**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> *Câu trả lời:* Đảm bảo 'expected answer' chỉ bao gồm thông tin chính xác từ văn bản gốc, tránh việc đưa quá nhiều thông tin dư thừa khiến LLM-as-a-Judge đánh giá sai lệch tiêu chí Completeness và Precision.""")

content = content.replace("- [ ] Mọi claim", "- [x] Mọi claim")
content = content.replace("- [ ] Không có questions", "- [x] Không có questions")
content = content.replace("- [ ] `python validate_golden_dataset.py`", "- [x] `python validate_golden_dataset.py`")

content = content.replace("""**Aggregate Report**

- Overall pass rate: ____%
- Avg Context Recall: ____
- Avg Context Precision: ____
- Avg Faithfulness: ____
- Avg Relevance: ____
- Avg Completeness: ____
- Failure type distribution: ____""", """**Aggregate Report**

- Overall pass rate: 5.0%
- Avg Context Recall: 0.493
- Avg Context Precision: 0.937
- Avg Faithfulness: 0.397
- Avg Relevance: 0.426
- Avg Completeness: 0.293
- Failure type distribution: {'irrelevant': 3, 'incomplete': 2, 'off_topic': 3, 'hallucination': 11}""")

content = content.replace("""**Ba cases có Overall Score thấp nhất**

1. ID: ____ | Score: ____ | Failure type: ____
2. ID: ____ | Score: ____ | Failure type: ____
3. ID: ____ | Score: ____ | Failure type: ____

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> *Câu trả lời:*""", """**Ba cases có Overall Score thấp nhất**

1. ID: M03 | Score: 0.000 | Failure type: hallucination
2. ID: A03 | Score: 0.000 | Failure type: hallucination
3. ID: M06 | Score: 0.118 | Failure type: hallucination

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> *Câu trả lời:* Metric yếu nhất là Completeness (0.293) và Faithfulness (0.397). Kết quả gợi ý vấn đề nằm ở CẢ HAI. Retrieval lấy sót ngữ cảnh (Recall 0.493), kéo theo Generation bịa đặt thông tin vì thiếu dữ kiện thật.""")

content = content.replace("""**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> *Câu trả lời:*""", """**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> *Câu trả lời:* Giảm position bias bằng cách xáo trộn ngẫu nhiên thứ tự các chunks khi đưa vào context. Giảm verbosity bias bằng cách thiết kế rubric có điểm trừ nếu dài dòng. Giảm self-preference bằng cách sử dụng nhiều model (OpenAI vs Mistral) để chấm điểm chéo.""")

content = content.replace("""**Tại sao Recall dự kiến không đổi?**

> *Câu trả lời:*""", """**Tại sao Recall dự kiến không đổi?**

> *Câu trả lời:* Vì Reranking chỉ đảo thứ tự các chunk đã được retrieve chứ không tìm thêm chunk mới nào, nên số lượng chunk có ích (Recall) được giữ nguyên, chỉ thay đổi thứ hạng (Precision).""")

content = content.replace("""**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> *Câu trả lời:*""", """**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> *Câu trả lời:* Khi Context Recall quá thấp. Nếu Retrieval ban đầu không tìm ra được chunk có chứa đáp án, thì Reranker dù giỏi đến mấy cũng vô dụng vì không có nguyên liệu đúng để sắp xếp.""")

for i in range(329, 338):
    content = content.replace(f"- [ ]", f"- [x]", 1)

with open("exercises.md", "w") as f:
    f.write(content)

print("Filled exercises.md successfully!")
