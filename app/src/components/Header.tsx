import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import { Trophy, LogOut, Calendar, Download, Shield } from 'lucide-react';

const Header = ({ session }: { session: any }) => {
    const handleLogout = async () => {
        await supabase.auth.signOut();
    };

    const ADMIN_EMAIL = "bonfantistefano4@gmail.com";

    return (
        <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-30">
            <div className="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <a href="https://www.milanotriathlonteam.com/" target="_blank" rel="noopener noreferrer" className="bg-gradient-to-br from-red-500 to-red-600 p-2.5 rounded-2xl text-white shadow-lg rotate-3 hover:scale-110 transition-transform" title="Sito Ufficiale MTT"><Trophy className="w-6 h-6" /></a>
                    <div className="flex flex-col">
                        <h1 className="text-xl font-black text-slate-800 tracking-tight leading-none uppercase">Fitri 2026</h1>
                        <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest mt-1">
                            Atleta: {session?.user?.user_metadata?.full_name || session?.user?.email}
                        </span>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <Link to="/" className="flex items-center gap-2 px-4 py-2 bg-slate-100 border border-slate-200 text-slate-600 rounded-2xl text-sm font-bold hover:bg-blue-50 hover:text-blue-600">Dashboard</Link>
                    <Link to="/calendario-team" className="flex items-center gap-2 px-4 py-2 bg-slate-100 border border-slate-200 text-slate-600 rounded-2xl text-sm font-bold hover:bg-blue-50 hover:text-blue-600">Team</Link>
                    
                    <div className="w-px h-6 bg-slate-200 mx-2"></div>

                    {session?.user?.email === ADMIN_EMAIL && (
                        <button onClick={() => {}} className="flex items-center gap-2 px-4 py-2 bg-amber-50 border border-amber-200 text-amber-600 rounded-2xl text-sm font-bold hover:bg-amber-100 transition-all"><Shield className="w-4 h-4" /> Admin</button>
                    )}

                    <div className="w-px h-6 bg-slate-200 mx-2"></div>
                    
                    <button onClick={handleLogout} className="flex items-center gap-2 px-4 py-2 bg-slate-100 border border-slate-200 text-slate-600 rounded-2xl text-sm font-bold hover:bg-red-50 hover:text-red-600 hover:border-red-100 transition-all" title="Logout"><LogOut className="w-4 h-4" /></button>
                </div>
            </div>
        </header>
    );
}

export default Header;
