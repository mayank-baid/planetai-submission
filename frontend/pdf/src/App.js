import './App.css';
import React, { useState } from 'react';
import Header from './Header';
import ChatInterface from './ChatInterface'

function App() {
  const [pdfName, setPdfName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePdfUpload = async (event) => {
    setPdfName('');
    const file = event.target.files[0];
    if (file) {
      setLoading(true);
      setError(null);

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://127.0.0.1:8000/upload-pdf', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Failed to upload PDF');
        }

        const data = await response.json();
        const filename = data.filename;
        setPdfName(filename);
      } catch (error) {
        console.error('Error uploading PDF:', error);
        setError('Failed to upload PDF. Please try again!');
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="App">
      <Header pdfName={pdfName} onPdfUpload={handlePdfUpload}>
      </Header>
      <main>
        <div className="loading-overlay">
          {loading && (
            <div className='loading-container'>
              <div className="loader"></div>
              <h3 className="loading">Processing PDF! Please wait</h3>
            </div>
          )}
          {error && <h3 className="loading-error">Error: {error}</h3>}
        </div>
        <ChatInterface disabled={loading || error || !pdfName} newUpload={loading} />
      </main>
    </div>
  );
}

export default App;
