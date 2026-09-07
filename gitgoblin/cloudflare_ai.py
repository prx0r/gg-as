"""Cloudflare AI integration — free models for web search and intelligence."""

from __future__ import annotations

import json
import httpx
from pathlib import Path
from typing import Optional


# Load credentials from vault
def get_cloudflare_credentials() -> dict:
    """Load Cloudflare credentials from vault."""
    vault_path = Path("/root/.agent-vault/vault.json")
    if vault_path.exists():
        with open(vault_path) as f:
            vault = json.load(f)
        return {
            "account_id": vault.get("CLOUDFLARE_ACCOUNT_ID"),
            "api_token": vault.get("CLOUDFLARE_API_TOKEN"),
        }
    return {}


# Available free models
FREE_MODELS = {
    "text": [
        "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "@cf/mistralai/mistral-small-3.1-24b-instruct",
        "@cf/qwen/qwen3-30b-a3b-fp8",
        "@cf/deepseek-ai/deepseek-v4-flash",
        "@cf/openai/gpt-oss-20b",
        "@cf/meta/llama-3.1-8b-instruct-fp8",
        "@cf/google/gemma-4-26b-a4b-it",
    ],
    "fast": [
        "@cf/meta/llama-3.1-8b-instruct-fp8",
        "@cf/meta/llama-3.2-3b-instruct",
        "@cf/meta/llama-3.2-1b-instruct",
    ],
    "smart": [
        "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "@cf/mistralai/mistral-small-3.1-24b-instruct",
        "@cf/qwen/qwen3-30b-a3b-fp8",
    ],
}


class CloudflareAI:
    """Cloudflare Workers AI client for free inference."""
    
    def __init__(self, account_id: str = "", api_token: str = ""):
        creds = get_cloudflare_credentials()
        self.account_id = account_id or creds.get("account_id", "")
        self.api_token = api_token or creds.get("api_token", "")
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"
    
    def run_model(self, model: str, prompt: str, max_tokens: int = 500) -> dict:
        """Run a model with a prompt."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        
        resp = httpx.post(
            f"{self.base_url}/{model}",
            headers=headers,
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()
    
    def search_engineers(self, niche: str, market: str) -> list[dict]:
        """Use AI to find engineers in a niche."""
        prompt = f"""Find the top 8 engineers working on {niche} in {market}.
        
For each engineer, provide:
- GitHub username (if known)
- What they work on
- Why they're relevant

Focus on:
- People building the infrastructure
- People solving the actual problems
- People with public GitHub activity

Return as JSON array."""
        
        model = "@cf/meta/llama-3.1-8b-instruct-fp8"  # Fast model
        result = self.run_model(model, prompt, max_tokens=1000)
        
        # Parse response
        try:
            content = result.get("result", {}).get("response", "")
            # Try to extract JSON from response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        
        return []
    
    def analyze_signal(self, signal_data: dict) -> dict:
        """Use AI to analyze a signal."""
        prompt = f"""Analyze this engineering signal:
        
Target: {signal_data.get('target_id', '')}
Alpha: {signal_data.get('technical_alpha', 0)}
Experts: {signal_data.get('expert_count', 0)}

What does this convergence mean? What should we build?
Return as JSON."""
        
        model = "@cf/meta/llama-3.1-8b-instruct-fp8"
        result = self.run_model(model, prompt, max_tokens=500)
        
        try:
            content = result.get("result", {}).get("response", "")
            return {"analysis": content}
        except Exception:
            return {"analysis": "Unable to analyze"}


# Global client
cloudflare_ai = CloudflareAI()
