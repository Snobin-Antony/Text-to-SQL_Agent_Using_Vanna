// src/components/Dashboard.js

import React from 'react';

// The renderResultsTable function remains the same...
const renderResultsTable = (results) => {
    // ... (no changes needed here)
    if (!results || results.length === 0) {
        return <p>No results found for this query.</p>;
    }
    const columns = Object.keys(results[0]);
    return (
        <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid #ccc' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
                {columns.map((col, index) => (
                <th key={index} style={{ border: '1px solid #ccc', padding: '12px', textAlign: 'left' }}>{col}</th>
                ))}
            </tr>
            </thead>
            <tbody>
            {results.map((row, rowIndex) => (
                <tr key={rowIndex} style={{ borderBottom: '1px solid #eee' }}>
                {columns.map((col, colIndex) => (
                    <td key={colIndex} style={{ border: '1px solid #ccc', padding: '12px' }}>{String(row[col])}</td>
                ))}
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    );
};


// --- UPDATED: The Dashboard now receives an onOpenChat prop ---
const Dashboard = ({ response, loading, error, onOpenChat }) => {
  // --- REMOVED: No longer need marginRight as the panel is a pop-up ---
  const dashboardStyles = {
    padding: '20px',
    transition: 'filter 0.3s ease-in-out', // For a nice blur effect later
  };
  
  const fabStyles = { // Floating Action Button styles
    position: 'fixed',
    bottom: '30px',
    right: '30px',
    width: '60px',
    height: '60px',
    borderRadius: '50%',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '24px',
    zIndex: 999,
  };
  
  // Same renderContent function as before...
  const renderContent = () => {
    if (loading) {
      return <p>Loading results...</p>;
    }
    if (error) {
      return (
        <div style={{ color: '#D8000C', backgroundColor: '#FFD2D2', padding: '10px', border: '1px solid #D8000C', borderRadius: '4px' }}>
          <strong>Error:</strong> {error}
        </div>
      );
    }
    if (response) {
      return (
        <div>
          <h3>Generated SQL:</h3>
          <pre style={{ backgroundColor: '#f0f0f0', padding: '15px', borderRadius: '4px', overflowX: 'auto', border: '1px solid #ddd' }}>
            <code>{response.sql}</code>
          </pre>

          <h3>Results:</h3>
          {renderResultsTable(response.results)}
        </div>
      );
    }
    return <p>Click the AI button to ask a question and see the results here.</p>;
  };

  return (
    <div style={dashboardStyles}>
      <h1>Dashboard</h1>
      <div style={{ marginTop: '20px' }}>
        {renderContent()}
      </div>

      {/* --- NEW: The button that opens the chat panel --- */}
      <button onClick={onOpenChat} style={fabStyles} title="Ask AI Agent">
        AI
      </button>
    </div>
  );
};

export default Dashboard;