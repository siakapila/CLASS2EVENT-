import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  LineChart, Line, AreaChart, Area, PieChart, Pie, Cell 
} from 'recharts';
import { 
  Users, Calendar, CheckCircle, TrendingUp, Download, 
  Filter, Search, ArrowUpRight, ArrowDownRight 
} from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, trend, trendValue }) => (
  <div className="glass-panel p-6 rounded-2xl relative overflow-hidden group">
    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
      <Icon size={48} />
    </div>
    <div className="flex items-start justify-between">
      <div>
        <p className="text-slate-400 text-sm font-medium mb-1">{title}</p>
        <h3 className="text-3xl font-bold text-white">{value}</h3>
      </div>
      <div className={`flex items-center px-2 py-1 rounded-full text-xs font-bold ${
        trend === 'up' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
      }`}>
        {trend === 'up' ? <ArrowUpRight size={14} className="mr-1" /> : <ArrowDownRight size={14} className="mr-1" />}
        {trendValue}%
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/analytics/dashboard', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch dashboard stats", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  );

  if (!stats) return <div className="text-center p-10 text-white">No data available. Create some events first!</div>;

  const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f97316', '#10b981'];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black tracking-tight text-white mb-2">Metrics <span className="text-blue-500">Dashboard</span></h1>
          <p className="text-slate-400">Track your campus impact and event performance with real-time data.</p>
        </div>
        <button 
          onClick={() => window.open('http://127.0.0.1:8000/reports/summary/csv')}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold transition-all transform hover:scale-105 active:scale-95 shadow-lg shadow-blue-600/20"
        >
          <Download size={18} />
          Export Report (.CSV)
        </button>
      </header>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Events" value={stats.total_events} icon={Calendar} trend="up" trendValue={12} />
        <StatCard title="Total Registrations" value={stats.total_registrations} icon={Users} trend="up" trendValue={24} />
        <StatCard title="Total Attendance" value={stats.total_attendance} icon={CheckCircle} trend="up" trendValue={18} />
        <StatCard title="Avg. Attendance Rate" value={`${stats.avg_attendance_rate}%`} icon={TrendingUp} trend="up" trendValue={5} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Registration Trends */}
        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="text-xl font-bold text-white mb-6">Registration <span className="text-blue-500">Trends</span></h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats.registration_trends}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#3b82f6' }}
                />
                <Area type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorCount)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Attendance Breakdown */}
        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="text-xl font-bold text-white mb-6">Event <span className="text-purple-500">Popularity</span></h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.event_performance}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                <XAxis dataKey="title" stroke="#94a3b8" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px', color: '#fff' }}
                />
                <Bar dataKey="registrations" fill="#8b5cf6" radius={[6, 6, 0, 0]} />
                <Bar dataKey="attendance" fill="#3b82f6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Detailed Table */}
      <div className="glass-panel rounded-2xl overflow-hidden">
        <div className="p-6 border-b border-white/5 flex items-center justify-between">
          <h3 className="text-xl font-bold text-white">Detailed <span className="text-emerald-500">Breakdown</span></h3>
          <div className="flex items-center bg-white/5 rounded-lg px-4 py-2">
            <Search size={18} className="text-slate-400 mr-2" />
            <input type="text" placeholder="Search events..." className="bg-transparent border-none outline-none text-white text-sm" />
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-white/5 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-6 py-4">Event Title</th>
                <th className="px-6 py-4">Registrations</th>
                <th className="px-6 py-4">Attendance</th>
                <th className="px-6 py-4">Conv. Rate</th>
                <th className="px-6 py-4">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {stats.event_performance.map((event, idx) => (
                <tr key={idx} className="hover:bg-white/5 transition-colors">
                  <td className="px-6 py-4 font-medium text-white">{event.title}</td>
                  <td className="px-6 py-4 text-slate-300">{event.registrations}</td>
                  <td className="px-6 py-4 text-slate-300">{event.attendance}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-emerald-500 rounded-full" 
                          style={{ width: `${event.attendance_rate}%` }}
                        />
                      </div>
                      <span className="text-xs font-bold text-emerald-400">{event.attendance_rate}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <button 
                      onClick={() => window.open(`http://127.0.0.1:8000/reports/events/${event.event_id}/registrations/csv`)}
                      className="p-2 hover:bg-emerald-500/20 text-emerald-400 rounded-lg transition-colors"
                    >
                      <Download size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
