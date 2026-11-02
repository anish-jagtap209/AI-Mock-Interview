import React, { useState } from 'react';

export default function JobDescriptionInput({
  sampleJobs,
  onSelectSample,
  onGenerateQuestions,
  isLoading
}) {
  const [title, setTitle] = useState('Full-Stack Software Engineer (React & Python)');
  const [skills, setSkills] = useState('React.js, Python, FastAPI, SQL, REST APIs, Git');
  const [description, setDescription] = useState(
    'Looking for a full-stack engineer to build scalable RESTful microservices in Python (FastAPI) and responsive frontend dashboards in React.js. Duties include relational database modeling in SQL and API latency optimization.'
  );

  const handleApplyPreset = (job) => {
    setTitle(job.title);
    setSkills(job.required_skills.join(', '));
    setDescription(job.description);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const skillsList = skills.split(',').map((s) => s.strip ? s.strip() : s.trim()).filter(Boolean);
    onGenerateQuestions({
      title,
      required_skills: skillsList,
      raw_description: description
    });
  };

  return (
    <div className="card-box">
      <h2 className="box-title">Step 1: Configure Target Job Description</h2>
      <p className="box-desc">
        Input the target engineering or analytics position. The NLP engine will parse the description,
        extract technical competencies, and generate customized interview prompts.
      </p>

      {/* Preset Pickers */}
      {sampleJobs && sampleJobs.length > 0 && (
        <div style={{ marginBottom: '1.5rem' }}>
          <span className="input-label">Load Role Benchmark Preset:</span>
          <div style={{ display: 'flex', gap: '0.6rem', flexWrap: 'wrap', marginTop: '0.35rem' }}>
            {sampleJobs.map((job) => (
              <button
                key={job.id}
                type="button"
                className="btn-ghost"
                onClick={() => handleApplyPreset(job)}
              >
                {job.title}
              </button>
            ))}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <label className="input-label">Target Role Title</label>
            <input
              type="text"
              className="text-field"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="input-label">Key Required Technologies (Comma-Separated)</label>
            <input
              type="text"
              className="text-field"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
            />
          </div>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label className="input-label">Job Description / Requirements Text</label>
          <textarea
            className="textarea-field"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Paste raw job description text here..."
            required
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="btn-cta" disabled={isLoading}>
            {isLoading ? 'Analyzing JD & Generating Questions...' : 'Generate Interview Questions →'}
          </button>
        </div>
      </form>
    </div>
  );
}
