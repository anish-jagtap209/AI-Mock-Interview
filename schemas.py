from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    company: Optional[str] = "Target Enterprise"
    experience_level: Optional[str] = "Entry to Mid Level"
    required_skills: List[str] = Field(default_factory=list)
    raw_description: str = Field(..., min_length=10)


class QuestionItem(BaseModel):
    id: str
    category: str  # System Architecture, Coding & Data Structures, Problem Solving, Behavioral
    question: str
    expected_keywords: List[str]
    evaluation_criteria: str
    difficulty: str  # Easy, Medium, Hard


class GenerateQuestionsResponse(BaseModel):
    role_title: str
    total_questions: int
    extracted_keywords: List[str]
    questions: List[QuestionItem]


class AnswerSubmission(BaseModel):
    question_id: str
    question_text: str
    candidate_answer: str
    expected_keywords: List[str] = Field(default_factory=list)
    job_context: Optional[str] = ""


class MetricScore(BaseModel):
    score: float = Field(..., ge=0.0, le=100.0)
    rating: str  # "Needs Improvement", "Proficient", "Exceptional"
    feedback: str


class EvaluationResult(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0)
    relevance: MetricScore
    technical_clarity: MetricScore
    keyword_coverage: MetricScore
    matched_keywords: List[str]
    missing_keywords: List[str]
    filler_word_ratio: float
    sentiment_analysis: Dict[str, Any]
    detailed_feedback: List[str]


class StreamChunk(BaseModel):
    session_id: str
    sequence_num: int
    token: str
    is_final: bool
    mock_audio_amplitude: Optional[float] = 0.5
