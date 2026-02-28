import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import { Trophy, LogOut, Shield, Users, LayoutDashboard } from 'lucide-react';

const Header = ({ session }: { session: any }) => {
    const handleLogout = async () => {
        await supabase.auth.signOut();
    };

    const ADMIN_EMAIL = "bonfantistefano4@gmail.com";
    
    const activeLinkStyle = {
        backgroundColor: '#eff6ff', // bg-blue-50
        color: '#2563eb' // text-blue-600
    };

    return (
        <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-30">
            <div className="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <a href="https://www.milanotriathlonteam.com/" target="_blank" rel="noopener noreferrer" className="hover:scale-105 transition-transform" title="Sito Ufficiale MTT">
                        <img src="/Logo.png" alt="MTT Logo" className="h-12 w-auto object-contain" />
                    </a>
                    <div className="flex flex-col">
                        <h1 className="text-xl font-black text-slate-800 tracking-tight leading-none uppercase">Fitri 2026</h1>
                        <span className="text-[10px] font-black text-blue-700 uppercase tracking-widest mt-1">
                            Atleta: {session?.user?.user_metadata?.full_name || session?.user?.email}
                        </span>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <NavLink to="/" end className="flex items-center gap-2 px-4 py-2 bg-slate-100 border border-slate-200 text-slate-600 rounded-2xl text-sm font-bold hover:bg-blue-50 hover:text-blue-600" style={({ isActive }: { isActive: boolean }) => isActive ? activeLinkStyle : undefined}>
                        <LayoutDashboard className="w-4 h-4" />
                        <span>Dashboard</span>
                    </NavLink>
                    <NavLink to="/calendario-team" className="flex items-center gap-2 px-4 py-2 bg-slate-100 border border-slate-200 text-slate-600 rounded-2xl text-sm font-bold hover:bg-blue-50 hover:text-blue-600" style={({ isActive }: { isActive: boolean }) => isActive ? activeLinkStyle : undefined}>
                        <Users className="w-4 h-4" />
                        <span>Team</span>
                    </NavLink>
                    
                    <div className="w-px h-6 bg-slate-200 mx-2"></div>
                    
                    {session?.user?.email === ADMIN_EMAIL && (
                        <button onClick={() => alert("Il pannello Admin è ora nella Dashboard.")} className="flex items-center gap-2 px-4 py-2 bg-amber-50 border border-amber-200 text-amber-800 rounded-2xl text-sm font-bold hover:bg-amber-100 transition-all"><Shield className="w-4 h-4" /> Admin</button>
                    )}
                    
                    <button onClick={handleLogout} className="flex items-center gap-2 px-4 py-2 bg-slate-100 border border-slate-200 text-slate-600 rounded-2xl text-sm font-bold hover:bg-red-50 hover:text-red-600 hover:border-red-100 transition-all" title="Logout"><LogOut className="w-4 h-4" /></button>
                </div>
            </div>
        </header>
    );
}

export default Header;
