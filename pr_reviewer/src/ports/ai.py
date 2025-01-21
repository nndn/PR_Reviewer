from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class ILanguageModel(ABC, Generic[PydanticModel]):
    
    @abstractmethod
    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type:PydanticModel) -> PydanticModel:
        pass
    
