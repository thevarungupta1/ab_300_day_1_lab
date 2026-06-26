from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
from src.foundry_client import ask_ai
from src.trace_logger import log_trace
from src.memory_store import save_memory, get_memory

def main():
    session_id = "invoice_portal_review"
    
    previous_memory = get_memory(session_id)
    
    memory_text = "\n".join([
        f"{role}: {content}"
        for role, content in previous_memory
    ])

    new_question = """
    We have now added payment gateway integration to the invoice portal.
    What should we review before approving this design?
    """

    system_prompt = f"""
    You are a memory-aware enterprise architect agent.

    Previous Memory:
    {memory_text}
    
    Reasing Instructions:
    1. Check previous risks.and
    2. Connect old risks with the new requirement.
    3. Identify new risks.
    4. Give approval recommendation.

    Return:
    Previous Context Used:
    New Risks:
    Reasoning:
    Final Recommendation:
    """

    answer = ask_ai(
        system_message=system_prompt,
        user_prompt=new_question,
        feature="memory_reasining"
    )
    
    save_memory(session_id, "user", new_question)
    save_memory(session_id, "assistant", answer)

    print("\n======Memory Reasoning Demo=======\n")
    print(answer)
    
    
if __name__ == "__main__":
    main()





    

