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