"""
Ollama integration client for LLM-powered decision making.
"""

import json
from typing import Dict, Any, Optional
import urllib.request
import urllib.error


class OllamaClient:
    """
    Client for interacting with Ollama API.
    
    Provides methods for generating responses from local LLM models
    for enhanced villain decision-making.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama2"
    ):
        self.base_url = base_url
        self.model = model
        self.is_available = False
        self._check_connection()
    
    def _check_connection(self) -> None:
        """Check if Ollama is available."""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=2) as response:
                self.is_available = response.status == 200
        except (urllib.error.URLError, TimeoutError):
            self.is_available = False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 200
    ) -> Optional[str]:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response or None if unavailable
        """
        if not self.is_available:
            return None
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        if max_tokens:
            payload["options"] = {"num_predict": max_tokens}
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "")
        
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
            return None
    
    def generate_decision_context(
        self,
        context: Dict[str, Any],
        personality_traits: Dict[str, float]
    ) -> Optional[str]:
        """
        Generate decision context using the LLM.
        
        Args:
            context: Current game context
            personality_traits: Current personality traits
            
        Returns:
            Generated decision context
        """
        if not self.is_available:
            return None
        
        traits_str = ", ".join(f"{k}: {v:.2f}" for k, v in personality_traits.items())
        
        prompt = f"""
        Current situation: {context.get('situation', 'unknown')}
        Available actions: {', '.join(context.get('available_actions', []))}
        Recent events: {context.get('recent_events', 'none')}
        
        Personality traits: {traits_str}
        
        What is the most appropriate action for a villain with these traits?
        """
        
        return self.generate(prompt, temperature=0.8)
    
    def generate_strategy_explanation(
        self,
        strategy: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[str]:
        """Generate an explanation for a strategy choice."""
        if not self.is_available:
            return None
        
        prompt = f"""
        Explain why the following strategy is appropriate:
        Strategy: {strategy.get('name', 'unknown')}
        Description: {strategy.get('description', 'none')}
        
        Current context: {context.get('description', 'unknown')}
        
        Provide a brief, in-character explanation as a villain would give.
        """
        
        return self.generate(prompt, temperature=0.6)
    
    def generate_taunt_or_dialogue(
        self,
        context: Dict[str, Any],
        style: str = "menacing"
    ) -> Optional[str]:
        """Generate villain dialogue or taunts."""
        if not self.is_available:
            return None
        
        prompt = f"""
        Generate a {style} taunt or dialogue line for a villain in this situation:
        {context.get('situation', 'unknown')}
        
        Keep it short (1-2 sentences), menacing, and fitting for a villain.
        """
        
        return self.generate(prompt, temperature=0.9)
    
    def is_connected(self) -> bool:
        """Check if Ollama is connected."""
        return self.is_available
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            "available": self.is_available,
            "base_url": self.base_url,
            "model": self.model
        }
