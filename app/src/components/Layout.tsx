import React, { useState, useEffect } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import Header from './Header';

const Layout: React.FC = () => {
  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  if (loading) return <div className="min-h-screen bg-[#f8fafc] flex items-center justify-center font-black uppercase tracking-widest text-slate-400">Caricamento...</div>;
  if (!session) return <Navigate to="/login" replace />;

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans selection:bg-blue-100">
      <Header session={session} />
      <main>
        <Outlet /> 
      </main>
    </div>
  );
};

export default Layout;
