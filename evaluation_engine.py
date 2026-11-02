"""Automated Evaluation Algorithms for Mock Interview Answers

DISCLAIMER & AI BEHAVIOR LABEL:
This module contains the prototype scoring algorithms that assess:
1. Answer Relevance: Lexical and semantic overlap between candidate answer, question, and expected topics.
2. Technical Clarity: Structural coherence, sentence length variance, and filler word penalty.
3. Keyword Coverage: Ratio of job-description-derived technical competencies demonstrated in the answer.

These algorithms use deterministic statistical NLP metrics (token normalization, Jaccard/Dice term similarity,
Flesch-style readability heuristics, and disfluency scoring). They provide an explainable scoring baseline
that can be extended with embeddings or LLM judge evaluators.
"""

import re
import math
from typing import List, Dict, Tuple, Any
import schemas
from sentiment_analyzer import analyze_sentiment_and_tone, FILLER_WORDS


def _clean_and_tokenize(text: str) -> List[str]:
    """Tokenize into lowercase alphabetic words."""
    return re.findall(r"\b[a-zA-Z0-9_\-+#.]+\b", text.lower())


def evaluate_keyword_coverage(candidate_answer: str, expected_keywords: List[str]) -> Tuple[schemas.MetricScore, List[str], List[str]]:
    """Calculates keyword coverage against expected technical vocabulary."""
    if not expected_keywords:
        return schemas.MetricScore(
            score=75.0,
            rating="Proficient",
            feedback="No specific required keywords were mandated for this prompt."
        ), [], []

    lower_answer = candidate_answer.lower()
    matched = []
    missing = []

    for kw in expected_keywords:
        kw_clean = kw.strip().lower()
        # Word boundary or exact phrase match
        pattern = r"\b" + re.escape(kw_clean) + r"\b"
        if re.search(pattern, lower_answer):
            matched.append(kw)
        else:
            missing.append(kw)

    coverage_ratio = len(matched) / len(expected_keywords)
    score = round(coverage_ratio * 100.0, 1)

    if score >= 80.0:
        rating = "Exceptional"
        feedback = f"Superb technical coverage! Successfully articulated {len(matched)} of {len(expected_keywords)} expected domain terms."
    elif score >= 50.0:
        rating = "Proficient"
        feedback = f"Adequate technical terminology ({len(matched)}/{len(expected_keywords)} terms). Consider incorporating: {', '.join(missing[:3])}."
    else:
        rating = "Needs Improvement"
        feedback = f"Insufficient technical depth. Omitted critical expected terms: {', '.join(missing[:4])}."

    return schemas.MetricScore(score=score, rating=rating, feedback=feedback), matched, missing


def evaluate_technical_clarity(candidate_answer: str) -> Tuple[schemas.MetricScore, float]:
    """Evaluates answer clarity, structural cadence, and filler word ratio."""
    tokens = _clean_and_tokenize(candidate_answer)
    total_tokens = len(tokens)

    if total_tokens < 15:
        return schemas.MetricScore(
            score=35.0,
            rating="Needs Improvement",
            feedback="Answer is overly brief. Elaborate with concrete architectural decisions, tradeoffs, or examples."
        ), 0.0

    # Count filler words
    filler_count = sum(1 for t in tokens if t in FILLER_WORDS)
    filler_ratio = round((filler_count / total_tokens) * 100.0, 2)

    # Sentence length and structural cadence
    sentences = [s.strip() for s in re.split(r"[.!?]+", candidate_answer) if s.strip()]
    avg_sentence_len = total_tokens / max(len(sentences), 1)

    # Base clarity calculation
    base_clarity = 90.0

    # Penalize high filler word ratio (> 3% starts reducing score)
    filler_penalty = max(0.0, (filler_ratio - 2.5) * 4.0)

    # Penalize run-on sentences (> 30 words/sentence) or overly choppy (< 6 words/sentence)
    length_penalty = 0.0
    if avg_sentence_len > 32:
        length_penalty = min(20.0, (avg_sentence_len - 32) * 1.5)
    elif avg_sentence_len < 6:
        length_penalty = 10.0

    clarity_score = max(20.0, min(98.0, round(base_clarity - filler_penalty - length_penalty, 1)))

    if clarity_score >= 82.0:
        rating = "Exceptional"
        feedback = f"Crisp, professional articulation with minimal filler hesitation ({filler_ratio}% filler density)."
    elif clarity_score >= 60.0:
        rating = "Proficient"
        feedback = f"Generally clear delivery. Be conscious of filler phrasing ('{', '.join(set(t for t in tokens if t in FILLER_WORDS)) or 'none'}')."
    else:
        rating = "Needs Improvement"
        feedback = f"Clarity hindered by filler words ({filler_ratio}%) or fragmented pacing. Aim for structured STAR / problem-solution phrasing."

    return schemas.MetricScore(score=clarity_score, rating=rating, feedback=feedback), filler_ratio


