import React, { useState } from 'react';
import StreamSimulator from './StreamSimulator';

export default function LiveInterviewRoom({
  generatedQuestions,
  extractedKeywords,
  onSubmitAnswer,
  isScoring,
  sampleBenchmarks
}) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isStreaming, setIsStreaming] = useState(false);

  if (!generatedQuestions || generatedQuestions.length === 0) {
    return (
      <div className="card-box" style={{ textAlign: 'center', padding: '3rem' }}>
        <p style={{ color: 'var(--text-secondary)' }}>No interview questions loaded. Complete Step 1 first.</p>
      </div>
    );
  }

  const activeQuestion = generatedQuestions[currentIdx];
  const activeAnswer = answers[activeQuestion.id] || '';

  const handleTranscriptChange = (newText) => {
    setAnswers({
      ...answers,
      [activeQuestion.id]: newText
    });
  };

  const handleStartStream = () => {
    setIsStreaming(true);
  };

  const handleStopStream = () => {
    setIsStreaming(false);
  };

  const handleTriggerEvaluation = () => {
    if (!activeAnswer.trim()) {
      alert('Please provide or stream an answer before evaluating.');
      return;
    }
    onSubmitAnswer({
      question_id: activeQuestion.id,
      question_text: activeQuestion.question,
      candidate_answer: activeAnswer,
      expected_keywords: activeQuestion.expected_keywords
    });
  };

  return (
    <div className="card-box">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div>
          <span className="badge-tag tag-cyan" style={{ marginRight: '0.5rem' }}>
            {activeQuestion.category}
          </span>
          <span className="badge-tag tag-purple">
            Difficulty: {activeQuestion.difficulty}
          </span>
        </div>
        <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
          Question {currentIdx + 1} of {generatedQuestions.length}
        </div>
      </div>

      {/* Question Prompt */}
      <div
        style={{
          background: '#090d16',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-md)',
          padding: '1.25rem',
          marginBottom: '1rem'
        }}
      >
        <h3 style={{ fontSize: '1.15rem', fontWeight: 700, lineHeight: 1.5, color: '#f8fafc' }}>
          {activeQuestion.question}
        </h3>
        <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
          💡 <strong>Evaluation Rubric:</strong> {activeQuestion.evaluation_criteria}
        </p>

        {/* Expected Keywords Badges */}
        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginTop: '0.75rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Target Technical Keywords:</span>
          {activeQuestion.expected_keywords.map((kw, i) => (
            <span key={i} className="badge-tag tag-emerald" style={{ fontSize: '0.7rem' }}>
              {kw}
            </span>
          ))}
        </div>
      </div>

      {/* Audio / Text Streaming Interface */}
      <StreamSimulator
        isStreaming={isStreaming}
        onStartStream={handleStartStream}
        onStopStream={handleStopStream}
        currentTranscript={activeAnswer}
        onTranscriptChange={handleTranscriptChange}
        sampleBenchmarks={sampleBenchmarks}
      />

      {/* Actions Toolbar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.75rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            type="button"
            className="btn-ghost"
            disabled={currentIdx === 0}
            onClick={() => setCurrentIdx((prev) => Math.max(0, prev - 1))}
          >
            ← Previous Question
          </button>
          <button
            type="button"
            className="btn-ghost"
            disabled={currentIdx === generatedQuestions.length - 1}
            onClick={() => setCurrentIdx((prev) => Math.min(generatedQuestions.length - 1, prev + 1))}
          >
            Next Question →
          </button>
        </div>

        <button
          type="button"
          className="btn-cta"
          onClick={handleTriggerEvaluation}
          disabled={isScoring || !activeAnswer.trim()}
        >
          {isScoring ? 'Scoring Response...' : 'Evaluate Answer with NLP Models ⚡'}
        </button>
      </div>
    </div>
  );
}
