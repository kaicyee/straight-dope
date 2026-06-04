import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>Straight Dope</h1>
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + New Question
        </button>
      </div>

      <div className="conversation-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">No sessions yet</div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`conversation-item ${conv.id === currentConversationId ? 'active' : ''}`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <div className="conversation-title">
                {conv.title || 'New Session'}
              </div>
              <div className="conversation-meta">
                {conv.message_count} {conv.message_count === 1 ? 'question' : 'questions'}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
