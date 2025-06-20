# Lead generation pipeline for orchestrating the entire process

import os
from typing import Dict, List, Any, Optional

from leadgen.agents.question_agents import (
    DefaultQuestionsAgent,
    PersonalizedQuestionsAgent,
    KeywordGenerationAgent,
    ICPGenerationAgent
)
from leadgen.config.config_loader import ConfigLoader
from leadgen.entity.models import QuestionSession, Keyword, IdealCustomerProfile
from leadgen.utils.helpers import generate_id, save_session_data, format_questions_for_display


class LeadGenPipeline:
    """Pipeline for orchestrating the lead generation process"""
    
    def __init__(self):
        """Initialize the lead generation pipeline"""
        self.config_loader = ConfigLoader()
        self.default_agent = DefaultQuestionsAgent()
        self.personalized_agent = PersonalizedQuestionsAgent()
        self.keyword_agent = KeywordGenerationAgent()
        self.icp_agent = ICPGenerationAgent()
        
        # Create a new session
        self.session = QuestionSession(id=generate_id())
        
        # Load configuration
        self.config = self.config_loader.get_config()
        self.params = self.config_loader.get_params()
        
        # Create data directory if it doesn't exist
        data_dir = self.config.get("storage", {}).get("path", "./data")
        os.makedirs(data_dir, exist_ok=True)
        self.data_dir = data_dir
    
    def run_default_questions_stage(self) -> List[str]:
        """Run the default questions stage
        
        Returns:
            List of default questions
        """
        return self.default_agent.get_default_questions()
    
    def process_default_answers(self, questions_and_answers: Dict[str, str]) -> None:
        """Process the answers to the default questions
        
        Args:
            questions_and_answers: Dictionary mapping questions to answers
        """
        processed_qa = self.default_agent.process_answers(questions_and_answers)
        self.session.default_questions = processed_qa
    
    def run_personalized_questions_stage(self) -> List[str]:
        """Run the personalized questions stage
        
        Returns:
            List of personalized questions
        """
        if not self.session.default_questions:
            raise ValueError("Default questions stage must be completed first")
        
        num_questions = self.config.get("questions", {}).get("personalized_count", 10)
        return self.personalized_agent.generate_questions(
            initial_qa=self.session.default_questions,
            num_questions=num_questions
        )
    
    def process_personalized_answers(self, questions_and_answers: Dict[str, str]) -> None:
        """Process the answers to the personalized questions
        
        Args:
            questions_and_answers: Dictionary mapping questions to answers
        """
        processed_qa = self.personalized_agent.process_answers(questions_and_answers)
        self.session.personalized_questions = processed_qa
    
    def run_keyword_generation_stage(self) -> List[str]:
        """Run the keyword generation stage
        
        Returns:
            List of generated keywords
        """
        if not self.session.personalized_questions:
            raise ValueError("Personalized questions stage must be completed first")
        
        all_qa_data = {
            "Default Questions": self.session.default_questions,
            "Personalized Questions": self.session.personalized_questions
        }
        
        num_keywords = self.config.get("questions", {}).get("keyword_count", 10)
        keywords = self.keyword_agent.generate_keywords(
            all_qa_data=all_qa_data,
            num_keywords=num_keywords
        )
        
        # Convert to Keyword objects
        keyword_objects = [Keyword(text=k) for k in keywords]
        self.session.keywords = keyword_objects
        
        return keywords
    
    def run_icp_generation_stage(self) -> Dict[str, Any]:
        """Run the ICP generation stage
        
        Returns:
            Dictionary containing the Ideal Customer Profile
        """
        if not self.session.keywords:
            raise ValueError("Keyword generation stage must be completed first")
        
        all_qa_data = {
            "Default Questions": self.session.default_questions,
            "Personalized Questions": self.session.personalized_questions
        }
        
        keywords = [k.text for k in self.session.keywords]
        
        icp_data = self.icp_agent.generate_icp(
            all_qa_data=all_qa_data,
            keywords=keywords
        )
        
        # Set the ICP in the session
        self.session.ideal_customer_profile = IdealCustomerProfile(summary=icp_data.get("profile"))
        
        return icp_data
    
    def save_session(self) -> str:
        """Save the current session
        
        Returns:
            Path to the saved session file
        """
        return save_session_data(self.session.dict(), self.data_dir)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session
        
        Returns:
            Dictionary containing a summary of the session
        """
        return {
            "session_id": self.session.id,
            "created_at": self.session.created_at,
            "default_questions_count": len(self.session.default_questions),
            "personalized_questions_count": len(self.session.personalized_questions),
            "keywords_count": len(self.session.keywords),
            "has_icp": self.session.ideal_customer_profile is not None
        }