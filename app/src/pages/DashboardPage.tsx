// ... (import e interfacce sono già corretti sopra)

// Ripopolo l'ultima parte del file DashboardPage.tsx assicurandomi che la sintassi sia perfetta.
// Questa sezione copre dalla fine della lista gare fino alla chiusura del componente.

            {/* FINE COLONNA DESTRA */}
        </div>

        {/* MODALE NOTE ATLETA */}
        {activeNoteRace && (
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in" role="dialog" aria-modal="true" aria-labelledby="note-modal-title">
                <div className="bg-white rounded-[2.5rem] p-8 max-w-md w-full shadow-2xl animate-in zoom-in-95">
                    <div className="flex justify-between items-start mb-6"><div className="bg-blue-50 p-3 rounded-2xl"><Edit3 className="w-6 h-6 text-blue-600" /></div><button onClick={() => setActiveNoteRace(null)} className="p-2 hover:bg-slate-100 rounded-xl transition-colors" aria-label="Chiudi diario di gara"><X className="w-5 h-5 text-slate-500" /></button></div>
                    <h3 id="note-modal-title" className="text-xl font-black text-slate-800 mb-1 uppercase tracking-tight">Diario di Gara</h3>
                    <label htmlFor="race-notes-textarea" className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6 block">{activeNoteRace.title}</label>
                    <textarea 
                        id="race-notes-textarea"
                        autoFocus 
                        className="w-full h-40 p-4 bg-slate-50 border-2 border-slate-100 rounded-2xl outline-none focus:border-blue-500 focus:bg-white transition-all text-sm font-bold text-slate-700 placeholder:text-slate-500" 
                        placeholder="Esempio: Obiettivo stare sotto le 2h15, gel ogni 45 min..." 
                        value={raceNotes[activeNoteRace.id] || ""} 
                        onChange={(e) => updateNote(activeNoteRace.id, e.target.value)} 
                    />
                    <button onClick={() => setActiveNoteRace(null)} className="w-full mt-8 py-4 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl text-xs font-black uppercase tracking-widest shadow-lg transition-all">Salva Note</button>
                </div>
            </div>
        )}

        {activeChecklistRace && (
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in" role="dialog" aria-modal="true" aria-labelledby="checklist-modal-title">
                <div className="bg-white rounded-[2.5rem] p-8 max-w-md w-full shadow-2xl animate-in zoom-in-95">
                    <div className="flex justify-between items-start mb-6"><div className="bg-emerald-50 p-3 rounded-2xl"><ShoppingBag className="w-6 h-6 text-emerald-600" /></div><button onClick={() => setActiveChecklistRace(null)} className="p-2 hover:bg-slate-100 rounded-xl transition-colors" aria-label="Chiudi checklist"><X className="w-5 h-5 text-slate-500" /></button></div>
                    <h3 id="checklist-modal-title" className="text-xl font-black text-slate-800 mb-6 uppercase tracking-tight">Checklist {activeChecklistRace.type}</h3>
                    <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">{getEquipment(activeChecklistRace.type).map((item, i) => (<div key={i} className="p-4 bg-slate-50 rounded-xl text-sm font-bold text-slate-600 flex items-center gap-3 border border-slate-100 hover:bg-white transition-all"><CheckCircle className="w-4 h-4 text-emerald-500" />{item}</div>))}</div>
                    <button onClick={() => setActiveChecklistRace(null)} className="w-full mt-8 py-4 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl text-xs font-black uppercase tracking-widest shadow-lg transition-all">Chiudi</button>
                </div>
            </div>
        )}

        {pendingConfirmId && (
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
                <div className="bg-white rounded-[2.5rem] p-8 max-w-md w-full text-center animate-in zoom-in-95 shadow-2xl">
                    <div className="bg-orange-50 w-16 h-16 rounded-3xl flex items-center justify-center mx-auto mb-6"><AlertTriangle className="w-8 h-8 text-orange-500" /></div>
                    <h3 className="text-xl font-black mb-4 uppercase">Gara molto vicina!</h3><p className="text-slate-500 mb-8 font-medium">Hai meno di 3 giorni di recupero. Vuoi procedere?</p>
                    <div className="flex gap-3"><button onClick={() => setPendingConfirmId(null)} className="flex-1 py-4 bg-slate-100 hover:bg-slate-200 rounded-2xl font-black text-xs uppercase transition-all">Annulla</button><button onClick={() => addRaceFinal(pendingConfirmId)} className="flex-1 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black text-xs uppercase shadow-lg transition-all">Conferma</button></div>
                </div>
            </div>
        )}

        {/* TEMPLATE SOCIAL STAGIONALE */}
        <div style={{ position: 'absolute', left: '-9999px', top: 0 }}>
            <div ref={cardRef} className="w-[1080px] min-h-[1920px] bg-slate-900 p-20 flex flex-col text-white font-sans relative overflow-hidden">
                <div className="absolute top-0 right-0 p-10 opacity-5"><img src="/Logo.png" alt="" className="w-[800px] h-auto grayscale brightness-200" /></div>
                <div className="flex items-center justify-between mb-20 border-b-4 border-red-600 pb-10 relative z-10">
                    <div className="flex items-center gap-8"><div className="bg-red-600 p-6 rounded-[2.5rem] rotate-3 shadow-2xl"><img src="/Logo.png" alt="" className="w-20 h-auto grayscale brightness-200" /></div><div><h1 className="text-7xl font-black tracking-tighter uppercase leading-none mb-2">My 2026 Season</h1><p className="text-2xl font-bold text-red-500 uppercase tracking-[0.5em]">MTT Milano Triathlon Team</p></div></div>
                    <div className="text-right text-9xl font-black text-white/10 leading-none">2026</div>
                </div>
                <div className="flex-1 space-y-10 relative z-10">
                    {myPlan.slice(0, 10).map((race) => (
                        <div key={race.id} className={`p-10 rounded-[3rem] flex items-center justify-between border-4 transition-all ${racePriorities[race.id] === 'A' ? 'bg-yellow-500/10 border-yellow-500' : 'bg-white/5 border-white/5'}`}>
                            <div className="flex items-center gap-10">
                                <div className="flex flex-col items-center justify-center bg-white/10 w-28 h-28 rounded-[2rem] border-2 border-white/10"><span className="text-sm font-black uppercase text-blue-400">{race.date.split('-')[1]}</span><span className="text-4xl font-black">{race.date.split('-')[0]}</span></div>
                                <div className="space-y-2">
                                    {racePriorities[race.id] === 'A' && <div className="flex items-center gap-2 text-yellow-500 mb-2"><Star className="w-6 h-6 fill-current" /><span className="text-xl font-black uppercase tracking-widest">Main Objective</span></div>}
                                    {race.event && <div className="text-xl font-black text-white/40 uppercase tracking-[0.2em] mb-1">{race.event}</div>}
                                    <h2 className="text-4xl font-black leading-tight max-w-2xl">{race.title}</h2>
                                    <div className="flex items-center gap-4 text-white/40 text-xl font-bold"><MapPin className="w-6 h-6" /><span>{race.location} • {race.region}</span></div>
                                </div>
                            </div>
                            <div className="flex flex-col items-end gap-4"><span className={`px-10 py-4 rounded-3xl text-3xl font-black uppercase ${race.type === 'Triathlon' ? 'bg-blue-600' : 'bg-orange-600'}`}>{race.type}</span></div>
                        </div>
                    ))}
                </div>
                <div className="mt-20 pt-10 border-t-2 border-white/10 flex justify-between items-end opacity-40 relative z-10"><div className="text-xl font-bold"><p>Generato da MTT Season Planner</p><p className="text-red-500 uppercase tracking-widest">www.milanotriathlonteam.com</p></div><div className="flex items-center gap-4"><img src="/Logo.png" alt="" className="w-10 h-auto grayscale brightness-200" /><span className="text-4xl font-black uppercase italic">Ready to Race</span></div></div>
            </div>
        </div>

        {/* TEMPLATE SOCIAL SINGOLA GARA */}
        <div style={{ position: 'absolute', left: '-9999px', top: 0 }}>
            {activeSingleRace && (
                <div ref={singleCardRef} className="w-[1080px] h-[1080px] bg-slate-900 p-20 flex flex-col items-center justify-center text-white font-sans relative overflow-hidden text-center">
                    <div className="absolute top-0 right-0 p-10 opacity-5"><img src="/Logo.png" alt="" className="w-[600px] h-auto grayscale brightness-200" /></div>
                    <div className="z-10 space-y-10">
                        <div className="bg-red-600 px-8 py-3 rounded-full inline-block mb-4 shadow-2xl"><span className="text-2xl font-black uppercase tracking-[0.5em]">Next Challenge</span></div>
                        <div className="space-y-4"><h1 className="text-8xl font-black tracking-tighter leading-none uppercase drop-shadow-2xl">{activeSingleRace.event || activeSingleRace.title}</h1><p className="text-4xl font-bold text-red-500 uppercase tracking-[0.3em]">MTT Milano Triathlon Team</p></div>
                        <div className="flex flex-col items-center gap-6 pt-10"><div className="flex items-center gap-6 bg-white/10 px-10 py-6 rounded-[2.5rem] border-2 border-white/10 shadow-xl"><Calendar className="w-12 h-12 text-blue-400" /><span className="text-6xl font-black">{activeSingleRace.date}</span></div><div className="flex items-center gap-4 text-white/60 text-3xl font-bold"><MapPin className="w-10 h-10" /><span>{activeSingleRace.location} • {activeSingleRace.region}</span></div></div>
                        <div className="pt-10 flex gap-6 justify-center">
                            <span className={`px-10 py-4 rounded-3xl text-3xl font-black uppercase shadow-lg ${activeSingleRace.type === 'Triathlon' ? 'bg-blue-600' : 'bg-orange-600'}`}>{activeSingleRace.type}</span>
                            {activeSingleRace.distance && <span className="px-10 py-4 bg-slate-700 rounded-3xl text-3xl font-black uppercase tracking-widest shadow-lg">{activeSingleRace.distance}</span>}
                        </div>
                    </div>
                    <div className="absolute bottom-10 left-0 right-0 text-center opacity-30 text-xl font-bold">www.milanotriathlonteam.com</div>
                </div>
            )}
        </div>
    </div>
  );
};

export default DashboardPage;
