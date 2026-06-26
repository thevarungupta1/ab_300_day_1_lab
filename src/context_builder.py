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