from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class ILanguageModel(ABC, Generic[PydanticModel]):
    """ Implementations for this interface should be in the adapter layer (outbound ports).
        This port is for language models that will used by the reviewer application """
    
    @abstractmethod
    def sync_prompt(self, system_prompt: str, user_prompt: str, response_type:PydanticModel) -> PydanticModel:
        """ Takes a PydanticModel Type as input and output variable will be of that type """
        pass
    
