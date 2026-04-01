import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { GraduationCap, Users, UserCog, X, Lock } from 'lucide-react';

const TopBar = () => (
  <nav className="w-full flex justify-between items-center py-6 px-12 absolute top-0 z-10 animate-fade-in">
    <div className="text-2xl font-black tracking-tighter mix-blend-overlay">class2event</div>
    <div className="flex gap-8 items-center text-sm font-semibold opacity-90">
      <a href="#community" className="hover:text-school-bg transition-colors">Community</a>
      <a href="#about" className="hover:text-school-bg transition-colors">About</a>
      <a href="#support" className="hover:text-school-bg transition-colors">Support</a>
      <a href="#contact" className="hover:text-school-bg transition-colors">Contact</a>
      <button className="btn-ghost ml-4">Enter Portal</button>
    </div>
  </nav>
);

const PortalModal = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div 
        className="absolute inset-0 bg-slate-950/60 backdrop-blur-md animate-fade-in"
        onClick={onClose}
      />
      
      <div className="card w-full max-w-4xl min-h-[400px] flex flex-col justify-center animate-fade-up border-slate-700/50 bg-slate-900/80">
        <button 
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-full bg-white/5 hover:bg-white/10 transition-colors"
        >
          <X size={20} />
        </button>
        
        <div className="text-center mb-12">
          <h2 className="text-4xl font-black mb-3 font-serif">Select your Portal</h2>
          <p className="text-slate-400 font-medium tracking-wide">Choose how you want to interact with the university universe.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Student Portal */}
          <button 
            onClick={() => navigate('/auth?role=student')}
            className="group flex flex-col items-center p-8 rounded-3xl border border-white/5 bg-white/5 hover:bg-white/10 transition-all duration-300 hover:scale-105 active:scale-95 hover:border-school-bg/50"
          >
            <div className="h-20 w-20 rounded-full bg-[#3f311c] flex items-center justify-center mb-6 group-hover:shadow-[0_0_30px_rgba(255,184,0,0.3)] transition-all">
              <GraduationCap size={36} className="text-[#FFB800]" />
            </div>
            <h3 className="text-2xl font-bold mb-4">Student</h3>
            <p className="text-sm text-slate-400 text-center leading-relaxed">
              Discover thrilling events, register with your peers, and form dynamic teams.
            </p>
          </button>

          {/* Club Portal */}
          <button 
            onClick={() => navigate('/auth?role=club')}
            className="group flex flex-col items-center p-8 rounded-3xl border border-white/5 bg-white/5 hover:bg-white/10 transition-all duration-300 hover:scale-105 active:scale-95 hover:border-blue-500/50"
          >
            <div className="h-20 w-20 rounded-full bg-[#1e2a45] flex items-center justify-center mb-6 group-hover:shadow-[0_0_30px_rgba(59,130,246,0.3)] transition-all">
              <Users size={36} className="text-blue-500" />
            </div>
            <h3 className="text-2xl font-bold mb-4">Club</h3>
            <p className="text-sm text-slate-400 text-center leading-relaxed">
              Orchestrate events, manage registrations, and assign organizers securely.
            </p>
          </button>

          {/* Faculty Portal */}
          <button 
             onClick={() => navigate('/auth?role=faculty')}
             className="group flex flex-col items-center p-8 rounded-3xl border border-white/5 bg-white/5 hover:bg-white/10 transition-all duration-300 hover:scale-105 active:scale-95 hover:border-green-500/50"
          >
            <div className="h-20 w-20 rounded-full bg-[#1b3327] flex items-center justify-center mb-6 group-hover:shadow-[0_0_30px_rgba(34,197,94,0.3)] transition-all">
              <UserCog size={36} className="text-green-500" />
            </div>
            <h3 className="text-2xl font-bold mb-4">Faculty</h3>
            <p className="text-sm text-slate-400 text-center leading-relaxed">
              Oversee student participation effortlessly with verified attendee lists.
            </p>
          </button>
        </div>
      </div>
    </div>
  );
};

const Welcome = () => {
  const [mounted, setMounted] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="flex-1 w-full relative flex flex-col">
      <TopBar />
      
      <main className="flex-1 flex flex-col justify-center px-12 lg:px-24">
        <div className="flex items-center gap-3 mb-6 animate-fade-up opacity-0" style={{ animationDelay: '200ms', animationFillMode: 'forwards' }}>
          <Lock size={16} className="text-slate-300" />
          <span className="text-sm font-semibold tracking-widest text-slate-300">Journey to new frontiers. Connect your campus.</span>
        </div>
        
        <h1 
          className="text-8xl md:text-[10rem] font-black leading-none mb-8 tracking-tighter opacity-0"
          style={{ 
            animation: 'fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards',
            animationDelay: '400ms',
            /* Fallback classic serif for the massive heading */
            fontFamily: '"Playfair Display", "Times New Roman", serif', 
            textShadow: '0 10px 30px rgba(0,0,0,0.5)'
          }}
        >
          CLASS<span className="text-white/80">2</span>EVENT
        </h1>
        
        <p 
          className="max-w-2xl text-lg md:text-xl text-slate-100/90 leading-relaxed font-medium mb-10 opacity-0 animate-fade-up"
          style={{ animationDelay: '600ms', animationFillMode: 'forwards', textShadow: '0 2px 10px rgba(0,0,0,0.8)' }}
        >
          Away from the manic energy of ordinary student life lies a unified platform linking clubs, students, and faculty. Surprising and captivating in equal measure, this is event management entirely reimagined.
        </p>
        
        <div className="opacity-0 animate-fade-up" style={{ animationDelay: '800ms', animationFillMode: 'forwards' }}>
          <button 
            onClick={() => setModalOpen(true)}
            className="group btn-primary inline-flex gap-4"
          >
            Start the journey
            <span className="group-hover:translate-x-1 transition-transform">►</span>
          </button>
        </div>
      </main>

      <PortalModal isOpen={modalOpen} onClose={() => setModalOpen(false)} />
    </div>
  );
};

export default Welcome;
