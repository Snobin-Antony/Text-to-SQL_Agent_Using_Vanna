// src/App.js

import React, { useState } from 'react';
import ChatPanel from './components/ChatPanel';
import Dashboard from './components/Dashboard';

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // --- NEW: State to manage chat panel visibility ---
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleAsk = async (question) => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const backendUrl = 'http://localhost:8000/api/ask'; 
      const res = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || data.detail || 'An unknown server error occurred.');
      }

      setResponse(data);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // --- NEW: Functions to open and close the chat panel ---
  const openChatPanel = () => setIsChatOpen(true);
  const closeChatPanel = () => setIsChatOpen(false);

  return (
    <div className="App">
      {/* Pass the openChatPanel function to the Dashboard */}
      <Dashboard 
        response={response} 
        loading={loading} 
        error={error}
        onOpenChat={openChatPanel} 
      />
      
      {/* --- NEW: Conditionally render the ChatPanel --- */}
      {isChatOpen && (
        <ChatPanel 
          onAsk={handleAsk} 
          loading={loading}
          onClose={closeChatPanel} // Pass the close function
        />
      )}
    </div>
  );
}

export default App;