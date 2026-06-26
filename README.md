# Enterprise Agentic AI

### Step 1: Create a project folder
```bash
mkdir enterprise-agentic-ai
cd enterprise-agentic-ai
```

### Step 2: Create a virtual Envirnment
```bash
python -m venv .venv
# windows
.venv\Scripts\activate

# mac/linux
source .venv/bin/activate
```

### Step 3: Install packages
create `requirements.txt`

```
azure-ai-inference
azure-core
python-dotenv
pandas
scikit-learn
```

```bash
pip install -r requirements.txt
```

### Step 4: Create folder structure

```
enterprise-agentic-ai
|--.venv
|--data
|--modules
|--prompts
|--reports
|--src
|--.env
|--README.md
|--requirements.txt

```

### Step 5: Add Azure Foundary Configuration
`.env`

```
AZURE_AI_ENDPOINT=""
AZURE_AI_KEY=""

PRIMARY_MODEL="gpt-4o-mini"
REASONING_MODEL="gpt-4o"
FAST_MODEL="gpt-4o-mini"
```

### Step 6: Create Config file
`src/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
AZURE_AI_KEY = os.getenv("AZURE_AI_KEY")

PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "gpt-4o-mini")
REASONING_MODEL = os.getenv("REASONING_MODEL", "gpt-4o")
FAST_MODEL = os.getenv("FAST_MODEL", "gpt-4o-mini")

```


### Step 7: Create Foundry Client
`src/foundry_client.py`

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from src.config import AZURE_AI_ENDPOINT, AZURE_AI_KEY, PRIMARY_MODEL

client = ChatCompletionsClient(
    endpoint=AZURE_AI_ENDPOINT,
    credential=AzureKeyCredential(AZURE_AI_KEY)
)

def ask_ai(
    system_message: str,
    user_prompt: str,
    model: str = None,
    temperature : float = 0.2,
    feature: str = "general"
):
    
    selected_model = model or PRIMARY_MODEL
    
    response = client.complete(
        model=selected_model,
        messages=[
            SystemMessage(content=system_message),
            UserMessage(content=user_prompt)
        ],
        temperature=temperature,
    )
    
    return response.choices[0].message.content
```

### Step 8: Create Cost Tracker
`src/cost_tracker.py`

```python
import csv
import os
from datetime import datetime

COST_FILE = "reports/cost_report.csv"

MODEL_PRICING = {
    "gpt-4o-mini": {
        "input": 0.00015 / 1000,
        "output": 0.00060 / 1000
    },
    "gpt-4o": {
        "input": 0.005 / 1000,
        "output": 0.015 / 1000
    },
}

