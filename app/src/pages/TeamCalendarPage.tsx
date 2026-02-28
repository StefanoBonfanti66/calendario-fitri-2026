/**
 * MTT Season Planner 2026 - Team Calendar
 * Author: Stefano Bonfanti
 */
import React, { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { User, Calendar, Users } from 'lucide-react';

interface TeamRace {
  race_id: string;
  race_title: string;
  race_date: string;
  participants: string[];
}

interface TeamMonth {
  month_key: string;
  races: TeamRace[];
}

const TeamCalendarPage: React.FC = () => {
  const [teamCalendar, setTeamCalendar] = useState<TeamMonth[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeamCalendar = async () => {
      const { data, error } = await supabase.rpc('get_team_calendar');
      
      if (error) {
        console.error("Errore nel caricare il calendario del team:", error);
      } else {
        setTeamCalendar(data);
      }
      setLoading(false);
    };

    fetchTeamCalendar();
  }, []);

  const getMonthName = (monthKey: string) => {
    const [year, month] = monthKey.split('-');
    return new Date(parseInt(year), parseInt(month) - 1, 1).toLocaleString('it-IT', { month: 'long', year: 'numeric' });
  };

  if (loading) {
    return <div className="text-center p-10 font-bold text-slate-500">Caricamento calendario team...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center gap-4 mb-10">
        <div className="bg-blue-500 p-4 rounded-3xl text-white shadow-lg">
          <Users className="w-8 h-8" />
        </div>
        <div>
          <h1 className="text-3xl font-black text-slate-800 tracking-tight uppercase">Calendario Team</h1>
          <p className="text-slate-600 font-bold text-sm">Le gare pianificate da tutti gli atleti MTT.</p>
        </div>
      </div>

      <div className="space-y-12">
        {teamCalendar.map((month) => (
          <div key={month.month_key}>
            <h2 className="text-xl font-black text-red-600 uppercase tracking-widest mb-6 pb-3 border-b-2 border-red-100 flex items-center gap-3">
              <Calendar className="w-5 h-5" />
              {getMonthName(month.month_key)}
            </h2>
            <div className="space-y-6">
              {month.races.map((race) => (
                <div key={race.race_id} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:border-blue-100 transition-colors">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="font-black text-slate-800 text-lg leading-tight">{race.race_title}</h3>
                    <div className="bg-blue-50 px-3 py-1 rounded-full border border-blue-100 shrink-0">
                      <span className="text-[11px] font-black text-blue-700">{race.race_date}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-slate-500" />
                    <div className="flex flex-wrap gap-2">
                      {race.participants.map((name, i) => (
                        <span key={i} className="text-xs font-bold bg-slate-100 text-slate-700 px-2 py-1 rounded-md border border-slate-200">
                          {name}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TeamCalendarPage;
