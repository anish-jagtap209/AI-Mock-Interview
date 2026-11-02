import React from 'react';

export default function EvaluationScorecard({ evaluation, onBackToInterview, onRetest }) {
  if (!evaluation) return null;

  const {
    overall_score = 0,
    relevance = {},
    technical_clarity = {},
    keyword_coverage = {},
    matched_keywords = [],
    missing_keywords = [],
    filler_word_ratio = 0,
    sentiment_analysis = {},
    detailed_feedback = []
  } = evaluation;

  const getScoreColor = (val) => {
    if (val >= 80) return 'var(--accent-emerald)';
    if (val >= 60) return 'var(--accent-amber)';
    return 'var(--accent-rose)';
  };

  return (
    <div className="card-box">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        <div>
          <h2 className="box-title">Step 3: Multi-Dimensional Evaluation Scorecard</h2>
          <p className="box-desc" style={{ margin: 0 }}>
            Automated NLP scoring breakdown based on answer relevance, technical clarity, keyword density, and sentiment.
          </p>
        </div>
        <button type="button" className="btn-ghost" onClick={onBackToInterview}>
          ← Back to Interview Room
        </button>
      </div>

      {/* Main Score Tiles */}
      <div className="score-grid">
        {/* Overall Score */}
        <div className="score-tile" style={{ borderLeft: `4px solid ${getScoreColor(overall_score)}` }}>
          <span className="input-label">Composite Overall Score</span>
          <div className="score-num" style={{ color: getScoreColor(overall_score) }}>
            {overall_score}
            <span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}> / 100</span>
          </div>
          <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            Weighted: 35% Relevance, 35% Keywords, 30% Clarity
          </p>
        </div>

        {/* Answer Relevance */}
        <div className="score-tile">
          <span className="input-label">Answer Relevance</span>
          <div className="score-num" style={{ color: getScoreColor(relevance.score || 0) }}>
            {relevance.score || 0}%
          </div>
          <span className={`badge-tag ${relevance.rating === 'Exceptional' ? 'tag-emerald' : relevance.rating === 'Proficient' ? 'tag-amber' : 'tag-rose'}`} style={{ marginTop: '0.35rem' }}>
            {relevance.rating}
          </span>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            {relevance.feedback}
          </p>
        </div>

        {/* Technical Clarity */}
        <div className="score-tile">
          <span className="input-label">Technical Clarity</span>
          <div className="score-num" style={{ color: getScoreColor(technical_clarity.score || 0) }}>
            {technical_clarity.score || 0}%
          </div>
          <span className={`badge-tag ${technical_clarity.rating === 'Exceptional' ? 'tag-emerald' : 'tag-amber'}`} style={{ marginTop: '0.35rem' }}>
            {filler_word_ratio}% filler density
          </span>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            {technical_clarity.feedback}
          </p>
        </div>

        {/* Keyword Coverage */}
        <div className="score-tile">
          <span className="input-label">Keyword Coverage</span>
          <div className="score-num" style={{ color: getScoreColor(keyword_coverage.score || 0) }}>
            {keyword_coverage.score || 0}%
          </div>
          <span className="badge-tag tag-cyan" style={{ marginTop: '0.35rem' }}>
            {matched_keywords.length} matched terms
          </span>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            {keyword_coverage.feedback}
          </p>
        </div>
      </div>

      {/* Technical Vocabulary Breakdown */}
      <div style={{ marginTop: '1.5rem', background: '#090d16', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '1.25rem' }}>
        <h4 style={{ fontSize: '0.9375rem', fontWeight: 600, marginBottom: '0.75rem' }}>
          Technical Vocabulary Audit
        </h4>
        
        <div style={{ marginBottom: '0.75rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.35rem' }}>
            Demonstrated Keywords ({matched_keywords.length}):
          </span>
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {matched_keywords.length === 0 ? (
              <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>None detected</span>
            ) : (
              matched_keywords.map((kw, i) => (
                <span key={i} className="badge-tag tag-emerald">✓ {kw}</span>
              ))
            )}
          </div>
        </div>

        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.35rem' }}>
            Recommended Missing Keywords ({missing_keywords.length}):
          </span>
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {missing_keywords.length === 0 ? (
              <span style={{ fontSize: '0.8125rem', color: 'var(--accent-emerald)' }}>All target keywords covered!</span>
            ) : (
              missing_keywords.map((kw, i) => (
                <span key={i} className="badge-tag tag-rose">✗ {kw}</span>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Sentiment & Tone Profiling */}
      {sentiment_analysis && (
        <div style={{ marginTop: '1.25rem', background: '#090d16', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '1.25rem' }}>
          <h4 style={{ fontSize: '0.9375rem', fontWeight: 600, marginBottom: '0.75rem' }}>
            Sentiment & Candidate Tone Analysis
          </h4>
          <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Tone Classification:</span>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '0.2rem' }}>
                {sentiment_analysis.dominant_tone || 'Professional'}
              </div>
            </div>
            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Confidence Metric:</span>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--accent-emerald)', marginTop: '0.2rem' }}>
                {sentiment_analysis.confidence_score || 0}%
              </div>
            </div>
            <div style={{ flex: 1, minWidth: '220px' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Tone Spectrum:</span>
              <div style={{ height: '8px', background: '#1e293b', borderRadius: '4px', overflow: 'hidden', display: 'flex', marginTop: '0.4rem' }}>
                <div style={{ width: `${sentiment_analysis.tone_breakdown?.assertive || 0}%`, background: '#10b981' }} title="Assertive" />
                <div style={{ width: `${sentiment_analysis.tone_breakdown?.neutral || 0}%`, background: '#3b82f6' }} title="Neutral" />
                <div style={{ width: `${sentiment_analysis.tone_breakdown?.hesitant || 0}%`, background: '#f43f5e' }} title="Hesitant" />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Actionable Feedback List */}
      <div style={{ marginTop: '1.25rem', background: '#090d16', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '1.25rem' }}>
        <h4 style={{ fontSize: '0.9375rem', fontWeight: 600, marginBottom: '0.75rem' }}>
          AI Coaching Recommendations
        </h4>
        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {detailed_feedback.map((item, idx) => (
            <li key={idx} style={{ fontSize: '0.8125rem', color: '#cbd5e1', display: 'flex', gap: '0.5rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
        <button type="button" className="btn-ghost" onClick={onRetest}>
          Try Another Response
        </button>
        <button type="button" className="btn-cta" onClick={onBackToInterview}>
          Proceed to Next Question →
        </button>
      </div>
    </div>
  );
}
