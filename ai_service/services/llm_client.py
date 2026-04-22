"""LLM Client - Abstraction for different LLM providers."""

import logging
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for LLM API calls."""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.1,
        system_prompt: str | None = None,
    ) -> str:
        """Generate completion from prompt."""
        if self.provider == "openai":
            return await self._openai_complete(prompt, max_tokens, temperature, system_prompt)
        elif self.provider == "azure":
            return await self._azure_complete(prompt, max_tokens, temperature, system_prompt)
        elif self.provider == "local":
            return await self._local_complete(prompt, max_tokens, temperature, system_prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    async def _openai_complete(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str | None,
    ) -> str:
        """Complete using OpenAI API."""
        import openai
        
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        return response.choices[0].message.content
    
    async def _azure_complete(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str | None,
    ) -> str:
        """Complete using Azure OpenAI API."""
        import openai
        
        client = openai.AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        )
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await client.chat.completions.create(
            model=settings.AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        return response.choices[0].message.content
    
    async def _local_complete(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str | None,
    ) -> str:
        """Complete using local LLM (Ollama)."""
        async with httpx.AsyncClient() as client:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = await client.post(
                f"{settings.LOCAL_LLM_URL}/api/generate",
                json={
                    "model": settings.LOCAL_LLM_MODEL,
                    "prompt": full_prompt,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                    },
                    "stream": False,
                },
                timeout=60.0,
            )
            
            response.raise_for_status()
            return response.json()["response"]
