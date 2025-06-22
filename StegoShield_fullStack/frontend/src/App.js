import React, { useState, useEffect } from 'react';
import axios from 'axios';

// --- CSS Styles ---
// In a self-contained environment, we include CSS directly in the component.
const Styles = () => (
  <style>{`
    /* General Body & Layout */
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        background-color: #f4f7f9;
        color: #333;
        margin: 0;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        min-height: 100vh;
    }

    .container {
        width: 100%;
        max-width: 900px;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    header {
        background-color: #4a5568;
        color: white;
        padding: 20px 30px;
    }

    header h1 {
        margin: 0;
        font-size: 2rem;
    }

    header p {
        margin: 5px 0 0;
        opacity: 0.9;
    }

    main {
        padding: 20px 30px;
    }

    footer {
        background-color: #e2e8f0;
        text-align: center;
        padding: 15px;
        font-size: 0.9em;
        color: #4a5568;
        border-top: 1px solid #cbd5e0;
    }

    /* Tab Navigation */
    .tabs {
        display: flex;
        background-color: #edf2f7;
        border-bottom: 2px solid #cbd5e0;
    }

    .tabs button {
        padding: 14px 20px;
        text-decoration: none;
        color: #4a5568;
        font-weight: bold;
        border: none;
        background: none;
        cursor: pointer;
        font-size: 1em;
        border-bottom: 3px solid transparent;
        transition: all 0.2s ease-in-out;
    }

    .tabs button:hover {
        background-color: #e2e8f0;
    }

    .tabs button.active {
        color: #2c5282;
        border-bottom-color: #2c5282;
    }

    /* Content & Forms */
    .content-box {
        padding: 20px;
        border: 1px solid #e2e8f0;
        border-radius: 5px;
        background: #fdfdfd;
    }

    .content-box h2 {
        margin-top: 0;
        color: #2d3748;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        font-weight: bold;
        margin-bottom: 8px;
    }

    .form-group input[type="file"],
    .form-group textarea {
        width: 100%;
        padding: 10px;
        border: 1px solid #cbd5e0;
        border-radius: 4px;
        box-sizing: border-box;
        font-size: 1em;
    }

    button[type="submit"] {
        background-color: #3182ce;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1em;
        font-weight: bold;
        transition: background-color 0.2s;
    }

    button[type="submit"]:hover:not(:disabled) {
        background-color: #2b6cb0;
    }

    button[type="submit"]:disabled {
        background-color: #a0aec0;
        cursor: not-allowed;
    }


    /* Results & Messages */
    .result-box {
      margin-top: 20px;
      padding: 15px;
    }

    .message-box {
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 4px;
        color: #fff;
        text-align: center;
    }

    .message-box.error {
        background-color: #e53e3e;
    }

    .message-box.success {
        background-color: #38a169;
    }

    /* Image Previews */
    .image-preview-container {
        display: flex;
        justify-content: space-around;
        gap: 20px;
        flex-wrap: wrap;
        margin-top: 20px;
    }

    .image-preview {
        text-align: center;
        width: 45%;
        min-width: 300px;
    }

    .image-preview h3 {
        margin-bottom: 10px;
        color: #4a5568;
    }

    .image-preview img {
        max-width: 100%;
        height: auto;
        border: 3px solid #e2e8f0;
        border-radius: 5px;
    }

    /* Help Page */
    .help-content hr {
        border: 0;
        height: 1px;
        background-color: #cbd5e0;
        margin: 30px 0;
    }
    .help-content p {
        line-height: 1.6;
    }

    /* Loading Spinner */
    .spinner {
        border: 5px solid #f3f3f3;
        border-top: 5px solid #3498db;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
  `}</style>
);


// --- Reusable Components ---

// Component for a single form input field
const FormInput = ({ label, type = "text", value, onChange, placeholder, required = true, accept }) => (
  <div className="form-group">
    <label>{label}</label>
    {type === 'textarea' ? (
      <textarea value={value} onChange={onChange} placeholder={placeholder} required={required} rows="4" />
    ) : (
      <input type={type} onChange={onChange} placeholder={placeholder} required={required} accept={accept} />
    )}
  </div>
);

// Component for displaying API responses (errors or success messages)
const MessageBox = ({ message, type }) => {
  if (!message) return null;
  return <div className={`message-box ${type}`}>{message}</div>;
};

// Component for showing image previews
const ImagePreview = ({ title, src }) => {
  if (!src) return null;
  return (
    <div className="image-preview">
      <h3>{title}</h3>
      <img src={src} alt={title} />
    </div>
  );
};


// --- Main App Component ---

