import ReactMarkdown from 'react-markdown';
import './Stage3.css';

export default function Stage3({ verdict }) {
  if (!verdict) return null;

  // Parse the two conclusions from the Chairman's verdict text
  const text = verdict.verdict || '';
  const outcomeMatch = text.match(/MOST LIKELY OUTCOME:\s*([\s\S]*?)(?=MOST EFFECTIVE RESOLUTION:|$)/i);
  const resolutionMatch = text.match(/MOST EFFECTIVE RESOLUTION:\s*([\s\S]*?)$/i);

  const outcome = outcomeMatch ? outcomeMatch[1].trim() : null;
  const resolution = resolutionMatch ? resolutionMatch[1].trim() : null;

  return (
    <div className="stage stage3">
      <h3 className="stage-title">Stage 3: The Chairman's Verdict</h3>

      {outcome && (
        <div className="verdict-section outcome-section">
          <div className="verdict-label outcome-label">Most Likely Outcome</div>
          <div className="verdict-text markdown-content">
            <ReactMarkdown>{outcome}</ReactMarkdown>
          </div>
        </div>
      )}

      {resolution && (
        <div className="verdict-section resolution-section">
          <div className="verdict-label resolution-label">Most Effective Resolution</div>
          <div className="verdict-text markdown-content">
            <ReactMarkdown>{resolution}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Fallback: render full text if parsing fails */}
      {!outcome && !resolution && (
        <div className="verdict-section">
          <div className="verdict-text markdown-content">
            <ReactMarkdown>{text}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}
