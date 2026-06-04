import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './Stage2.css';

const ROLE_COLORS = {
  Forecaster: '#e67e22',
  Critic: '#c0392b',
  'Reality-Checker': '#8e44ad',
};

export default function Stage2({ challenges }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!challenges || challenges.length === 0) return null;

  const active = challenges[activeTab];
  const color = ROLE_COLORS[active.role] || '#888';

  return (
    <div className="stage stage2">
      <h3 className="stage-title">Stage 2: Cross-Examination</h3>
      <p className="stage-description">
        Each advisor challenges the weakest argument from the other two.
      </p>

      <div className="tabs">
        {challenges.map((ch, index) => (
          <button
            key={index}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            style={activeTab === index ? { borderColor: ROLE_COLORS[ch.role], color: ROLE_COLORS[ch.role] } : {}}
            onClick={() => setActiveTab(index)}
          >
            {ch.role}
          </button>
        ))}
      </div>

      <div className="tab-content">
        <div className="role-label" style={{ color }}>
          {active.role} — Challenge
        </div>
        <div className="challenge-text markdown-content">
          <ReactMarkdown>{active.challenge}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
