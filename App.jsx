import React, { useState, useEffect } from 'react';
import JobDescriptionInput from './components/JobDescriptionInput';
import LiveInterviewRoom from './components/LiveInterviewRoom';
import EvaluationScorecard from './components/EvaluationScorecard';

export default function App() {
  const [currentStep, setCurrentStep] = useState(1); // 1 = JD Setup, 2 = Live Interview, 3 = Scorecard
  const [sampleJobs, setSampleJobs] = useState([]);
  const [sampleBenchmarks, setSampleBenchmarks] = useState([]);

  // Active Session State
  const [jobDetails, setJobDetails] = useState(null);
  const [generatedQuestions, setGeneratedQuestions] = useState([]);
  const [extractedKeywords, setExtractedKeywords] = useState([]);
  const [evaluationResult, setEvaluationResult] = useState(null);

  // Loading States
  const [isLoadingQuestions, setIsLoadingQuestions] = useState(false);
  const [isScoring, setIsScoring] = useState(false);

  // Load preset benchmarks & jobs on mount
  useEffect(() => {
    fetch('/api/jobs/samples')
      .then((res) => res.json())
      .then((data) => setSampleJobs(data))
      .catch((err) => console.error('Failed to load sample jobs', err));

    fetch('/api/benchmarks/samples')
      .then((res) => res.json())
      .then((data) => setSampleBenchmarks(data))
      .catch((err) => console.error('Failed to load benchmark samples', err));
  }, []);

  const handleGenerateQuestions = async (jobPayload) => {
    setIsLoadingQuestions(true);
    setJobDetails(jobPayload);
    try {
      const response = await fetch('/api/questions/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jobPayload)
      });
      const data = await response.json();
      setGeneratedQuestions(data.questions || []);
      setExtractedKeywords(data.extracted_keywords || []);
      setCurrentStep(2);
    } catch (err) {
      console.error('Error generating questions', err);
      alert('Failed to generate interview questions. Verify backend service is running.');
    } finally {
      setIsLoadingQuestions(false);
    }
  };

  const handleSubmitAnswerForScoring = async (submission) => {
    setIsScoring(true);
    try {
      const response = await fetch('/api/evaluations/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...submission,
          job_context: jobDetails?.raw_description || ''
        })
      });
      const data = await response.json();
      setEvaluationResult(data);
      setCurrentStep(3);
    } catch (err) {
      console.error('Error scoring answer', err);
      alert('Failed to evaluate candidate response.');
    } finally {
      setIsScoring(false);
    }
  };

  return (
    <div>
      {/* Top Cockpit Navigation */}
      <header className="top-nav">
        <div className="brand-wrapper">
          <div className="ai-pill">AI INTERVIEW</div>
          <div>
            <h1 className="app-title">AI Mock Interview Test System</h1>
            <p className="app-subtitle">NLP Response Generation, Sentiment Profiling & Scoring</p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Status:</span>
          <span className="badge-tag tag-emerald">● Service Ready</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="main-layout">
        {/* Stepper Navigation Bar */}
        <div className="stepper-bar">
          <div
            className={`step-item ${currentStep === 1 ? 'active' : currentStep > 1 ? 'completed' : ''}`}
            onClick={() => setCurrentStep(1)}
          >
            <span>①</span> Target Job Description
          </div>
          <div
            className={`step-item ${currentStep === 2 ? 'active' : currentStep > 2 ? 'completed' : ''}`}
            onClick={() => generatedQuestions.length > 0 && setCurrentStep(2)}
          >
            <span>②</span> Live Assessment Session
          </div>
          <div
            className={`step-item ${currentStep === 3 ? 'active' : ''}`}
            onClick={() => evaluationResult && setCurrentStep(3)}
          >
            <span>③</span> Evaluation Scorecard
          </div>
        </div>

        {/* View Switching */}
        {currentStep === 1 && (
          <JobDescriptionInput
            sampleJobs={sampleJobs}
            onGenerateQuestions={handleGenerateQuestions}
            isLoading={isLoadingQuestions}
          />
        )}

        {currentStep === 2 && (
          <LiveInterviewRoom
            generatedQuestions={generatedQuestions}
            extractedKeywords={extractedKeywords}
            onSubmitAnswer={handleSubmitAnswerForScoring}
            isScoring={isScoring}
            sampleBenchmarks={sampleBenchmarks}
          />
        )}

        {currentStep === 3 && (
          <EvaluationScorecard
            evaluation={evaluationResult}
            onBackToInterview={() => setCurrentStep(2)}
            onRetest={() => setCurrentStep(2)}
          />
        )}
      </main>
    </div>
  );
}
