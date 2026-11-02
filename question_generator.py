"""Dynamic Question Generation Engine

DISCLAIMER & AI BEHAVIOR LABEL:
This module provides an automated question generation engine that parses dynamic job descriptions,
extracts key technologies/skills, and synthesizes role-aligned technical interview questions.
It uses an explainable NLP template-mapping approach:
- Domain vocabulary extraction from raw JD text.
- Skill-to-topic semantic mapping.
- Structured synthesis of expected keywords and scoring criteria.
This provides a reproducible and robust test harness that can also serve as a prompt orchestrator
for external generative LLMs.
"""

import re
from typing import List, Dict, Set
import schemas

COMMON_TECH_LEXICON = {
    "react", "react.js", "python", "fastapi", "flask", "django", "sql", "sqlite",
    "postgresql", "mysql", "power bi", "dax", "power query", "tableau", "docker",
    "kubernetes", "git", "ci/cd", "rest", "rest api", "graphql", "redis", "kafka",
    "tensorflow", "pytorch", "machine learning", "deep learning", "cnn", "nlp",
    "sentiment analysis", "data structures", "algorithms", "microservices"
}

QUESTION_TEMPLATES = [
    {
        "category": "System Architecture & Design",
        "difficulty": "Medium",
        "template": "In {role}, how would you architect a scalable system using {tech_primary} to handle asynchronous data processing while minimizing latency?",
        "criteria": "Evaluates architectural decomposition, decoupling, caching strategies, and bottleneck avoidance."
    },
    {
        "category": "Core Technical Principles",
        "difficulty": "Medium",
        "template": "Can you explain how you handle state management, data integrity, and error propagation when working with {tech_primary} and {tech_secondary}?",
        "criteria": "Assesses depth in framework internals, error boundaries, transactional integrity, and edge case handling."
    },
    {
        "category": "Performance & Optimization",
        "difficulty": "Hard",
        "template": "Suppose your application using {tech_primary} experiences sudden throughput degradation under load. What diagnostic steps and profiling tools would you employ?",
        "criteria": "Tests practical debugging methodology, indexing/query analysis, memory leak isolation, and benchmarking."
    },
    {
        "category": "Scenario & Problem Solving",
        "difficulty": "Medium",
        "template": "Describe an end-to-end project where you applied {tech_primary} to solve a concrete business problem. What technical tradeoffs did you navigate?",
        "criteria": "Measures engineering tradeoffs, technical rationale, communication clarity, and business impact."
    }
]


def extract_skills_from_jd(raw_text: str, preloaded_skills: List[str] = None) -> List[str]:
    """Extracts technical skills and key technologies from job description text."""
    found: Set[str] = set()
    
    if preloaded_skills:
        for s in preloaded_skills:
            found.add(s.strip())

    clean_text = raw_text.lower()
    for tech in COMMON_TECH_LEXICON:
        # Match as whole word/phrase
        pattern = r"\b" + re.escape(tech) + r"\b"
        if re.search(pattern, clean_text):
            found.add(tech.title() if len(tech) > 4 else tech.upper())

    if not found:
        # Fallback default competencies if text was minimal
        found = {"Python", "SQL", "REST APIs", "System Design"}

    return sorted(list(found))


def generate_interview_questions(jd_req: schemas.JobDescriptionRequest) -> schemas.GenerateQuestionsResponse:
    """Generates structured interview questions mapped dynamically to the supplied Job Description."""
    extracted_skills = extract_skills_from_jd(jd_req.raw_description, jd_req.required_skills)
    
    tech_primary = extracted_skills[0] if len(extracted_skills) > 0 else "Python"
    tech_secondary = extracted_skills[1] if len(extracted_skills) > 1 else "SQL"
    tech_tertiary = extracted_skills[2] if len(extracted_skills) > 2 else "REST APIs"

    questions: List[schemas.QuestionItem] = []

    for idx, tmpl in enumerate(QUESTION_TEMPLATES, start=1):
        formatted_question = tmpl["template"].format(
            role=jd_req.title,
            tech_primary=tech_primary,
            tech_secondary=tech_secondary,
            tech_tertiary=tech_tertiary
        )

        # Expected keywords include the extracted technologies + category-specific terms
        if tmpl["category"] == "System Architecture & Design":
            keywords = [tech_primary, "Latency", "Caching", "Throughput", "Scalability", "Asynchronous"]
        elif tmpl["category"] == "Core Technical Principles":
            keywords = [tech_primary, tech_secondary, "State", "Error Handling", "Validation", "Data Flow"]
        elif tmpl["category"] == "Performance & Optimization":
            keywords = [tech_primary, "Profiling", "Bottleneck", "Monitoring", "Concurrency", "Optimization"]
        else:
            keywords = [tech_primary, "Tradeoffs", "Implementation", "Requirements", "Testing"]

        questions.append(schemas.QuestionItem(
            id=f"q-{idx}",
            category=tmpl["category"],
            question=formatted_question,
            expected_keywords=keywords,
            evaluation_criteria=tmpl["criteria"],
            difficulty=tmpl["difficulty"]
        ))

    return schemas.GenerateQuestionsResponse(
        role_title=jd_req.title,
        total_questions=len(questions),
        extracted_keywords=extracted_skills,
        questions=questions
    )
