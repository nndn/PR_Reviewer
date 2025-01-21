from src.ports.ai import ILanguageModel
from anthropic import Anthropic

# class ClaudeAIModel(ILanguageModel):
    
#     def __init__(self, api_key:str):
#         self.client = Anthropic(api_key=api_key)
    
#     def sync_prompt(self, user_prompt: str, system_prompt: str) -> str:
#         response = self.client.messages.create(
#                         model="claude-3-5-sonnet-20240620",
#                         max_tokens=2000,
#                         messages=[
#                             {"role":"assistant", "content":system_prompt},
#                             {"role":"user", "content":user_prompt}
#                         ]
#                     )
        
#         return str(response.content[0]) or ""