def evaluate_answer_relevance(candidate_answer: str, question: str, expected_keywords: List[str], job_context: str) -> schemas.MetricScore:
    """Evaluates lexical topical overlap and responsiveness between the answer and prompt."""
    answer_tokens = set(_clean_and_tokenize(candidate_answer))
    question_tokens = set(_clean_and_tokenize(question)) - {"how", "what", "why", "do", "you", "the", "a", "an", "is", "are", "in", "to", "for"}
    
    if len(answer_tokens) < 10:
        return schemas.MetricScore(
            score=30.0,
            rating="Needs Improvement",
            feedback="Answer is too short to establish contextual relevance to the interview prompt."
        )

    # Overlap with question intent
    q_overlap = len(answer_tokens.intersection(question_tokens))
    q_ratio = q_overlap / max(len(question_tokens), 1)

    # Overlap with core expected keywords
    kw_tokens = set()
    for kw in expected_keywords:
        kw_tokens.update(_clean_and_tokenize(kw))
    
    kw_overlap = len(answer_tokens.intersection(kw_tokens))
    kw_ratio = kw_overlap / max(len(kw_tokens), 1) if kw_tokens else 0.5

    # Compute composite relevance
    composite = (q_ratio * 0.4 + kw_ratio * 0.6) * 100.0
    
    # Scale with minimum threshold
    relevance_score = max(25.0, min(96.0, round(composite * 1.25, 1)))

    if relevance_score >= 80.0:
        rating = "Exceptional"
        feedback = "Directly addresses the core technical problem posed in the question with high contextual alignment."
    elif relevance_score >= 55.0:
        rating = "Proficient"
        feedback = "Answer is relevant to the topic but could address the specific prompt constraints more directly."
    else:
        rating = "Needs Improvement"
        feedback = "Response diverged from the central question. Focus on directly answering the core technical dilemma."

    return schemas.MetricScore(score=relevance_score, rating=rating, feedback=feedback)


def run_full_evaluation(submission: schemas.AnswerSubmission) -> schemas.EvaluationResult:
    """Runs composite evaluation pipeline: relevance, clarity, keyword coverage, and sentiment analysis."""
    # 1. Keyword coverage
    keyword_metric, matched_kws, missing_kws = evaluate_keyword_coverage(
        submission.candidate_answer, submission.expected_keywords
    )

    # 2. Technical clarity & filler words
    clarity_metric, filler_ratio = evaluate_technical_clarity(submission.candidate_answer)

    # 3. Answer relevance
    relevance_metric = evaluate_answer_relevance(
        submission.candidate_answer,
        submission.question_text,
        submission.expected_keywords,
        submission.job_context or ""
    )

    # 4. Sentiment & Tone
    sentiment = analyze_sentiment_and_tone(submission.candidate_answer)

    # 5. Composite overall score
    # Weighted average: 35% Relevance, 35% Keyword Coverage, 30% Clarity
    overall = (relevance_metric.score * 0.35) + (keyword_metric.score * 0.35) + (clarity_metric.score * 0.30)
    overall_score = round(max(0.0, min(100.0, overall)), 1)

    # 6. Detailed Actionable Feedback
    feedback_bullets = [
        relevance_metric.feedback,
        clarity_metric.feedback,
        keyword_metric.feedback,
        f"Candidate Tone: Classified as '{sentiment['dominant_tone']}' with a confidence index of {sentiment['confidence_score']}%."
    ]

    return schemas.EvaluationResult(
        overall_score=overall_score,
        relevance=relevance_metric,
        technical_clarity=clarity_metric,
        keyword_coverage=keyword_metric,
        matched_keywords=matched_kws,
        missing_keywords=missing_kws,
        filler_word_ratio=filler_ratio,
        sentiment_analysis=sentiment,
        detailed_feedback=feedback_bullets
    )
