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