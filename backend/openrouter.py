"""OpenRouter API client for Straight Dope."""

import httpx
import asyncio
from typing import List, Dict, Any, Optional
from .config import OPENROUTER_API_KEY, OPENROUTER_API_URL


async def query_model(
    model: str,
    system_prompt: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0,
) -> Optional[Dict[str, Any]]:
    """
    Query a model via OpenRouter with a system prompt.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            message = data["choices"][0]["message"]
            return {"content": message.get("content", "")}
    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_roles_parallel(
    roles: List[Dict[str, str]],
    messages: List[Dict[str, str]],
) -> List[Optional[Dict[str, Any]]]:
    """
    Query multiple roles in parallel. Each role is a dict with 'name', 'model', 'system_prompt'.
    Returns a list of response dicts in the same order as roles.
    """
    tasks = [
        query_model(role["model"], role["system_prompt"], messages)
        for role in roles
    ]
    return await asyncio.gather(*tasks)
