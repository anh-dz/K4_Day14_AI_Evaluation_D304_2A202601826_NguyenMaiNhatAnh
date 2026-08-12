import json
import os

with open("golden_dataset.json", "r") as f:
    data = json.load(f)

docs = [
    "00_system_scope.md",
    "01_product_catalog.md",
    "02_orders_and_payments.md",
    "03_promotions_and_membership.md",
    "04_shipping_and_delivery.md",
    "05_returns_and_exchanges.md",
    "06_warranty_policy.md",
    "07_repair_and_technical_support.md",
    "08_accounts_privacy_and_security.md",
    "09_escalation_and_policy_updates.md"
]

doc_texts = {}
for doc in docs:
    with open(os.path.join("data", "technology_store", doc), "r") as f:
        content = f.read()
        # Find first non-empty paragraph after frontmatter (---)
        lines = content.split('\n')
        in_frontmatter = False
        text_lines = []
        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter and line.strip() and not line.startswith('#'):
                text_lines.append(line.strip())
        doc_texts[doc] = text_lines[0] if text_lines else content[:50]

for i, pair in enumerate(data["qa_pairs"]):
    pair["question"] = f"Dummy question for {pair['id']}?"
    pair["expected_answer"] = f"Dummy expected answer for {pair['id']}."
    
    if pair["id"].startswith("E"):
        doc = docs[(i % 9) + 1]
        pair["contexts"] = [{"source_doc": doc, "text": doc_texts[doc]}]
    elif pair["id"].startswith("M") or pair["id"].startswith("H"):
        doc1 = docs[(i % 9) + 1]
        doc2 = docs[((i + 1) % 9) + 1]
        pair["contexts"] = [
            {"source_doc": doc1, "text": doc_texts[doc1]},
            {"source_doc": doc2, "text": doc_texts[doc2]}
        ]
    elif pair["id"] == "A01":
        pair["attack_type"] = "out_of_scope"
        pair["contexts"] = [{"source_doc": "00_system_scope.md", "text": doc_texts["00_system_scope.md"]}]
    elif pair["id"] == "A02":
        pair["attack_type"] = "prompt_injection"
        pair["contexts"] = [{"source_doc": "00_system_scope.md", "text": doc_texts["00_system_scope.md"]}]
    elif pair["id"] == "A03":
        pair["attack_type"] = "false_premise_or_ambiguous_trap"
        pair["contexts"] = [{"source_doc": "00_system_scope.md", "text": doc_texts["00_system_scope.md"]}]

with open("golden_dataset.json", "w") as f:
    json.dump(data, f, indent=2)
