import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Sun, Moon, Leaf, Mail, Briefcase, Code, Cpu, Sparkles, ArrowRight, Compass, Activity } from 'lucide-react';
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
          An elegant exploration into the emotional resonance of language. Navigate to the AI tool to experience multidimensional sentiment visualization.
        </p>
        <Link to="/ai" className="blush-button inline-block mt-30">
          Enter the Studio <ArrowRight size={16} className="ml-2" />
        </Link>
      </div>

      <div className="info-grid mt-30">
        <div className="elegant-card p-40">
          <Cpu className="accent-green-icon mb-20" size={32} />
          <h3 className="section-title">The Circumplex Model</h3>
          <p className="body-text text-sm">
            Moving beyond simple positive/negative tracking, Neural maps emotions onto a 2D plane using Russell's Circumplex Model. By calculating structural heuristics, the engine plots your text based on its Valence (pleasantness) and Arousal (energy).
          </p>
        </div>

        <div className="elegant-card p-40">
          <Sparkles className="accent-peach-icon mb-20" size={32} />
          <h3 className="section-title">Lexicon-Based Analytics</h3>
          <p className="body-text text-sm">
            Powered by VADER (Valence Aware Dictionary and sEntiment Reasoner), the engine utilizes an ultra-fast, rule-based lexicon. It intelligently detects sentiment intensity, polarity, and context without the overhead of massive neural networks.
          </p>
        </div>
      </div>
    </div>
  );
}

// --- PAGE: ABOUT ---
function About() {
  return (
    <div className="page fade-in home-layout">
      <div className="elegant-card">
        <p className="subtitle">Our Philosophy</p>
        <h1 className="title mb-20">
          The <span className="title-green">Architecture</span>
        </h1>
        <p className="body-text mb-20">
          This application bridges the gap between raw computational math and human emotion. By mapping structural psychological vectors onto highly optimized sentiment algorithms, it interprets syntax without losing the poetic nuance of expression.
        </p>
        <p className="body-text">
          Built with a lightweight Flask API, NLTK VADER heuristics, and an interactive React frontend, it demonstrates the seamless integration of blazing-fast NLP pipelines into beautiful, experiential web interfaces.
        </p>
      </div>

      <div className="info-grid">
        <div className="elegant-card p-40">
          <Compass className="accent-peach-icon mb-20" size={32} />
          <h3 className="section-title">Valence & Arousal Mapping</h3>
          <p className="body-text text-sm">
            The mathematical plane is governed by James A. Russell’s psychological blueprint. The horizontal axis measures <strong>Valence</strong> (ranging from highly unpleasant cognitive states to blissful semantic constructs). The vertical axis tracks <strong>Arousal</strong>, capturing underlying somatic intensity and physiological activation levels.
          </p>
        </div>

        <div className="elegant-card p-40">
          <Activity className="accent-green-icon mb-20" size={32} />
          <h3 className="section-title">VADER Rule-Based Engines</h3>
          <p className="body-text text-sm">
            Instead of selecting just one label, our customized backend extracts structural probability coefficients from a lexicon. By mapping each sentiment's preset compound vector coordinates to its contextual intensity score, the interface builds an aggregate cross-emotional spatial coordinate.
          </p>
        </div>
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
      // 1. Updated URL to point to the local VADER backend
      const response = await fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'An unknown error occurred on the server.');
      }
      
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page fade-in home-layout">
      {/* MAIN CARD: INPUT AND VERDICT */}
      <div className="elegant-card text-center">
        <p className="subtitle">Circumplex Engine</p>
        <h1 className="title">
          <span className="title-peach">Neural</span> <span className="title-green">Mapping</span>
        </h1>
        <div className="divider"></div>
        <div className="input-group">
          <textarea
            className="editorial-input"
            placeholder="Type a sentence to visualize its emotional footprint..."
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
            {loading ? <span className="spinner"></span> : 'Plot Emotion'}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        {result && (
          <div className="result-box fade-in">
            <div className="emotion-readout fade-in">
              <h2>{result.primary_emotion}</h2>
              <p>Network Confidence: {result.confidence}</p>
            </div>

            <div className="circumplex-wrapper">
              <div className="circumplex-grid">
                <div className="x-axis"></div>
                <div className="y-axis"></div>
                <span className="axis-label top">High Energy</span>
                <span className="axis-label bottom">Low Energy</span>
                <span className="axis-label left">Unpleasant</span>
                <span className="axis-label right">Pleasant</span>
                
                <div 
                  className="circumplex-dot"
                  style={{
                    left: `${((result.valence + 1) / 2) * 100}%`,
                    top: `${((1 - result.arousal) / 2) * 100}%`
                  }}
                ></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* SECONDARY LAYOUT ROW */}
      {result && (
        <div className="info-grid fade-in">
          <div className="elegant-card p-40">
            <Compass className="accent-peach-icon mb-20" size={28} />
            <h3 className="section-title">Coordinate Mapping</h3>
            <div className="mt-30">
              <div className="metric-row">
                <span className="metric-label">Valence Axis (X)</span>
                <span className="metric-value">{result.valence > 0 ? `+${result.valence}` : result.valence}</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Arousal Axis (Y)</span>
                <span className="metric-value">{result.arousal > 0 ? `+${result.arousal}` : result.arousal}</span>
              </div>
            </div>
            <p className="body-text text-sm mt-30" style={{ fontSize: '13px' }}>
              These spatial coordinates reflect the mathematical epicenter of your syntax. Positive valence signifies language associated with pleasure, while elevated arousal logs somatic drive based on lexical intensity.
            </p>
          </div>

          <div className="elegant-card p-40">
            <Activity className="accent-green-icon mb-20" size={28} />
            <h3 className="section-title">Linguistic Dynamics</h3>
            <p className="body-text text-sm mt-30" style={{ fontSize: '13px' }}>
              Your input triggers a primary output of <strong>{result.primary_emotion}</strong>. Russell’s model suggests human feelings occupy a continuous topographic plane rather than isolated buckets. By using heuristic compound scores, the system maps structural intensity across an emotional continuum.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

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
        <div className="bg-shape shape-1"></div>
        <div className="bg-shape shape-2"></div>

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

        <div className="content-wrapper">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/ai" element={<AIPage />} />
          </Routes>
        </div>

        <Footer />
      </div>
    </Router>
  );
}

export default App;