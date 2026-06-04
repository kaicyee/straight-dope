/**
 * API client for the Straight Dope backend.
 */

const API_BASE = 'http://localhost:8002';

export const api = {
  async listConversations() {
    const response = await fetch(`${API_BASE}/api/conversations`);
    if (!response.ok) throw new Error('Failed to list sessions');
    return response.json();
  },

  async createConversation() {
    const response = await fetch(`${API_BASE}/api/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    });
    if (!response.ok) throw new Error('Failed to create session');
    return response.json();
  },

  async getConversation(conversationId) {
    const response = await fetch(`${API_BASE}/api/conversations/${conversationId}`);
    if (!response.ok) throw new Error('Failed to get session');
    return response.json();
  },

  async sendMessageStream(conversationId, content, onEvent) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}/message/stream`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      }
    );

    if (!response.ok) throw new Error('Failed to send message');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          try {
            const event = JSON.parse(data);
            onEvent(event.type, event);
          } catch (e) {
            console.error('Failed to parse SSE event:', e);
          }
        }
      }
    }
  },
};
