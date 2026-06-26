from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import FAST_MODEL, REASONING_MODEL
from src.foundry_client import ask_ai


def select_model(task_type):
    if task_type in ["classification", "summary"]:
        return FAST_MODEL
    if task_type in ["architecture_review", "risk_analysis"]:
        return REASONING_MODEL
    return FAST_MODEL  # Default to FAST_MODEL if task_type is unrecognized


def main():
    tasks = [
        {
            "type": "classification",
            "prompt": "Classify this request: Can I store customer invoices in personal Google Drive?",
        },
        {
            "type": "summary",
            "prompt": "Summarize why RBAC is important in enterprise applications.",
        },
        {
            "type": "architecture_review",
            "prompt": "Review the architecture of a customer invoice portal built with Python FastAPI backend, React frontend, PostgresSQL database, and Azure App Service.",
        },
        {
            "type": "risk_analysis",
            "prompt": "Analyze the risks associated with storing sensitive customer data in a cloud environment.",
        }
    ]    
    system_prompt = """
    You are an enterprise AI assistent
    Answer the task based on the user's request
    Keep the answer practicle and concise.
    """
    
    print("\n======LLM Ecosystem Router Demo=======\n")
    for task in tasks:
        selected_model = select_model(task["type"])

        answer = ask_ai(
            system_message=system_prompt,
            user_prompt=task["prompt"],
            feature="llm_ecosystem_router",
            model=selected_model
        )
        print(f"Task: {task['type']}")
        print(f"Prompt: {task['prompt']}")
        print(f"Answer: {answer}\n")
        
if __name__ == "__main__":
    main()