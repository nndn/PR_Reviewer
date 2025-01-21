from src.ports.ai import ILanguageModel, PydanticModel
from openai import OpenAI
from typing import Generic
import instructor


class OpenRouterInstructorAIModel(ILanguageModel, Generic[PydanticModel]):
    
    def __init__(self, api_key:str, model_name: str):
        self.openai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        self.client = instructor.from_openai(self.openai)
        self.model_name = model_name
        
    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type: type[PydanticModel]) -> PydanticModel:
        response = self.client.chat.completions.create(
                        model=self.model_name,
                        response_model=response_type,
                        messages=[
                            {"role":"developer", "content":system_prompt},
                            {"role":"user", "content":user_prompt}
                        ]
                    )
        return response
    
    def sync_prompt2(self, system_prompt: str, user_prompt: str) -> str:
        response = self.openai.chat.completions.create(
                        model="qwen/qwen-2-vl-7b-instruct",
                        messages=[
                            {"role":"developer", "content":system_prompt},
                            {"role":"user", "content":user_prompt}
                        ]
                    )
        return response.choices[0].message.content or ""
    
