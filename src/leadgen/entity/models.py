# Data models for the leadgen application

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Question(BaseModel):
    """Model representing a question"""
    id: str
    text: str
    stage: str
    order: int


class Answer(BaseModel):
    """Model representing an answer to a question"""
    question_id: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)


class Keyword(BaseModel):
    """Model representing a generated keyword"""
    text: str
    relevance_score: Optional[float] = None
    type: Optional[str] = None


class Demographics(BaseModel):
    """Demographic information for the ideal customer profile"""
    age_range: Optional[str] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    income_level: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)


class Firmographics(BaseModel):
    """Firmographic information for B2B ideal customer profiles"""
    industry: Optional[str] = None
    company_size: Optional[str] = None
    revenue: Optional[str] = None
    location: Optional[str] = None
    maturity: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)


class Psychographics(BaseModel):
    """Psychographic information for the ideal customer profile"""
    values: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    attitudes: List[str] = Field(default_factory=list)
    lifestyle: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)


class Behaviors(BaseModel):
    """Behavioral patterns of the ideal customer"""
    purchasing_habits: List[str] = Field(default_factory=list)
    brand_interactions: List[str] = Field(default_factory=list)
    online_behavior: List[str] = Field(default_factory=list)
    decision_making: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)


class BuyingPatterns(BaseModel):
    """Buying patterns and preferences of the ideal customer"""
    purchase_frequency: Optional[str] = None
    average_order_value: Optional[str] = None
    decision_factors: List[str] = Field(default_factory=list)
    preferred_channels: List[str] = Field(default_factory=list)
    additional_info: Dict[str, Any] = Field(default_factory=dict)


class IdealCustomerProfile(BaseModel):
    """Comprehensive ideal customer profile"""
    demographics: Optional[Demographics] = Field(default_factory=Demographics)
    firmographics: Optional[Firmographics] = Field(default_factory=Firmographics)
    psychographics: Optional[Psychographics] = Field(default_factory=Psychographics)
    behaviors: Optional[Behaviors] = Field(default_factory=Behaviors)
    pain_points: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    buying_patterns: Optional[BuyingPatterns] = Field(default_factory=BuyingPatterns)
    summary: Optional[str] = None


class QuestionSession(BaseModel):
    """Model representing a complete question session"""
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    default_questions: Dict[str, str] = Field(default_factory=dict)
    personalized_questions: Dict[str, str] = Field(default_factory=dict)
    keywords: List[Keyword] = Field(default_factory=list)
    ideal_customer_profile: Optional[IdealCustomerProfile] = None