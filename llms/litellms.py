from agents.extensions.models.litellm_model import LitellmModel
import os
import abc
import asyncio
import inspect

class LiteLLMsBase(abc.ABC):
    """
    Base class for all LiteLLM models.
    Handles common initialization logic.
    """

    def __init__(self, model_name: str, api_key: str, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.config = kwargs

        self.base_url = None
        self._client = None

    @abc.abstractmethod
    def _load_model(self):
        self.client = LitellmModel(provider=self.model_name,
                                   base_url=self.base_url,
                                   api_key=self.api_key)
        return self.client
    
    @abc.abstractmethod
    async def generate(self, prompt: str, **kwargs):
        raise NotImplementedError("Subclasses must implement generate()")
    
    async def a_generate(self, prompt: str, **kwargs):
        if not self._client:
            self._load_model()
        
        generation = getattr(self, "generate")
        if inspect.iscoroutinefunction(generation):
            return await generation(prompt, **kwargs)
        else:
            return await asyncio.to_thread(generation, prompt, **kwargs)