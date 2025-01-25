from src.ports.ai import ILanguageModel
from huggingface_hub import InferenceClient

# class LlamaAIModel(ILanguageModel):

#     def __init__(self, api_key:str):
#         self.client = InferenceClient(api_key=api_key)

#     def sync_prompt(self, system_prompt: str, user_prompt: str) -> str:
#         response = self.client.chat.completions.create(
#                         model="MiniMaxAI/MiniMax-Text-01",
#                         messages=[
#                             {"role":"developer", "content":system_prompt},
#                             {"role":"user", "content":user_prompt}
#                         ]
#                     )
#         return response.choices[0].message.content or ""
