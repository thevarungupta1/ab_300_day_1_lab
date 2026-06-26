from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))



from src.foundry_client import ask_ai
from src.trace_logger import log_trace

def run_agent(agent_name, prompt_file, proposal):
    system_prompt = Path(prompt_file).read_text(encoding="utf-8")
    
    log_trace("02_multi_agent", agent_name, "Started", "SUCCESS", "Agent started review")
    
    response = ask_ai(
        system_message=system_prompt,
        user_prompt=proposal,
        feature=agent_name)

    log_trace("02_multi_agent", agent_name, "Completed", "SUCCESS", response)
    
    return agent_name, response

def main():
    proposal = """"
    We are designing a healthcare appointent platform.
    It has React frontend, FastAPI backend, PostgreSQL database,
    Redis cache, Azure Blocb Storage, and Azure App Service deployment.
    Patient records and appointment history will be stored.
    """

    agents = [
        ("ArchitectureAgent", "prompts/architecture_agent.txt"),
        ("SecurityAgent", "prompts/security_agent.txt"),
        ("ComplianceAgent", "prompts/compliance_agent.txt"),
    ]
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(run_agent, agent_name, prompt_file, proposal)
            for agent_name, prompt_file in agents
        ]
        
        for future in futures:
            agent_name, response = future.result()
            results[agent_name] = response

        combined_feedback = f"""
ARCHITECTURE FEEDBACK:
{results['ArchitectureAgent']}

SECURITY FEEDBACK:
{results['SecurityAgent']}

COMPLIANCE FEEDBACK:
{results['ComplianceAgent']}
"""
        final_prompt = Path("prompts/final_reviewer.txt").read_text(encoding="utf-8")
        
        final_response = ask_ai(
            system_message=final_prompt,
            user_prompt=combined_feedback,
            feature="final_reviewer"
        )
        
        print("\n======Multi-Agent AI Demo=======\n")
        print(final_response)
        
        
if __name__ == "__main__":
    main()
    

