from domain_assistant import DomainAssistant
import json

def test_ai():
    print("Initializing DomainAssistant...")
    assistant = DomainAssistant.from_corpus("data/technology_store")
    
    question = "How many USB-C ports does the NovaBook 14 have?"
    print(f"\nQuestion: {question}")
    
    print("\nRetrieving contexts...")
    contexts = assistant.retrieve(question)
    for i, ctx in enumerate(contexts):
        print(f"  Context {i+1}: {ctx[:100]}...")
        
    print("\nGenerating answer with AI...")
    answer = assistant.answer(question)
    print(f"\nAnswer:\n{answer}")

if __name__ == "__main__":
    test_ai()
