#!/usr/bin/env python
# Main entry point for the leadgen application

import os
import argparse
from typing import Dict, List, Any

from leadgen.pipeline.lead_gen_pipeline import LeadGenPipeline
from leadgen.utils.helpers import format_questions_for_display


def get_user_answers(questions: List[str]) -> Dict[str, str]:
    """Get answers from the user for a list of questions
    
    Args:
        questions: List of questions to ask
        
    Returns:
        Dictionary mapping questions to answers
    """
    answers = {}
    print("\nPlease answer the following questions:\n")
    
    for i, question in enumerate(questions):
        print(f"Question {i+1}: {question}")
        answer = input("Your answer: ")
        answers[question] = answer
        print()  # Add a blank line for readability
    
    return answers


def run_default_questions_stage(pipeline: LeadGenPipeline) -> None:
    """Run the default questions stage
    
    Args:
        pipeline: The lead generation pipeline
    """
    print("\n=== Default Questions Stage ===")
    questions = pipeline.run_default_questions_stage()
    answers = get_user_answers(questions)
    pipeline.process_default_answers(answers)
    print("Default questions stage completed.")


def run_personalized_questions_stage(pipeline: LeadGenPipeline) -> None:
    """Run the personalized questions stage
    
    Args:
        pipeline: The lead generation pipeline
    """
    print("\n=== Personalized Questions Stage ===")
    print("Generating personalized questions based on your initial answers...")
    questions = pipeline.run_personalized_questions_stage()
    answers = get_user_answers(questions)
    pipeline.process_personalized_answers(answers)
    print("Personalized questions stage completed.")


def run_keyword_generation_stage(pipeline: LeadGenPipeline) -> None:
    """Run the keyword generation stage
    
    Args:
        pipeline: The lead generation pipeline
    """
    print("\n=== Keyword Generation Stage ===")
    print("Generating keywords based on your answers...")
    keywords = pipeline.run_keyword_generation_stage()
    
    print("\nGenerated Keywords:")
    for i, keyword in enumerate(keywords):
        print(f"{i+1}. {keyword}")
    
    print("\nKeyword generation stage completed.")


def run_icp_generation_stage(pipeline: LeadGenPipeline) -> None:
    """Run the ICP generation stage
    
    Args:
        pipeline: The lead generation pipeline
    """
    print("\n=== Ideal Customer Profile Generation Stage ===")
    print("Generating Ideal Customer Profile based on all collected data...")
    icp_data = pipeline.run_icp_generation_stage()
    
    print("\nIdeal Customer Profile:")
    print(icp_data.get("profile", "No profile generated"))
    
    print("\nICP generation stage completed.")


def run_full_pipeline() -> None:
    """Run the full lead generation pipeline"""
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Please set it before running the application.")
        print("Example: export GROQ_API_KEY='your-api-key'")
        return
    
    print("\n=== Lead Generation Pipeline ===")
    print("This application will guide you through a multi-step process to generate an Ideal Customer Profile.")
    
    # Initialize the pipeline
    pipeline = LeadGenPipeline()
    
    try:
        # Run each stage
        run_default_questions_stage(pipeline)
        run_personalized_questions_stage(pipeline)
        run_keyword_generation_stage(pipeline)
        run_icp_generation_stage(pipeline)
        
        # Save the session
        session_file = pipeline.save_session()
        print(f"\nSession data saved to: {session_file}")
        
        # Show summary
        print("\n=== Session Summary ===")
        summary = pipeline.get_session_summary()
        print(f"Session ID: {summary['session_id']}")
        print(f"Created at: {summary['created_at']}")
        print(f"Default questions answered: {summary['default_questions_count']}")
        print(f"Personalized questions answered: {summary['personalized_questions_count']}")
        print(f"Keywords generated: {summary['keywords_count']}")
        print(f"Ideal Customer Profile generated: {'Yes' if summary['has_icp'] else 'No'}")
        
        print("\nThank you for using the Lead Generation application!")
    
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("The pipeline was interrupted. Saving current progress...")
        session_file = pipeline.save_session()
        print(f"Session data saved to: {session_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Lead Generation Application")
    parser.add_argument("--version", action="store_true", help="Show version information")
    
    args = parser.parse_args()
    
    if args.version:
        from leadgen import __version__
        print(f"Lead Generation Application v{__version__}")
        return
    
    run_full_pipeline()


if __name__ == "__main__":
    main()