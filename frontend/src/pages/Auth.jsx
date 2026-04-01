import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Mail, Lock, User, Terminal } from 'lucide-react';

const Auth = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const role = searchParams.get('role') || 'student';
  const [isLogin, setIsLogin] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const themeConfig = {
    student: {
      color: 'text-[#FFB800]',
      shadow: 'hover:shadow-[0_0_20px_rgba(255,184,0,0.5)]',
      title: 'Student Access',
      subtitle: 'Join your campus ecosystem.',
    },
    club: {
      color: 'text-blue-500',
      shadow: 'hover:shadow-[0_0_20px_rgba(59,130,246,0.5)]',
      title: 'Club Organizer',
      subtitle: 'Manage events and engage members.',
    },
    faculty: {
      color: 'text-green-500',
      shadow: 'hover:shadow-[0_0_20px_rgba(34,197,94,0.5)]',
      title: 'Faculty Portal',
      subtitle: 'Verify attendance and oversee activity.',
    }
  };

  const config = themeConfig[role] || themeConfig.student;

  if (!mounted) return null;

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 relative">
      <button 
        onClick={() => navigate(-1)}
        className="absolute top-10 left-10 p-3 rounded-full bg-slate-900/50 hover:bg-slate-800 transition-colors border border-white/5 animate-fade-in"
      >
        <ArrowLeft size={24} />
      </button>

      <div className="card w-full max-w-md animate-fade-up">
        <div className="flex justify-center mb-6 mt-4">
          <Terminal size={48} className={config.color} />
        </div>
        
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold font-serif mb-2">{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
          <p className="text-slate-400">{config.subtitle}</p>
          <div className={`mt-2 font-bold uppercase tracking-widest text-xs ${config.color}`}>
            {config.title}
          </div>
        </div>

        <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
          {!isLogin && (
            <div className="relative group">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-white transition-colors" size={20} />
              <input type="text" placeholder="Full Name" className="input-field pl-12" required />
            </div>
          )}

          <div className="relative group">
            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-white transition-colors" size={20} />
            <input type="email" placeholder="University Email" className="input-field pl-12" required />
          </div>

          <div className="relative group">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-white transition-colors" size={20} />
            <input type="password" placeholder="Password" className="input-field pl-12" required />
          </div>

          <button className={`w-full py-4 rounded-xl bg-white text-slate-950 font-black tracking-wide font-display mt-8 transition-all hover:scale-[1.02] active:scale-95 shadow-[0_4px_20px_rgba(255,255,255,0.1)] ${config.shadow}`}>
            {isLogin ? 'Sign In' : 'Register'}
          </button>
        </form>

        <div className="mt-8 text-center">
          <button 
            onClick={() => setIsLogin(!isLogin)}
            className="text-slate-400 hover:text-white transition-colors text-sm font-semibold"
          >
            {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Auth;