def log_cost(feature, model, input_tokens, output_tokens):
    os.makedirs("reports", exist_ok=True)
    
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4o-mini"])
    
    estimated_cost = (
        input_tokens * pricing["input"] +
        output_tokens * pricing["output"]
    )

    file_exists = os.path.exists(COST_FILE)
    
    with open(COST_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow([
                "timestamp", 
                "feature", 
                "model", 
                "input_tokens", 
                "output_tokens", 
                "estimated_cost"
        ])
            
        writer.writerow([
            datetime.now(),
            feature,
            model,
            input_tokens,
            output_tokens,
            round(estimated_cost, 6)
        ])
```

### Step 9: Create Logger
`src\trace_logger.py`

```python
import csv
import os
from datetime import datetime

TRACE_FILE = "reports/execution_trace.csv"

def log_trace(module, agent, step, status, details):
    os.makedirs("reports", exist_ok=True)
    
    file_exists = os.path.exists(TRACE_FILE)
    
    with open(TRACE_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow([
                "timestamp", 
                "module", 
                "agent", 
                "step", 
                "status", 
                "details"
            ])
            
        writer.writerow([
            datetime.now(),
            module,
            agent,
            step,
            status,
            details
        ])
```

### Step 10: Update Foundry Client
update `src/foundry_client.py`

```python
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from src.config import AZURE_AI_ENDPOINT, AZURE_AI_KEY, PRIMARY_MODEL
from src.cost_tracker import log_cost

client = ChatCompletionsClient(
    endpoint=AZURE_AI_ENDPOINT,
    credential=AzureKeyCredential(AZURE_AI_KEY)
)

def ask_ai(
    system_message: str,
    user_prompt: str,
    model: str = None,
    temperature : float = 0.2,
    feature: str = "general"
):
    
    selected_model = model or PRIMARY_MODEL
    
    response = client.complete(
        model=selected_model,
        messages=[
            SystemMessage(content=system_message),
            UserMessage(content=user_prompt)
        ],
        temperature=temperature,
    )
    
    answer = response.choices[0].message.content

    usage = getattr(response, "usage", None)
    
    input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0
    
    log_cost(
        feature=feature,
        model=selected_model,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
    
    return answer
```

### Step 11: Data Files

`data/enterprise_policy.txt`

```
Enterprise applications must follow secure design principles
Customer data must not be stored in personal storage.
Any system handling sensitive data must include audit logging, encryption, RBAC, and data retention rule.
Production workloads must have monitoring, alerting, backup and disaster recovery strategy.
```

`data/security_guidelines.txt`

```
APP APIs must be use authentication and authorization.
JWT tokens must be short lived.
Secrets must be stored in Azure Key Vault.
Sensitive data must be encrypted in transit and at rest.
Public APIs must be rate limiting and request validation.
```

`data/architecture_standards.txt`

```
Enterprise applications should use layered architecture or clean archotecture.
Business logic should be placed directly in controllers.
Systems should be designed for scalability, obervability, maintainability, and failure handling.
For distributed systems, retry, circuit breaker, timeout, and idempatency should be considered
```


### Step 12: Create document loader
`src/document_loader.py`

```python
from pathlib import Path

def load_documents(data_dir= "data"):
    documents = []
    
    for file_path in Path(data_dir).glob("*.txt"):
        documents.append({
            "file_name": file_path.name,
            "content": file_path.read_text(encoding="utf-8")
        })
        
    return documents
```

### Step 13: Create retriver 
`src/simple_retriver.py`

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.document_loader import load_documents

def retrieve_context(query, top_k=2):
    documents = load_documents()
    
    texts = [doc["content"] for doc in documents]

    vertorizer = TfidfVectorizer()
    vectors = vertorizer.fit_transform(texts)
    
    query_vector = vertorizer.transform([query])
    scores = cosine_similarity(query_vector, vectors).flatten()
    
    ranked = scores.argsort()[::-1][:top_k]

    results = []
    
    for index in ranked:
        results.append({
            "source": documents[index]["file_name"],
            "content": documents[index]["content"],
            "score": scores[index]
        })
        
    return results
```

### Step 14: Create Context Builder

`src/content_builder.py`

```python
def build_enterprise_context(role, task, business_context, constraints, examples, retrived_context):
    context = f"""
    ROLE:
    {role}
    
    TASK:
    {task}
    
    Business Context:
    {business_context}
    
    Constraints:
    {constraints}
    
    Examples:
    {examples}
    
    Retrieved Context:
    {retrived_context}
    
    INSTRUCTIONS:
    - Think like a senior enterprise archjitect.
    - Give practical recommendations.
    - Identify risks.
    - Avoid generic answer.
    - Return structured output.
    
    """
    
    return context.strip()
```


------
# Exercise 1: Agentic AI 

### Business Use case:
Enterprise architecture team wants an AI Agent to review applicationm design before technical approcal.

### Purpose:
Demonstarte how an AI Agent is diffeernt from nomal prompt
A normal LLM answer a question
An agent has
- Goal
- Role
- Task
- Decision logic
- Output format
- Trace



### Create Prompt Library
`prompts/agentic_reviewer.txt`

```
You are an Agentic AI Architecture Reviewer.

You must:
1. Understand the user's architecture proposal.
2. Identify missing enterprise concerns.
3. Evaluate security, scalability, obervability and maintainability.
4. Recommand concrete improvements.

Return response in the format:

Architecture Summary:
Risk:
Recommandations:
Final Decision:
```


### Create Main methdo
`modules/01_agentic_ai.py`

```python
from pathlib import Path

from src.foundry_client import ask_ai
from src.trace_logger import log_trace

def main():
    module = "01_agentic_ai"
    
    proposal = """
    We are building a customer invoice portal using Python FastAPI backend, React frontend, PostgresSQL database, and Azure App Service. 
    Users can view invoices, download PDFs and make payments.    
    """
    
    system_prompt = Path("../prompts/agentic_reviewer.txt").read_text(encoding="utf-8")
    
    log_trace(module, "ArchitectureAgent", "Input recived", "SUCCESS", proposal)
    
    answer = ask_ai(
        system_message=system_prompt,
        user_prompt=proposal,
        feature="agentic_ai"
    )

    log_trace(module, "ArchitectureAgent", "Review completed", "SUCCESS", answer)
    
    print("\n======Agentic AI Demo=======\n")
    print(answer)
        
    
    
```

```bash
cd modules
python 01_agentic_ai.py
```


### Deploy model in azure foundary and update key and endpoint