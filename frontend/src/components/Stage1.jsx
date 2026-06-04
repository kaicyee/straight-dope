import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './Stage1.css';

const ROLE_COLORS = {
  Forecaster: '#e67e22',
  Critic: '#c0392b',
  'Reality-Checker': '#8e44ad',
};

export default function Stage1({ responses }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!responses || responses.length === 0) return null;

  const active = responses[activeTab];
  const color = ROLE_COLORS[active.role] || '#888';

  return (
    <div className="stage stage1">
      <h3 className="stage-title">Stage 1: The Advisors Speak</h3>

      <div className="tabs">
        {responses.map((resp, index) => (
          <button
            key={index}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            style={activeTab === index ? { borderColor: ROLE_COLORS[resp.role], color: ROLE_COLORS[resp.role] } : {}}
            onClick={() => setActiveTab(index)}
          >
            {resp.role}
          </button>
        ))}
      </div>

      <div className="tab-content">
        <div className="role-label" style={{ color }}>
          {active.role}
        </div>
        <div className="response-text markdown-content">
          <ReactMarkdown>{active.response}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