function App() {
  const [activeTab, setActiveTab] = useState('encodeText');
  
  // State for API communication
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  // State for form inputs
  const [carrierImage, setCarrierImage] = useState(null);
  const [secretText, setSecretText] = useState('');
  const [secretImage, setSecretImage] = useState(null);
  const [encodedImage, setEncodedImage] = useState(null);

  // State for help text
  const [helpContent, setHelpContent] = useState(null);

  const API_URL = 'http://localhost:5000/api';

  // --- Helper Functions ---
  const resetState = () => {
    setLoading(false);
    setError('');
    setResult(null);
    setCarrierImage(null);
    setSecretText('');
    setSecretImage(null);
    setEncodedImage(null);
    // Reset file input fields visually
    document.querySelectorAll('input[type="file"]').forEach(input => (input.value = ''));
  };

  const handleTabClick = (tab) => {
    setActiveTab(tab);
    resetState();
  };

  // Generic file download handler
  const downloadFile = (response, filename) => {
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    // Return the URL for previewing
    return url;
  };
  
  // Unified error handler for API calls
  const handleApiError = async (err) => {
    if (err.response && err.response.data) {
        // If the response data is a blob, it needs to be read as text first
        if (err.response.data instanceof Blob) {
            try {
                const errorText = await err.response.data.text();
                const errorJson = JSON.parse(errorText);
                setError(errorJson.error || 'Failed to process the request.');
            } catch (parseError) {
                setError('An unreadable error response was received from the server.');
            }
        } else {
            // If it's not a blob, it might already be a JSON object
            setError(err.response.data.error || 'An unexpected error occurred.');
        }
    } else {
        // This handles cases like "Network Error" where there's no response object
        setError('Network Error: Could not connect to the server. Please ensure the backend is running.');
    }
  };


  // --- API Handlers ---

  const handleEncodeText = async (e) => {
    e.preventDefault();
    if (!carrierImage || !secretText) {
      setError('Please provide a carrier image and a secret message.');
      return;
    }
    const formData = new FormData();
    formData.append('carrier', carrierImage);
    formData.append('message', secretText);
    
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/encode-text`, formData, { responseType: 'blob' });
      const downloadUrl = downloadFile(response, 'encoded_text.png');
      setResult({
        type: 'image-preview',
        original: URL.createObjectURL(carrierImage),
        processed: downloadUrl,
        message: "Text encoded successfully! The download has started."
      });
    } catch (err) {
      await handleApiError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDecodeText = async (e) => {
    e.preventDefault();
    if (!encodedImage) {
      setError('Please provide an image to decode.');
      return;
    }
    const formData = new FormData();
    formData.append('encoded', encodedImage);

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/decode-text`, formData);
      setResult({ type: 'text', message: response.data.message });
    } catch (err) {
      await handleApiError(err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleEncodeImage = async (e) => {
    e.preventDefault();
    if (!carrierImage || !secretImage) {
      setError('Please provide both a carrier and a secret image.');
      return;
    }
    const formData = new FormData();
    formData.append('carrier', carrierImage);
    formData.append('secret', secretImage);

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/encode-image`, formData, { responseType: 'blob' });
      const downloadUrl = downloadFile(response, 'encoded_image.png');
       setResult({
        type: 'image-preview',
        original: URL.createObjectURL(carrierImage),
        processed: downloadUrl,
        message: "Image encoded successfully! The download has started."
      });
    } catch (err) {
      await handleApiError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDecodeImage = async (e) => {
    e.preventDefault();
    if (!encodedImage) {
      setError('Please provide an image to decode.');
      return;
    }
    const formData = new FormData();
    formData.append('encoded', encodedImage);

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/decode-image`, formData, { responseType: 'blob' });
      const extractedUrl = downloadFile(response, 'extracted_image.png');
      setResult({
        type: 'image-preview',
        original: URL.createObjectURL(encodedImage),
        processed: extractedUrl,
        originalTitle: 'Encoded Image',
        processedTitle: 'Extracted Secret Image',
        message: "Image extracted successfully! The download has started."
      });
    } catch (err) {
      await handleApiError(err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch help text on component mount
  useEffect(() => {
    const fetchHelp = async () => {
      try {
        const response = await axios.get(`${API_URL}/help`);
        setHelpContent(response.data);
      } catch (err) {
        console.error("Failed to fetch help content:", err);
        setError('Network Error: Could not load help content. Please ensure the backend server is running and refresh the page.');
      }
    };
    fetchHelp();
  }, []);

  // --- Render Functions for Tabs ---

  const renderContent = () => {
    switch (activeTab) {
      case 'encodeText':
        return (
          <form onSubmit={handleEncodeText}>
            <h2>Hide a Text Message in an Image</h2>
            <FormInput label="Carrier Image" type="file" onChange={e => setCarrierImage(e.target.files[0])} accept="image/*" />
            <FormInput label="Secret Message" type="textarea" value={secretText} onChange={e => setSecretText(e.target.value)} placeholder="Enter your secret message..." />
            <button type="submit" disabled={loading}>{loading ? 'Encoding...' : 'Encode Text'}</button>
          </form>
        );
      case 'decodeText':
        return (
          <form onSubmit={handleDecodeText}>
            <h2>Extract a Hidden Message from an Image</h2>
            <FormInput label="Encoded Image (PNG)" type="file" onChange={e => setEncodedImage(e.target.files[0])} accept="image/*" />
            <button type="submit" disabled={loading}>{loading ? 'Decoding...' : 'Decode Text'}</button>
          </form>
        );
      case 'encodeImage':
         return (
          <form onSubmit={handleEncodeImage}>
            <h2>Hide an Image Inside Another Image</h2>
            <FormInput label="Carrier Image (the one that will be visible)" type="file" onChange={e => setCarrierImage(e.target.files[0])} accept="image/*" />
            <FormInput label="Secret Image (the one you want to hide)" type="file" onChange={e => setSecretImage(e.target.files[0])} accept="image/*" />
            <button type="submit" disabled={loading}>{loading ? 'Encoding...' : 'Encode Image'}</button>
          </form>
        );
      case 'decodeImage':
        return (
          <form onSubmit={handleDecodeImage}>
            <h2>Extract a Hidden Image from an Image</h2>
            <FormInput label="Encoded Image (PNG)" type="file" onChange={e => setEncodedImage(e.target.files[0])} accept="image/*" />
            <button type="submit" disabled={loading}>{loading ? 'Decoding...' : 'Decode Image'}</button>
          </form>
        );
      case 'help':
        if (!helpContent) return <p>Loading help content...</p>;
        return (
          <div className="help-content">
            <h2>{helpContent.title_what_it_does}</h2>
            <p dangerouslySetInnerHTML={{ __html: helpContent.text_what_it_does.replace(/\n/g, '<br />') }} />
            <hr />
            <h2>{helpContent.title_how_to_use}</h2>
            <p dangerouslySetInnerHTML={{ __html: helpContent.text_how_to_use.replace(/\n/g, '<br />') }} />
            <hr />
            <h2>{helpContent.title_rules_restrictions}</h2>
            <p dangerouslySetInnerHTML={{ __html: helpContent.text_rules_restrictions.replace(/\n/g, '<br />') }} />
          </div>
        );
      default:
        return null;
    }
  };

  const renderResult = () => {
    if (!result) return null;
    
    if (result.type === 'text') {
      return <MessageBox message={`Decoded Message: ${result.message}`} type="success" />;
    }

    if (result.type === 'image-preview') {
      return (
        <div className="result-container">
           <MessageBox message={result.message} type="success" />
           <div className="image-preview-container">
            <ImagePreview title={result.originalTitle || "Original Carrier Image"} src={result.original} />
            <ImagePreview title={result.processedTitle || "Processed Stego Image"} src={result.processed} />
           </div>
        </div>
      );
    }
    
    return null;
  };

  return (
    <>
      <Styles />
      <div className="container">
        <header>
          <h1>🛡️ StegoShield Full-Stack</h1>
          <p>A React & Flask application for steganography.</p>
        </header>
        <nav className="tabs">
          <button onClick={() => handleTabClick('encodeText')} className={activeTab === 'encodeText' ? 'active' : ''}>Encode Text</button>
          <button onClick={() => handleTabClick('decodeText')} className={activeTab === 'decodeText' ? 'active' : ''}>Decode Text</button>
          <button onClick={() => handleTabClick('encodeImage')} className={activeTab === 'encodeImage' ? 'active' : ''}>Encode Image</button>
          <button onClick={() => handleTabClick('decodeImage')} className={activeTab === 'decodeImage' ? 'active' : ''}>Decode Image</button>
          <button onClick={() => handleTabClick('help')} className={activeTab === 'help' ? 'active' : ''}>Help</button>
        </nav>
        <main>
          <div className="content-box">
            {renderContent()}
          </div>
          <div className="result-box">
            {loading && <div className="spinner"></div>}
            <MessageBox message={error} type="error" />
            {renderResult()}
          </div>
        </main>
        <footer>
          <p>StegoShield Full-Stack Application</p>
        </footer>
      </div>
    </>
  );
}

export default App;
