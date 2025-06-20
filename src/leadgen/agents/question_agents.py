# Question generation agents for the leadgen application

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from pydantic_ai import Agent

from leadgen.services.llm_service import LLMService
from leadgen.config.config_loader import ConfigLoader
from leadgen.utils.helpers import format_qa_for_prompt, extract_keywords_from_text


class QuestionList(BaseModel):
    """Model for a list of questions"""
    questions: List[str]


class KeywordList(BaseModel):
    """Model for a list of keywords"""
    keywords: List[str]


class DefaultQuestionsAgent:
    """Agent for handling the default questions stage"""
    
    def __init__(self):
        """Initialize the default questions agent"""
        self.config_loader = ConfigLoader()
        self.llm_service = LLMService()
        self.system_prompt = self.config_loader.get_system_prompt("default_questions_agent")
        self.default_questions = self.config_loader.get_default_questions()
    
    def get_default_questions(self) -> List[str]:
        """Get the default questions
        
        Returns:
            List of default questions
        """
        return self.default_questions
    
    def process_answers(self, questions_and_answers: Dict[str, str]) -> Dict[str, str]:
        """Process the answers to the default questions
        
        Args:
            questions_and_answers: Dictionary mapping questions to answers
            
        Returns:
            Processed questions and answers
        """
        # In this simple implementation, we just return the questions and answers as is
        # In a more complex implementation, you might do some processing or validation
        return questions_and_answers


class PersonalizedQuestionsAgent:
    """Agent for generating personalized questions based on initial answers"""
    
    def __init__(self):
        """Initialize the personalized questions agent"""
        self.config_loader = ConfigLoader()
        self.llm_service = LLMService()
        self.system_prompt = self.config_loader.get_system_prompt("personalized_questions_agent")
        
    def generate_questions(self, initial_qa: Dict[str, str], num_questions: int = 10) -> List[str]:
        """Generate personalized questions based on initial answers
        
        Args:
            initial_qa: Dictionary mapping initial questions to answers
            num_questions: Number of questions to generate
            
        Returns:
            List of generated questions
        """
        # Create an agent with the appropriate system prompt and output type
        agent = self.llm_service.create_agent(
            system_prompt=self.system_prompt,
            output_type=QuestionList
        )
        
        # Format the initial Q&A for the prompt
        formatted_qa = format_qa_for_prompt(initial_qa)
        
        # Generate the prompt
        prompt = f"Based on the following information, generate {num_questions} personalized questions to gather deeper insights:\n\n{formatted_qa}"
        
        # Run the agent
        result = agent.run_sync(prompt)
        
        # Return the generated questions
        return result.output.questions
    
    def process_answers(self, questions_and_answers: Dict[str, str]) -> Dict[str, str]:
        """Process the answers to the personalized questions
        
        Args:
            questions_and_answers: Dictionary mapping questions to answers
            
        Returns:
            Processed questions and answers
        """
        # In this simple implementation, we just return the questions and answers as is
        return questions_and_answers


class KeywordGenerationAgent:
    """Agent for generating keywords based on questions and answers"""
    
    def __init__(self):
        """Initialize the keyword generation agent"""
        self.config_loader = ConfigLoader()
        self.llm_service = LLMService()
        self.system_prompt = self.config_loader.get_system_prompt("keyword_generation_agent")
    
    def generate_keywords(self, all_qa_data: Dict[str, Dict[str, str]], num_keywords: int = 10) -> List[str]:
        """Generate keywords based on all questions and answers
        
        Args:
            all_qa_data: Dictionary mapping stage names to Q&A dictionaries
            num_keywords: Number of keywords to generate
            
        Returns:
            List of generated keywords
        """
        # Create an agent with the appropriate system prompt and output type
        agent = self.llm_service.create_agent(
            system_prompt=self.system_prompt,
            output_type=KeywordList
        )
        
        # Format all Q&A data for the prompt
        formatted_data = ""
        for stage, qa_dict in all_qa_data.items():
            formatted_data += f"\n\n--- {stage} ---\n"
            formatted_data += format_qa_for_prompt(qa_dict)
        
        # Generate the prompt
        prompt = f"Based on the following questions and answers, generate {num_keywords} relevant keywords for lead generation:\n\n{formatted_data}"
        
        # Run the agent
        result = agent.run_sync(prompt)
        
        # Return the generated keywords
        return result.output.keywords


class ICPGenerationAgent:
    """Agent for generating an Ideal Customer Profile based on all data"""
    
    def __init__(self):
        """Initialize the ICP generation agent"""
        self.config_loader = ConfigLoader()
        self.llm_service = LLMService()
        self.system_prompt = self.config_loader.get_system_prompt("icp_generation_agent")
    
    def generate_icp(self, all_qa_data: Dict[str, Dict[str, str]], keywords: List[str]) -> Dict[str, Any]:
        """Generate an Ideal Customer Profile based on all data
        
        Args:
            all_qa_data: Dictionary mapping stage names to Q&A dictionaries
            keywords: List of generated keywords
            
        Returns:
            Dictionary containing the Ideal Customer Profile
        """
        # Create an agent with the appropriate system prompt
        agent = self.llm_service.create_agent(system_prompt=self.system_prompt)
        
        # Format all Q&A data for the prompt
        formatted_data = ""
        for stage, qa_dict in all_qa_data.items():
            formatted_data += f"\n\n--- {stage} ---\n"
            formatted_data += format_qa_for_prompt(qa_dict)
        
        # Add keywords to the prompt
        formatted_keywords = ", ".join(keywords)
        formatted_data += f"\n\n--- Keywords ---\n{formatted_keywords}"
        
        # Generate the prompt
        prompt = f"Based on all the following information, generate a detailed ideal customer profile:\n\n{formatted_data}"
        
        # Run the agent
        result = agent.run_sync(prompt)
        
        # Return the generated ICP
        # Note: In a real implementation, you might want to parse this into a structured format
        return {"profile": result.output}