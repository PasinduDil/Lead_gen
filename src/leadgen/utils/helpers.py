# Helper utilities for the leadgen application

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional


def generate_id() -> str:
    """Generate a unique ID
    
    Returns:
        A unique ID string
    """
    return str(uuid.uuid4())


def save_session_data(session_data: Dict[str, Any], directory: str = "data") -> str:
    """Save session data to a JSON file
    
    Args:
        session_data: The session data to save
        directory: Directory to save the data in
        
    Returns:
        Path to the saved file
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Generate a filename based on timestamp and session ID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = session_data.get("id", generate_id())
    filename = f"{timestamp}_{session_id}.json"
    file_path = os.path.join(directory, filename)
    
    # Convert datetime objects to strings
    session_data_copy = json.loads(json.dumps(session_data, default=str))
    
    # Save the data
    with open(file_path, "w") as file:
        json.dump(session_data_copy, file, indent=2)
    
    return file_path


def load_session_data(file_path: str) -> Dict[str, Any]:
    """Load session data from a JSON file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the session data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Session data file not found: {file_path}")
    
    with open(file_path, "r") as file:
        return json.load(file)


def format_questions_for_display(questions: List[str]) -> str:
    """Format a list of questions for display
    
    Args:
        questions: List of question strings
        
    Returns:
        Formatted string with numbered questions
    """
    return "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])


def format_qa_for_prompt(questions_and_answers: Dict[str, str]) -> str:
    """Format questions and answers for use in a prompt
    
    Args:
        questions_and_answers: Dictionary mapping questions to answers
        
    Returns:
        Formatted string with questions and answers
    """
    return "\n\n".join([f"Q: {q}\nA: {a}" for q, a in questions_and_answers.items()])


def extract_keywords_from_text(text: str) -> List[str]:
    """Extract keywords from text (simple implementation)
    
    Args:
        text: Text to extract keywords from
        
    Returns:
        List of extracted keywords
    """
    # This is a simple implementation that just splits by commas or newlines
    # In a real application, you might use a more sophisticated approach
    if not text:
        return []
    
    # Try to handle different formats
    if "," in text:
        keywords = [k.strip() for k in text.split(",")]
    elif "\n" in text:
        keywords = [k.strip() for k in text.split("\n")]
    else:
        keywords = [text.strip()]
    
    # Remove empty strings
    return [k for k in keywords if k]