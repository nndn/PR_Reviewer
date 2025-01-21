from src.ports.ai import ILanguageModel, PydanticModel
from openai import OpenAI
from typing import Generic
import instructor


class OpenAIModel(ILanguageModel, Generic[PydanticModel]):
    
    def __init__(self, api_key:str):
        self.client = instructor.from_openai(OpenAI(api_key=api_key))
        
    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type: type[PydanticModel]) -> PydanticModel:
        response = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        response_model=response_type,
                        messages=[
                            {"role":"developer", "content":system_prompt},
                            {"role":"user", "content":user_prompt}
                        ],
                        strict=True,
                    )
        return response
