import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Mail, Lock, User, Terminal, Building2, BookOpen, Key, Users } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const Auth = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const role = searchParams.get('role') || 'student';
  const [step, setStep] = useState('login'); // 'login', 'register', 'otp'
  const [mounted, setMounted] = useState(false);
  
  // Form Data State
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    registration_number: '',
    department: '',
    course: '',
    year: '',
    section: '',
    otp: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

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

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(''); // Clear error on edit
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Build payload based on role
      const payload = {
        full_name: formData.full_name,
        email: formData.email,
        password: formData.password
      };

      if (role === 'student') {
        Object.assign(payload, {
          registration_number: formData.registration_number,
          department: formData.department,
          course: formData.course,
          year: parseInt(formData.year),
          section: formData.section
        });
      } else if (role === 'faculty') {
        Object.assign(payload, {
          department: formData.department,
          course: formData.course
        });
      }

      const response = await fetch(`${API_BASE_URL}/auth/signup/${role}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          (data.detail && typeof data.detail === 'string' && data.detail) ||
          (data.detail && Array.isArray(data.detail) && data.detail[0]?.msg) ||
          'Registration failed'
        );
      }

      // Proceed to OTP step
      setStep('otp');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: formData.email, otp: formData.otp })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Invalid OTP');
      }

      // Redirect to login after successful validation
      setStep('login');
      setError('Email verified! You can now log in.');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const loginData = new URLSearchParams();
      loginData.append('username', formData.email);
      loginData.append('password', formData.password);

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: loginData.toString()
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      // Store token and redirect
      localStorage.setItem('token', data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

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
        
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold font-serif mb-2">
            {step === 'login' && 'Welcome Back'}
            {step === 'register' && 'Create Account'}
            {step === 'otp' && 'Verify Email'}
          </h2>
          <p className="text-slate-400">
            {step === 'otp' ? 'Check your inbox for a verification code' : config.subtitle}
          </p>
          <div className={`mt-2 font-bold uppercase tracking-widest text-xs ${config.color}`}>
            {config.title}
          </div>
        </div>

        {error && (
          <div className={`mb-6 p-3 text-sm rounded ${error.includes('verified') ? 'bg-green-500/10 border border-green-500/20 text-green-400' : 'bg-red-500/10 border border-red-500/20 text-red-400'}`}>
            {error}
          </div>
        )}

        {step === 'otp' && (
          <form className="space-y-5" onSubmit={handleVerifyOTP}>
            <div className="relative group">
              <Key className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-white transition-colors" size={20} />
              <input type="text" name="otp" placeholder="Enter 6-digit OTP" className="input-field pl-12 tracking-widest text-center text-lg" required value={formData.otp} onChange={handleInputChange} />
            </div>
            <button disabled={loading} className={`w-full py-4 rounded-xl bg-white text-slate-950 font-black tracking-wide font-display mt-8 transition-all hover:scale-[1.02] active:scale-95 shadow-[0_4px_20px_rgba(255,255,255,0.1)] ${config.shadow}`}>
              {loading ? 'Verifying...' : 'Verify & Continue'}
            </button>
          </form>
        )}

        {step === 'register' && (
          <form className="space-y-4" onSubmit={handleRegister}>
            <div className="relative group">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
              <input type="text" name="full_name" placeholder={role === 'club' ? 'Club Name' : 'Full Name'} className="input-field pl-12" required value={formData.full_name} onChange={handleInputChange} />
            </div>

            <div className="relative group">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
              <input type="email" name="email" placeholder={`College Email (@${role==='faculty'?'jaipur':'muj'}.manipal.edu)`} className="input-field pl-12" required value={formData.email} onChange={handleInputChange} />
            </div>

            {role === 'student' && (
              <>
                <div className="relative group">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                  <input type="text" name="registration_number" placeholder="Registration Number" className="input-field pl-12" required value={formData.registration_number} onChange={handleInputChange} />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="relative group">
                    <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input type="text" name="department" placeholder="Department" className="input-field pl-11 text-sm" required value={formData.department} onChange={handleInputChange} />
                  </div>
                  <div className="relative group">
                    <BookOpen className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input type="text" name="course" placeholder="Course" className="input-field pl-11 text-sm" required value={formData.course} onChange={handleInputChange} />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="relative group">
                    <input type="number" name="year" placeholder="Year (1-5)" min="1" max="5" className="input-field text-center" required value={formData.year} onChange={handleInputChange} />
                  </div>
                  <div className="relative group">
                    <input type="text" name="section" placeholder="Section" className="input-field text-center uppercase" maxLength="5" required value={formData.section} onChange={handleInputChange} />
                  </div>
                </div>
              </>
            )}

            {role === 'faculty' && (
              <div className="grid grid-cols-2 gap-4">
                <div className="relative group">
                  <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                  <input type="text" name="department" placeholder="Department" className="input-field pl-11 text-sm" required value={formData.department} onChange={handleInputChange} />
                </div>
                <div className="relative group">
                  <BookOpen className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                  <input type="text" name="course" placeholder="Course" className="input-field pl-11 text-sm" required value={formData.course} onChange={handleInputChange} />
                </div>
              </div>
            )}

            <div className="relative group">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
              <input type="password" name="password" placeholder="Password" className="input-field pl-12" required value={formData.password} onChange={handleInputChange} />
            </div>

            <button disabled={loading} className={`w-full py-4 rounded-xl bg-white text-slate-950 font-black tracking-wide font-display mt-8 transition-all hover:scale-[1.02] active:scale-95 shadow-[0_4px_20px_rgba(255,255,255,0.1)] ${config.shadow}`}>
              {loading ? 'Creating Account...' : 'Register'}
            </button>
          </form>
        )}

        {step === 'login' && (
          <form className="space-y-4" onSubmit={handleLogin}>
            <div className="relative group">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-white transition-colors" size={20} />
              <input type="email" name="email" placeholder="University Email" className="input-field pl-12" required value={formData.email} onChange={handleInputChange} />
            </div>

            <div className="relative group">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-white transition-colors" size={20} />
              <input type="password" name="password" placeholder="Password" className="input-field pl-12" required value={formData.password} onChange={handleInputChange} />
            </div>

            <button disabled={loading} className={`w-full py-4 rounded-xl bg-white text-slate-950 font-black tracking-wide font-display mt-8 transition-all hover:scale-[1.02] active:scale-95 shadow-[0_4px_20px_rgba(255,255,255,0.1)] ${config.shadow}`}>
              {loading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>
        )}

        {step !== 'otp' && (
          <div className="mt-8 text-center border-t border-slate-800 pt-6">
            <button 
              onClick={() => {
                setStep(step === 'login' ? 'register' : 'login');
                setError('');
              }}
              className="text-slate-400 hover:text-white transition-colors text-sm font-semibold inline-flex items-center gap-2"
            >
              {step === 'login' ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Auth;
