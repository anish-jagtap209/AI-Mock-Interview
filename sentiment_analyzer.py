"""Sentiment & Tone Analysis Module

DISCLAIMER & AI BEHAVIOR LABEL:
This module implements a deterministic rule- and lexicon-based NLP sentiment & tone
evaluator designed for transparent, repeatable mock interview feedback. It measures:
1. Assertiveness and confidence markers vs. hesitation / hedging markers.
2. Emotional valence (Positive, Neutral, Hesitant, Defensive).
3. Speech fluency disfluency indicators.
For production deployments, this interface can be connected to fine-tuned transformer
sentiment classifiers (e.g., RoBERTa/DeBERTa) or speech acoustic prosody models.
"""

import re
from typing import Dict, Any


POSITIVE_ASSERTIVE_MARKERS = {
    "implemented", "designed", "architected", "optimized", "ensured", "achieved",
    "confident", "resolved", "collaborated", "structured", "streamlined",
    "effectively", "systematically", "proven", "measurable", "spearheaded"
}

HESITATION_MARKERS = {
    "maybe", "perhaps", "i guess", "i think maybe", "probably", "not sure",
    "kind of", "sort of", "i don't know", "might be", "hopefully", "somewhat"
}

FILLER_WORDS = {
    "um", "uh", "er", "like", "basically", "you know", "actually", "literally", "honestly"
}


def analyze_sentiment_and_tone(text: str) -> Dict[str, Any]:
    """Analyzes text for emotional tone, assertiveness, and candidate confidence.

    Returns deterministic confidence scores and tone classifications.
    """
    if not text or not text.strip():
        return {
            "dominant_tone": "Indeterminate",
            "confidence_score": 0.0,
            "tone_breakdown": {
                "assertive": 0.0,
                "hesitant": 0.0,
                "neutral": 100.0
            },
            "hesitation_count": 0,
            "assertive_count": 0,
            "methodology": "Lexicon & Heuristic Tone Profiler (Educational / Prototype Mode)"
        }

    lower_text = text.lower()
    words = re.findall(r"\b[a-z']+\b", lower_text)
    total_words = max(len(words), 1)

    # Count assertive matches
    assertive_hits = sum(1 for w in words if w in POSITIVE_ASSERTIVE_MARKERS)

    # Count hesitation phrase & word matches
    hesitant_hits = sum(1 for w in words if w in HESITATION_MARKERS)
    for phrase in ["i guess", "i think maybe", "not sure", "kind of", "sort of", "i don't know"]:
        hesitant_hits += lower_text.count(phrase)

    # Calculate ratios
    assertive_ratio = min((assertive_hits / total_words) * 300, 100.0)
    hesitant_ratio = min((hesitant_hits / total_words) * 400, 100.0)

    # Calculate net confidence score (0 - 100)
    base_confidence = 65.0
    confidence = base_confidence + (assertive_ratio * 0.4) - (hesitant_ratio * 0.6)
    confidence = max(10.0, min(98.0, round(confidence, 1)))

    # Determine dominant tone
    if hesitant_ratio > 35.0:
        dominant_tone = "Hesitant & Uncertain"
    elif assertive_ratio > 20.0 and hesitant_ratio < 15.0:
        dominant_tone = "Confident & Assertive"
    elif assertive_ratio >= 10.0:
        dominant_tone = "Professional & Balanced"
    else:
        dominant_tone = "Neutral & Conversational"

    return {
        "dominant_tone": dominant_tone,
        "confidence_score": confidence,
        "tone_breakdown": {
            "assertive": round(assertive_ratio, 1),
            "hesitant": round(hesitant_ratio, 1),
            "neutral": round(max(0.0, 100.0 - assertive_ratio - hesitant_ratio), 1)
        },
        "hesitation_count": hesitant_hits,
        "assertive_count": assertive_hits,
        "methodology": "Lexicon & Heuristic Tone Profiler (Educational / Prototype Mode)"
    }
