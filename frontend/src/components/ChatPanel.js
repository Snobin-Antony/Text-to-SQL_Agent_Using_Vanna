// src/components/ChatPanel.js

import React, { useState } from 'react';

// --- UPDATED: It now receives an onClose prop ---
const ChatPanel = ({ onAsk, loading, onClose }) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    onAsk(question);
    // We can choose to either close the panel on submit or keep it open
    // For now, let's keep it open to see the loading state.
    // onClose(); 
  };

  // --- NEW: Styles for the modal backdrop ---
  const backdropStyles = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 1000,
    display: 'flex',
    justifyContent: 'flex-end', // Align the panel to the right
  };

  // --- UPDATED: Styles for the panel itself ---
  const panelStyles = {
    width: '420px',
    height: '100%',
    backgroundColor: 'white',
    boxShadow: '-5px 0px 15px rgba(0,0,0,0.2)',
    padding: '20px',
    boxSizing: 'border-box',
    display: 'flex',
    flexDirection: 'column',
    position: 'relative', // For positioning the close button
  };

  const closeButtonStyles = {
    position: 'absolute',
    top: '15px',
    right: '15px',
    background: 'transparent',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer',
    color: '#888',
  };

  return (
    // Clicking the backdrop calls the onClose function
    <div style={backdropStyles} onClick={onClose}>
      {/* Clicks inside the panel are stopped from propagating to the backdrop */}
      <div style={panelStyles} onClick={(e) => e.stopPropagation()}>
        <button onClick={onClose} style={closeButtonStyles} title="Close">
          &times;
        </button>
        <h2>Data AI Agent</h2>
        <p>Ask a question to query the database.</p>
        <form onSubmit={handleSubmit} style={{ marginTop: 'auto' }}>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Show total sales per country..."
            style={{ width: '100%', minHeight: '80px', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '1rem', marginBottom: '10px' }}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            style={{ width: '100%', padding: '12px 20px', borderRadius: '4px', border: 'none', backgroundColor: '#007bff', color: 'white', cursor: loading ? 'not-allowed' : 'pointer', fontSize: '1rem' }}
          >
            {loading ? 'Thinking...' : 'Ask'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPanel;