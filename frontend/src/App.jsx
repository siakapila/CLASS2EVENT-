import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Welcome from './pages/Welcome';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import CustomCursor from './components/CustomCursor';

function Background() {
  return (
    <>
      {/* User must supply their image as public/background.jpg */}
      <div 
        className="fixed inset-0 z-[-2] bg-cover bg-center bg-no-repeat object-cover"
        style={{ backgroundImage: "url('/background.jpg')" }}
      />
      <div className="ambient-overlay" />
    </>
  );
}

function App() {
  return (
    <Router>
      <CustomCursor />
      <Background />
      <div className="flex flex-col min-h-screen text-slate-100 font-display">
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/auth" element={<Auth />} />
          {/* Dashboard route with metrics and and visuals */}
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
