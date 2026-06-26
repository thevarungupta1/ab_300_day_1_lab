from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.foundry_client import ask_ai
from src.trace_logger import log_trace

def main():
    module = "01_agentic_ai"
    
    proposal = """
    We are building a customer invoice portal using Python FastAPI backend, React frontend, PostgresSQL database, and Azure App Service. 
    Users can view invoices, download PDFs and make payments.    
    """
    
    system_prompt = Path("prompts/agentic_reviewer.txt").read_text(encoding="utf-8")
    
    log_trace(module, "ArchitectureAgent", "Input recived", "SUCCESS", proposal)
    
    answer = ask_ai(
        system_message=system_prompt,
        user_prompt=proposal,
        feature="agentic_ai"
    )

    log_trace(module, "ArchitectureAgent", "Review completed", "SUCCESS", answer)
    
    print("\n======Agentic AI Demo=======\n")
    print(answer)
    
if __name__ == "__main__":
    main()