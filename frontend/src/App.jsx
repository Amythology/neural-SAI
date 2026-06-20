import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Sun, Moon, Leaf, Mail, Briefcase, Code, Cpu, Sparkles, ArrowRight } from 'lucide-react';
import './App.css';

// --- GLOBAL FOOTER COMPONENT ---
function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>Designed & Developed by <strong>Amith S</strong></p>
        <div className="social-links">
          <a href="mailto:amith0755@gmail.com" className="social-link">
            <Mail size={16} /> amith0755@gmail.com
          </a>
          <a href="https://linkedin.com/in/amythologies" target="_blank" rel="noreferrer" className="social-link">
            <Briefcase size={16} /> amythologies
          </a>
          <a href="https://github.com/amythology" target="_blank" rel="noreferrer" className="social-link">
            <Code size={16} /> amythology
          </a>
        </div>
      </div>
    </footer>
  );
}

// --- PAGE: HOME ---
function Home() {
  return (
    <div className="page fade-in home-layout">
      <div className="elegant-card text-center hero-section">
        <Leaf className="accent-icon mx-auto" size={42} />
        <h1 className="title">
          <span className="title-dark">Welcome to</span> <span className="title-peach">Neural</span>
        </h1>
        <p className="body-text max-w-lg mx-auto">
          An elegant exploration into the emotional resonance of language. Navigate to the AI tool to experience natural language processing in a refined, minimalist environment.
        </p>
        <Link to="/ai" className="blush-button inline-block mt-30">
          Enter the Studio <ArrowRight size={16} className="ml-2" />
        </Link>
      </div>

      <div className="info-grid mt-30">
        <div className="elegant-card p-40">
          <Cpu className="accent-green-icon mb-20" size={32} />
          <h3 className="section-title">How It Works</h3>
          <p className="body-text text-sm">
            Neural utilizes a custom-trained Logistic Regression model powered by Word2Vec Twitter embeddings. By mapping sentences into a 25-dimensional mathematical space, it bypasses the limitations of traditional keyword counting to understand context, slang, and genuine emotional weight.
          </p>
        </div>

        <div className="elegant-card p-40">
          <Sparkles className="accent-peach-icon mb-20" size={32} />
          <h3 className="section-title">The Horizon</h3>
          <p className="body-text text-sm">
            We are continuously refining the architecture. Upcoming updates include a transition to a deep-learning Transformer (BERT) backend for full sequential context awareness, multilingual support, and real-time API webhooks for developers.
          </p>
        </div>
      </div>
    </div>
  );
}

// --- PAGE: ABOUT ---
function About() {
  return (
    <div className="page fade-in">
      <div className="elegant-card">
        <p className="subtitle">Our Philosophy</p>
        <h1 className="title mb-20">
          The <span className="title-green">Architecture</span>
        </h1>
        <p className="body-text mb-20">
          This application bridges the gap between raw computational math and human emotion. Powered by a custom Python backend parsing thousands of data points, it interprets sentiment without losing the poetic nuance of human expression.
        </p>
        <p className="body-text">
          Built with a lightweight Flask API and an interactive React frontend, it demonstrates the seamless integration of classic Machine Learning pipelines into modern web experiences.
        </p>
      </div>
    </div>
  );
}

// --- PAGE: AI ENGINE ---
function AIPage() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeSentiment = async () => {
    if (!text.trim()) return;
    setLoading(true); 
    setError(null); 
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) throw new Error('Server error');
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Could not connect to the AI server. Is it running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page fade-in">
      <div className="elegant-card text-center">
        <p className="subtitle">AI Analysis</p>
        <h1 className="title">
          <span className="title-peach">Neural</span> <span className="title-green">Sentiment</span>
        </h1>
        <div className="divider"></div>
        <div className="input-group">
          <textarea
            className="editorial-input"
            placeholder="Enter your thoughts here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => { 
              if (e.key === 'Enter' && !e.shiftKey) { 
                e.preventDefault(); 
                analyzeSentiment(); 
              } 
            }}
          />
          <button className="blush-button" onClick={analyzeSentiment} disabled={loading || !text.trim()}>
            {loading ? <span className="spinner"></span> : 'Analyze Text'}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        {result && (
          <div className={`result-box fade-in ${result.sentiment.toLowerCase()}`}>
            <div className="result-header">
              <h2>{result.sentiment}</h2>
            </div>
            <div className="confidence-container">
              <div className="confidence-bar-bg">
                <div className="confidence-bar-fill" style={{ width: result.confidence }}></div>
              </div>
              <p className="confidence-text">Confidence: {result.confidence}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// --- MAIN APP COMPONENT ---
function App() {
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  return (
    <Router>
      <div className="app-container">
        {/* Background ambient shapes */}
        <div className="bg-shape shape-1"></div>
        <div className="bg-shape shape-2"></div>

        {/* Elegant Navigation Bar */}
        <nav className="navbar">
          <div className="nav-brand">
            <Leaf size={18} /> Neural
          </div>
          <div className="nav-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/about" className="nav-link">About</Link>
            <Link to="/ai" className="nav-link">AI Engine</Link>
            <button onClick={toggleTheme} className="theme-toggle" aria-label="Toggle Theme">
              {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
            </button>
          </div>
        </nav>

        {/* Page Routing Area */}
        <div className="content-wrapper">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/ai" element={<AIPage />} />
          </Routes>
        </div>

        {/* Global Footer */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;