# LLM Service for handling interactions with Groq LLM

import os
from typing import List, Dict, Any, Optional

from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel


class LLMService:
    """Service for interacting with Groq LLM using Pydantic AI"""
    
    def __init__(self, model_name: str = "qwen/qwen3-32b"):
        """Initialize the LLM service with the specified model
        
        Args:
            model_name: The name of the Groq model to use
        """
        self.model_name = model_name
        self._check_api_key()
        self.model = GroqModel(model_name)
    
    def _check_api_key(self):
        """Check if the GROQ_API_KEY environment variable is set"""
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError(
                "GROQ_API_KEY environment variable is not set. "
                "Please set it before using the LLM service."
            )
    
    def create_agent(self, system_prompt: str, output_type: Any = None) -> Agent:
        """Create a Pydantic AI agent with the specified system prompt
        
        Args:
            system_prompt: The system prompt for the agent
            output_type: Optional output type for structured responses
            
        Returns:
            A configured Pydantic AI agent
        """
        if output_type:
            return Agent(self.model, system_prompt=system_prompt, output_type=output_type)
        return Agent(self.model, system_prompt=system_prompt)
    
    def generate_questions(self, agent: Agent, context: Dict[str, Any], num_questions: int = 10) -> List[str]:
        """Generate questions using the provided agent and context
        
        Args:
            agent: The Pydantic AI agent to use
            context: The context information for question generation
            num_questions: The number of questions to generate (default: 10)
            
        Returns:
            A list of generated questions
        """
        prompt = f"Based on the following information, generate {num_questions} relevant questions:\n\n{context}"
        result = agent.run_sync(prompt)
        return result.output
    
    def generate_keywords(self, agent: Agent, questions_and_answers: Dict[str, str]) -> List[str]:
        """Generate keywords based on questions and answers
        
        Args:
            agent: The Pydantic AI agent to use
            questions_and_answers: Dictionary mapping questions to answers
            
        Returns:
            A list of generated keywords
        """
        qa_text = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in questions_and_answers.items()])
        prompt = f"Based on the following questions and answers, generate a list of relevant keywords:\n\n{qa_text}"
        result = agent.run_sync(prompt)
        return result.output
    
    def generate_ideal_customer_profile(self, agent: Agent, all_qa_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an ideal customer profile based on all collected data
        
        Args:
            agent: The Pydantic AI agent to use
            all_qa_data: All collected question and answer data
            
        Returns:
            A dictionary containing the ideal customer profile
        """
        # Format the data for the prompt
        formatted_data = ""
        for stage, qa_dict in all_qa_data.items():
            formatted_data += f"\n\n--- {stage} ---\n"
            for q, a in qa_dict.items():
                formatted_data += f"Q: {q}\nA: {a}\n"
        
        prompt = f"Based on all the following information, generate a detailed ideal customer profile:\n\n{formatted_data}"
        result = agent.run_sync(prompt)
        return result.output