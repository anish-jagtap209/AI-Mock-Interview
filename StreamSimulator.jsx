import React, { useState, useEffect } from 'react';

export default function StreamSimulator({
  isStreaming,
  onStartStream,
  onStopStream,
  onAppendToken,
  currentTranscript,
  onTranscriptChange,
  sampleBenchmarks
}) {
  const [amplitudeBars, setAmplitudeBars] = useState([20, 15, 35, 45, 10, 25, 40, 30, 20, 15]);

  // Audio waveform animation effect when streaming
  useEffect(() => {
    let interval;
    if (isStreaming) {
      interval = setInterval(() => {
        setAmplitudeBars(
          Array.from({ length: 16 }, () => Math.floor(Math.random() * 38) + 8)
        );
      }, 120);
    } else {
      setAmplitudeBars(Array.from({ length: 16 }, () => 6));
    }
    return () => clearInterval(interval);
  }, [isStreaming]);

  const handleSimulateStrongResponse = () => {
    if (sampleBenchmarks && sampleBenchmarks.length > 0) {
      onTranscriptChange(sampleBenchmarks[0].sample_strong_response);
    }
  };

  const handleSimulateWeakResponse = () => {
    if (sampleBenchmarks && sampleBenchmarks.length > 1) {
      onTranscriptChange(sampleBenchmarks[1].sample_weak_response);
    }
  };

  return (
    <div style={{ marginTop: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
        <span className="input-label" style={{ margin: 0 }}>
          Audio / Text Stream Buffer {isStreaming && <span className="badge-tag tag-rose">● LIVE STREAMING</span>}
        </span>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
            onClick={handleSimulateStrongResponse}
          >
            Load Benchmark Strong Response
          </button>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
            onClick={handleSimulateWeakResponse}
          >
            Load Benchmark Weak Response
          </button>
        </div>
      </div>

      {/* Audio Waveform Display */}
      <div className="waveform-container">
        {amplitudeBars.map((height, i) => (
          <div
            key={i}
            className="wave-bar"
            style={{
              height: `${height}px`,
              backgroundColor: isStreaming ? '#06b6d4' : '#334155'
            }}
          />
        ))}
        <span style={{ fontSize: '0.75rem', color: isStreaming ? 'var(--accent-cyan)' : 'var(--text-muted)', marginLeft: '1rem' }}>
          {isStreaming ? 'Stream Active: Ingesting speech tokens...' : 'Microphone idle (Click below or type directly)'}
        </span>
      </div>

      {/* Live Transcript Textarea */}
      <div style={{ marginTop: '0.75rem' }}>
        <textarea
          className="textarea-field"
          style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.85rem' }}
          placeholder="Speak or type your candidate response here..."
          value={currentTranscript}
          onChange={(e) => onTranscriptChange(e.target.value)}
        />
      </div>

      {/* Stream Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.75rem' }}>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Word Count: {currentTranscript.trim() ? currentTranscript.trim().split(/\s+/).length : 0} words
        </span>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          {!isStreaming ? (
            <button
              type="button"
              className="btn-ghost"
              style={{ color: 'var(--accent-cyan)', borderColor: 'var(--accent-cyan)' }}
              onClick={onStartStream}
            >
              🎙️ Start Live Stream Ingestion
            </button>
          ) : (
            <button
              type="button"
              className="btn-ghost"
              style={{ color: 'var(--accent-rose)', borderColor: 'var(--accent-rose)' }}
              onClick={onStopStream}
            >
              ⏹️ Stop & Finalize Stream
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
