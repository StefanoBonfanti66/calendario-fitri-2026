import React, { useState, useEffect, useMemo, useTransition, useCallback } from "react";
import { 
  Search, Plus, Calendar, MapPin, Trash2, CheckCircle, Trophy, Filter, 
  Info, Download, Upload, Bike, Map as MapIcon, ChevronRight, Star, ExternalLink, Activity, Navigation, List, AlertTriangle, X, Camera, Image, ShoppingBag
} from "lucide-react";
import { toPng } from 'html-to-image';
import racesData from "./races_full.json";
import { provinceCoordinates } from "./coords";
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './map.css';

interface Race {
  id: string;
  date: string;
  title: string;
  event?: string;
  location: string;
  region: string;
  type: string;
  distance: string;
  rank: string;
  category: string;
  link?: string;
  mapCoords?: [number, number];
  distanceFromHome?: number | null;
}

const getEquipment = (type: string) => {
    const base = ["Chip", "Body MTT", "Pettorale", "Gel", "Documento", "Tessera"];
    if (type === 'Triathlon') return [...base, "Muta", "Occhialini", "Scarpe Bici", "Casco", "Scarpe Corsa"];
    if (type === 'Duathlon') return [...base, "Scarpe Bici", "Casco", "Scarpe Corsa"];
    if (type.includes('Winter')) return [...base, "Termica", "Guanti", "Scarpe/Sci"];
    if (type === 'Cross') return [...base, "MTB", "Casco", "Scarpe Trail"];
    return base;
};

// Componente Card memoizzato per massime performance
const RaceCard = React.memo(({ 
    race, 
    isSelected, 
    priority, 
    cost, 
    onToggle, 
    onPriority, 
    onCost,
    onSingleCard,
    onChecklist,
    getRankColor 
}: { 
    race: Race, 
    isSelected: boolean, 
    priority: string, 
    cost: number, 
    onToggle: (id: string) => void,
    onPriority: (id: string, p: string) => void,
    onCost: (id: string, c: number) => void,
    onSingleCard: (race: Race) => void,
    onChecklist: (race: Race) => void,
    getRankColor: (r: string) => string
}) => {
    return (
        <div 
            className={`group bg-white p-6 rounded-[2.5rem] border-2 transition-all duration-300 hover:shadow-xl hover:shadow-slate-200/50 flex flex-col ${
                isSelected 
                ? 'border-blue-500 ring-4 ring-blue-50 shadow-lg shadow-blue-100/50' 
                : 'border-white hover:border-blue-100 shadow-sm'
            } ${priority === 'A' ? 'bg-yellow-50/20 border-yellow-100' : ''}`}
        >
            <div className="flex justify-between items-start mb-5">
                <div className="flex flex-col gap-1">
                    <div className="flex items-center gap-2 bg-slate-50 px-3 py-1.5 rounded-full w-fit">
                        <Calendar className="w-3.5 h-3.5 text-blue-500" />
                        <span className="text-[11px] font-black text-slate-700">{race.date}</span>
                    </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                    <span className={`text-[9px] font-black uppercase px-3 py-1.5 rounded-xl tracking-wider ${
                        race.type === 'Triathlon' ? 'bg-blue-100 text-blue-700' :
                        race.type === 'Duathlon' ? 'bg-orange-100 text-orange-700' :
                        race.type.includes('Winter') ? 'bg-cyan-100 text-cyan-700' :
                        'bg-emerald-100 text-emerald-700'
                    }`}>
                        {race.type}
                    </span>
                    {race.rank && (
                        <div className={`flex items-center gap-1 text-[9px] font-black uppercase px-2 py-1 rounded-lg border-2 ${getRankColor(race.rank)}`}>
                            <Star className="w-2.5 h-2.5 fill-current" />
                            {race.rank}
                        </div>
                    )}
                </div>
            </div>
            
            {race.event && (
                <div className="text-sm font-black text-slate-600 uppercase tracking-wide mb-1.5 truncate">
                    {race.event}
                </div>
            )}
            <h3 className="font-black text-slate-800 text-lg mb-3 leading-[1.2] group-hover:text-blue-600 transition-colors">
                {race.title}
            </h3>
            
            <div className="space-y-2 mb-6">
                <div className="flex items-start gap-2.5">
                    <MapPin className="w-4 h-4 text-slate-300 mt-0.5 shrink-0" />
                    <div className="flex flex-col">
                        <p className="text-xs font-bold text-slate-500 leading-snug">
                            {race.location}
                        </p>
                        <span className="text-blue-400/70 text-[10px] font-bold uppercase tracking-tighter">{race.region}</span>
                    </div>
                </div>
                <div className="flex items-center gap-4">
                    {race.distance && (
                        <div className="flex items-center gap-2">
                            <Bike className="w-4 h-4 text-slate-300 shrink-0" />
                            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{race.distance}</span>
                        </div>
                    )}
                    {race.distanceFromHome !== undefined && race.distanceFromHome !== null && (
                        <div className="flex items-center gap-2 bg-blue-50/50 px-2 py-1 rounded-lg border border-blue-100/50">
                            <Navigation className="w-3 h-3 text-blue-400" />
                            <span className="text-[10px] font-black text-blue-600 uppercase">~{race.distanceFromHome} KM</span>
                        </div>
                    )}
                </div>
            </div>
            
            <div className="flex items-center justify-between mt-auto pt-5 border-t border-slate-50">
                <div className="flex flex-col gap-2">
                    {race.category ? (
                        <span className="text-[10px] font-black text-slate-500 bg-slate-100 border border-slate-200 px-2 py-1 rounded-lg uppercase tracking-wider w-fit">
                            {race.category}
                        </span>
                    ) : <div></div>}
                    
                    {isSelected && (
                        <div className="flex items-center gap-2">
                            <div className="flex items-center gap-1 bg-slate-50 p-1 rounded-xl border border-slate-100 w-fit relative group/legend">
                                {['A', 'B', 'C'].map(p => (
                                    <button
                                        key={p}
                                        onClick={(e) => { e.stopPropagation(); onPriority(race.id, p); }}
                                        className={`w-7 h-7 rounded-lg text-[10px] font-black transition-all ${
                                            priority === p
                                            ? (p === 'A' ? 'bg-yellow-400 text-white shadow-sm' : p === 'B' ? 'bg-blue-400 text-white shadow-sm' : 'bg-slate-400 text-white shadow-sm')
                                            : 'text-slate-400 hover:bg-white'
                                        }`}
                                    >
                                        {p}
                                    </button>
                                ))}
                                <div className="absolute bottom-full left-0 mb-2 w-48 p-3 bg-slate-900 text-white text-[9px] rounded-xl opacity-0 invisible group-hover/legend:opacity-100 group-hover/legend:visible transition-all z-50 shadow-xl border border-white/10">
                                    <p className="mb-1.5"><b className="text-yellow-400">A: OBIETTIVO</b> - Gara principale, scarico totale.</p>
                                    <p className="mb-1.5"><b className="text-blue-400">B: PREPARAZIONE</b> - Test di forma, scarico parziale.</p>
                                    <p><b>C: ALLENAMENTO</b> - Gara test senza scarico.</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-2 bg-slate-50 px-2 py-1 rounded-lg border border-slate-100 w-fit h-9">
                                <span className="text-[9px] font-black text-slate-400 uppercase">€</span>
                                <input 
                                    type="number" 
                                    placeholder="0"
                                    className="bg-transparent border-none outline-none text-[10px] font-black text-slate-600 w-10 text-center"
                                    value={cost || ''}
                                    onChange={(e) => onCost(race.id, parseFloat(e.target.value) || 0)}
                                />
                            </div>
                            <button
                                onClick={(e) => { e.stopPropagation(); onSingleCard(race); }}
                                className="p-2 rounded-lg text-slate-400 hover:text-blue-600 hover:bg-white transition-all shadow-sm"
                                title="Genera Post Instagram"
                            >
                                <Image className="w-4 h-4" />
                            </button>
                            <button
                                onClick={(e) => { e.stopPropagation(); onChecklist(race); }}
                                className="p-2 rounded-lg text-slate-400 hover:text-emerald-600 hover:bg-white transition-all shadow-sm"
                                title="Checklist Attrezzatura"
                            >
                                <ShoppingBag className="w-4 h-4" />
                            </button>
                        </div>
                    )}
                </div>
                
                <div className="flex items-center gap-2">
                    {race.link && (
                        <a 
                            href={race.link} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="p-3 rounded-[1.25rem] text-blue-600 bg-blue-50 hover:bg-blue-100 transition-colors shadow-sm"
                            title="Scheda Ufficiale MyFITri"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <ExternalLink className="w-4 h-4" />
                        </a>
                    )}
                    <button
                        onClick={() => onToggle(race.id)}
                        className={`flex items-center gap-2 px-6 py-3 rounded-[1.25rem] text-xs font-black uppercase tracking-widest transition-all duration-300 ${
                            isSelected
                            ? 'bg-red-50 text-red-600 hover:bg-red-100'
                            : 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-200 hover:-translate-y-0.5 active:translate-y-0'
                        }`}
                    >
                        {isSelected ? (
                            <><Trash2 className="w-3.5 h-3.5" /> Rimuovi</>
                        ) : (
                            <><Plus className="w-3.5 h-3.5" /> Aggiungi</>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
});

const App: React.FC = () => {
  const [isPending, startTransition] = useTransition();
  const cardRef = React.useRef<HTMLDivElement>(null);
  const singleCardRef = React.useRef<HTMLDivElement>(null);
  const [activeSingleRace, setActiveSingleRace] = useState<Race | null>(null);
  const [activeChecklistRace, setActiveChecklistRace] = useState<Race | null>(null);
  const [racesState, setRacesState] = useState<Race[]>([]);
  const [selectedRaces, setSelectedRaces] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("Tutti");
  const [filterRegion, setFilterRegion] = useState("Tutte");
  const [filterDistance, setFilterDistance] = useState("Tutte");
  const [filterSpecial, setFilterSpecial] = useState<string[]>([]);
  const [filterRadius, setFilterRadius] = useState<number>(1000);
  const [homeCity, setHomeCity] = useState(localStorage.getItem("home_city") || "");
  const [viewMode, setViewMode] = useState<'list' | 'map'>('list');
  const [racePriorities, setRacePriorities] = useState<Record<string, string>>({});
  const [raceCosts, setRaceCosts] = useState<Record<string, number>>({});
  const [pendingConfirmId, setPendingConfirmId] = useState<string | null>(null);

  const getDistance = useCallback((targetLocation: string, home: string) => {
    if (!home) return null;
    const provinceMatch = targetLocation.match(/\((.*?)\)/);
    const targetProvince = provinceMatch ? provinceMatch[1] : targetLocation;
    const startCoords = provinceCoordinates[home];
    const endCoords = provinceCoordinates[targetProvince];
    if (!startCoords || !endCoords) return null;
    const R = 6371;
    const dLat = (endCoords[0] - startCoords[0]) * Math.PI / 180;
    const dLon = (endCoords[1] - startCoords[1]) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(startCoords[0] * Math.PI / 180) * Math.cos(endCoords[0] * Math.PI / 180) * Math.sin(dLon/2) * Math.sin(dLon/2);
    return Math.round(R * (2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))) * 1.2);
  }, []);

  const races = useMemo(() => {
    const source = racesState.length > 0 ? racesState : (racesData as Race[]);
    return source.map(race => {
      const cityName = race.location.split('(')[0].trim();
      let coords = provinceCoordinates[cityName];
      if (!coords) {
        const provinceMatch = race.location.match(/\((.*?)\)/);
        const province = provinceMatch ? provinceMatch[1] : race.location;
        coords = provinceCoordinates[province];
      }
      let mapCoords: [number, number] | undefined = undefined;
      if (coords) {
        const num = parseInt(race.id) || 0;
        mapCoords = [coords[0] + (((num % 10) - 5) * 0.005), coords[1] + ((((num * 7) % 10) - 5) * 0.005)];
      }
      return { ...race, mapCoords, distanceFromHome: getDistance(race.location, homeCity) };
    });
  }, [racesState, homeCity, getDistance]);

  const myPlan = useMemo(() => {
    return races.filter((r) => selectedRaces.includes(r.id))
        .sort((a,b) => {
            const dateA = a.date.split("-").reverse().join("-");
            const dateB = b.date.split("-").reverse().join("-");
            return dateA.localeCompare(dateB);
        });
  }, [races, selectedRaces]);

  const budgetTotals = useMemo(() => {
    const registration = myPlan.reduce((acc, r) => acc + (raceCosts[r.id] || 0), 0);
    let travel = 0;
    myPlan.forEach(r => { if (r.distanceFromHome) travel += (r.distanceFromHome * 2) * 0.25; });
    return { registration, travel, total: registration + travel };
  }, [myPlan, raceCosts]);

  const seasonStats = useMemo(() => {
    const priorities = { A: 0, B: 0, C: 0 };
    const types: Record<string, number> = {};
    let totalKm = 0;
    myPlan.forEach(r => {
        const p = racePriorities[r.id] || 'C';
        if (p === 'A') priorities.A++; else if (p === 'B') priorities.B++; else priorities.C++;
        types[r.type] = (types[r.type] || 0) + 1;
        if (r.distanceFromHome) totalKm += (r.distanceFromHome * 2);
    });
    return { priorities, types, totalKm };
  }, [myPlan, racePriorities]);

  const nextObjective = useMemo(() => {
    const now = new Date();
    return myPlan.find(r => {
        const p = racePriorities[r.id] || 'C';
        if (p !== 'A') return false;
        const [d, m, y] = r.date.split("-");
        return new Date(parseInt(y), parseInt(m)-1, parseInt(d)) > now;
    });
  }, [myPlan, racePriorities]);

  const [timeLeft, setTimeLeft] = useState<{days: number, hours: number, mins: number} | null>(null);

  useEffect(() => {
    if (!nextObjective) { setTimeLeft(null); return; }
    const update = () => {
        const [d, m, y] = nextObjective.date.split("-");
        const diff = new Date(parseInt(y), parseInt(m)-1, parseInt(d)).getTime() - new Date().getTime();
        if (diff > 0) setTimeLeft({ days: Math.floor(diff / 86400000), hours: Math.floor((diff % 86400000) / 3600000), mins: Math.floor((diff % 3600000) / 60000) });
    };
    update();
    const t = setInterval(update, 60000);
    return () => clearInterval(t);
  }, [nextObjective]);

  const getCachedIcon = useMemo(() => {
    const cache: Record<string, L.DivIcon> = {};
    ['Triathlon', 'Duathlon', 'Winter', 'Cross'].forEach(t => {
      [undefined, 'A'].forEach(p => {
        [true, false].forEach(s => {
          let color = '#3b82f6';
          if (t === 'Duathlon') color = '#f97316';
          if (t.includes('Winter')) color = '#06b6d4';
          if (t === 'Cross') color = '#10b981';
          if (s) color = '#ef4444';
          if (p === 'A') color = '#eab308';
          cache[`${t}-${p}-${s}`] = L.divIcon({
            className: 'custom-div-icon',
            html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: white; font-size: 8px; font-weight: 900;">${p === 'A' ? 'A' : ''}</div>`,
            iconSize: [14, 14],
            iconAnchor: [7, 7]
          });
        });
      });
    });
    return (type: string, isSelected: boolean, priority?: string) => {
        const key = `${type.includes('Winter') ? 'Winter' : type}-${priority === 'A' ? 'A' : 'undefined'}-${isSelected}`;
        return cache[key] || cache['Triathlon-undefined-false'];
    };
  }, []);

  const handleViewChange = (mode: 'list' | 'map') => { startTransition(() => setViewMode(mode)); };

  const regions = useMemo(() => {
    const r = new Set(races.map(race => race.region).filter(Boolean));
    return ["Tutte", ...Array.from(r).sort()];
  }, [races]);

  const distances = useMemo(() => {
    const d = new Set(races.map(race => race.distance).filter(Boolean));
    return ["Tutte", ...Array.from(d).sort()];
  }, [races]);

  useEffect(() => {
    const saved = localStorage.getItem("selected_races");
    if (saved) try { setSelectedRaces(JSON.parse(saved)); } catch (e) {}
    const savedPriorities = localStorage.getItem("race_priorities");
    if (savedPriorities) try { setRacePriorities(JSON.parse(savedPriorities)); } catch (e) {}
    const savedCosts = localStorage.getItem("race_costs");
    if (savedCosts) try { setRaceCosts(JSON.parse(savedCosts)); } catch (e) {}
  }, []);

  useEffect(() => {
    localStorage.setItem("selected_races", JSON.stringify(selectedRaces));
    localStorage.setItem("race_priorities", JSON.stringify(racePriorities));
    localStorage.setItem("race_costs", JSON.stringify(raceCosts));
  }, [selectedRaces, racePriorities, raceCosts]);

  const setPriority = useCallback((id: string, p: string) => { setRacePriorities(prev => ({ ...prev, [id]: p })); }, []);
  const updateCost = useCallback((id: string, cost: number) => { setRaceCosts(prev => ({ ...prev, [id]: cost })); }, []);

  const addRaceFinal = useCallback((id: string) => {
    setSelectedRaces((prev) => [...prev, id]);
    setRacePriorities(prev => ({ ...prev, [id]: 'C' }));
    setPendingConfirmId(null);
  }, []);

  const toggleRace = useCallback((id: string) => {
    if (selectedRaces.includes(id)) {
      setSelectedRaces((prev) => prev.filter((r) => r !== id));
      setRacePriorities(prev => { const next = {...prev}; delete next[id]; return next; });
      return;
    }
    const newRace = races.find(r => r.id === id);
    if (newRace) {
      const [nd, nm, ny] = newRace.date.split("-");
      const diffDays = Math.ceil(Math.abs(new Date(parseInt(ny), parseInt(nm) - 1, parseInt(nd)).getTime() - 0) / 86400000); // Semplificato per brevità qui
      const tooClose = myPlan.some(r => {
          const [rd, rm, ry] = r.date.split("-");
          return Math.ceil(Math.abs(new Date(parseInt(ny), parseInt(nm) - 1, parseInt(nd)).getTime() - new Date(parseInt(ry), parseInt(rm) - 1, parseInt(rd)).getTime()) / 86400000) < 3;
      });
      if (tooClose) { setPendingConfirmId(id); return; }
    }
    addRaceFinal(id);
  }, [selectedRaces, races, myPlan, addRaceFinal]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const imported = JSON.parse(event.target?.result as string);
          if (Array.isArray(imported)) { setRacesState(imported); alert("Gare caricate!"); }
        } catch (err) { alert("Errore JSON."); }
      };
      reader.readAsText(file);
    }
  };

  const exportPlan = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(myPlan, null, 2));
    const a = document.createElement('a'); a.setAttribute("href", dataStr); a.setAttribute("download", "mio_piano_mtt_2026.json"); a.click();
  };

  const exportToICS = () => {
    if (myPlan.length === 0) return;
    let ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Fitri Planner//IT", "CALSCALE:GREGORIAN", "METHOD:PUBLISH"];
    myPlan.forEach(race => {
      const [d, m, y] = race.date.split("-");
      const start = `${y}${m}${d}`;
      const end = new Date(parseInt(y), parseInt(m) - 1, parseInt(d) + 1).toISOString().slice(0, 10).replace(/-/g, "");
      ics.push("BEGIN:VEVENT", `UID:${race.id}@mtt`, `DTSTART;VALUE=DATE:${start}`, `DTEND;VALUE=DATE:${end}`, `SUMMARY:${race.title}`, `LOCATION:${race.location}`, `DESCRIPTION:Priorità: ${racePriorities[race.id] || 'C'}`, "END:VEVENT");
    });
    ics.push("END:VCALENDAR");
    const blob = new Blob([ics.join("\r\n")], { type: "text/calendar" });
    const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.setAttribute("download", "gare_mtt_2026.ics"); link.click();
  };

  const exportToCSV = () => {
    if (myPlan.length === 0) return;
    const headers = ["Data", "Evento", "Specialità", "Località", "Regione", "Sport", "Distanza", "Priorità", "Costo", "Km"];
    const rows = myPlan.map(r => [r.date, r.event || "", r.title, r.location, r.region, r.type, r.distance, racePriorities[r.id] || 'C', raceCosts[r.id] || 0, r.distanceFromHome || ""]);
    const csv = [headers, ...rows].map(e => e.join(",")).join("\n");
    const blob = new Blob(["\ufeff" + csv], { type: 'text/csv' });
    const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.setAttribute("download", "piano_mtt_2026.csv"); link.click();
  };

  const filteredRaces = useMemo(() => {
    return races.filter((race) => {
        const matchesSearch = (race.title?.toLowerCase() || "").includes(searchTerm.toLowerCase()) || (race.location?.toLowerCase() || "").includes(searchTerm.toLowerCase());
        const matchesType = filterType === "Tutti" || race.type === filterType || (race.type === "Winter" && filterType === "Winter");
        const matchesRegion = filterRegion === "Tutte" || race.region === filterRegion;
        const matchesDistance = filterDistance === "Tutte" || race.distance === filterDistance;
        const matchesSpecial = filterSpecial.length === 0 || filterSpecial.some(s => (race.category?.toLowerCase() || "").includes(s.toLowerCase()) || (race.title?.toLowerCase() || "").includes(s.toLowerCase()) || (race.event?.toLowerCase() || "").includes(s.toLowerCase()));
        const matchesRadius = filterRadius >= 1000 || !race.distanceFromHome || race.distanceFromHome <= filterRadius;
        return matchesSearch && matchesType && matchesRegion && matchesDistance && matchesSpecial && matchesRadius;
    }).sort((a,b) => a.date.split("-").reverse().join("-").localeCompare(b.date.split("-").reverse().join("-")));
  }, [races, searchTerm, filterType, filterRegion, filterDistance, filterSpecial, filterRadius]);

  const getRankColor = useCallback((rank: string) => {
    if (rank === 'Gold') return 'text-yellow-500 bg-yellow-50 border-yellow-100';
    if (rank === 'Silver') return 'text-slate-400 bg-slate-50 border-slate-100';
    return 'text-orange-400 bg-orange-50 border-orange-100';
  }, []);

  const generateRaceCard = async () => {
    if (cardRef.current) {
        const dataUrl = await toPng(cardRef.current, { backgroundColor: '#0f172a' });
        const link = document.createElement('a'); link.download = `stagione-mtt-2026.png`; link.href = dataUrl; link.click();
    }
  };

  const generateSingleRaceCard = async (race: Race) => {
    setActiveSingleRace(race);
    setTimeout(async () => {
        if (singleCardRef.current) {
            const dataUrl = await toPng(singleCardRef.current, { backgroundColor: '#0f172a', width: 1080, height: 1080 });
            const link = document.createElement('a'); link.download = `challenge-${race.id}.png`; link.href = dataUrl; link.click();
            setActiveSingleRace(null);
        }
    }, 100);
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans selection:bg-blue-100">
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-br from-red-500 to-red-600 p-2.5 rounded-2xl text-white shadow-lg shadow-red-100 rotate-3"><Trophy className="w-6 h-6" /></div>
            <div>
              <h1 className="text-xl font-black text-slate-800 tracking-tight leading-none uppercase">Fitri 2026</h1>
              <span className="text-[10px] font-bold text-red-500 uppercase tracking-[0.2em]">MTT Milano Triathlon Team</span>
            </div>
          </div>
          <div className="flex gap-2">
            <button onClick={exportToICS} disabled={myPlan.length === 0} className="flex items-center gap-2 px-4 py-2 bg-blue-50 border border-blue-200 text-blue-600 rounded-2xl text-sm font-bold disabled:opacity-50"><Calendar className="w-4 h-4" /> <span className="hidden xs:inline">Calendario</span></button>
            <button onClick={exportToCSV} disabled={myPlan.length === 0} className="flex items-center gap-2 px-4 py-2 bg-emerald-50 border border-emerald-200 text-emerald-600 rounded-2xl text-sm font-bold disabled:opacity-50"><Download className="w-4 h-4" /> <span className="hidden xs:inline">Excel</span></button>
            <label className="flex items-center gap-2 px-5 py-2.5 bg-slate-900 text-white rounded-2xl text-sm font-bold cursor-pointer shadow-xl shadow-slate-200">
              <Upload className="w-4 h-4" /> <span className="hidden xs:inline">Importa</span>
              <input type="file" className="hidden" accept=".json" onChange={handleFileUpload} />
            </label>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 sticky top-28">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center gap-2"><Filter className="w-4 h-4 text-blue-500" /> Filtri</h2>
                <button onClick={() => { setSearchTerm(""); setFilterType("Tutti"); setFilterRegion("Tutte"); setFilterDistance("Tutte"); setFilterSpecial([]); setFilterRadius(1000); }} className="text-[10px] font-bold text-blue-600 hover:underline">Reset</button>
            </div>
            
            <div className="space-y-5">
              <div className="relative group">
                <Search className="absolute left-4 top-3.5 w-5 h-5 text-slate-300" />
                <input type="text" placeholder="Cerca gara..." className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border-2 border-transparent rounded-2xl focus:border-blue-500 outline-none text-sm font-medium" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
              </div>

              {homeCity && (
                  <div>
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2 flex justify-between"><span>Raggio d'azione</span><span className="text-blue-600">{filterRadius >= 1000 ? 'Illimitato' : `${filterRadius} km`}</span></label>
                    <input type="range" min="50" max="1000" step="50" value={filterRadius} onChange={(e) => setFilterRadius(parseInt(e.target.value))} className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-blue-600" />
                  </div>
              )}

              <div>
                <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Sport</label>
                <div className="flex flex-wrap gap-2">
                    {["Tutti", "Triathlon", "Duathlon", "Winter", "Cross"].map((t) => (
                    <button key={t} onClick={() => setFilterType(t)} className={`px-3 py-1.5 rounded-xl text-[10px] font-black uppercase transition-all ${(filterType === t) ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-500"}`}>{t}</button>
                    ))}
                </div>
              </div>

              <div>
                <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Settori Speciali</label>
                <div className="flex flex-wrap gap-2">
                    {["Paratriathlon", "Kids", "Youth"].map((s) => (
                    <button key={s} onClick={() => { setFilterSpecial(prev => prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s]); }} className={`px-3 py-1.5 rounded-xl text-[10px] font-black uppercase transition-all ${(filterSpecial.includes(s)) ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-500"}`}>{s}</button>
                    ))}
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                  <div>
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">La tua provincia</label>
                    <select value={homeCity} onChange={(e) => { setHomeCity(e.target.value); localStorage.setItem("home_city", e.target.value); }} className="w-full p-2.5 bg-slate-50 border-none rounded-xl text-xs font-bold outline-none cursor-pointer">
                        <option value="">Seleziona...</option>
                        {Object.keys(provinceCoordinates).sort().map(p => <option key={p} value={p}>{p}</option>)}
                    </select>
                  </div>
              </div>
            </div>

            <div className="mt-10 pt-10 border-t border-slate-100">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-black text-slate-800">Il Tuo Anno <span className="text-blue-600">({myPlan.length})</span></h2>
                    <div className="flex gap-2">
                        <span title="Race Card"><Camera className="w-4 h-4 text-slate-400 cursor-pointer hover:text-blue-600" onClick={generateRaceCard} /></span>
                    </div>
                </div>
                
                <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                    {myPlan.map((race, index) => (
                    <div key={race.id} className={`p-4 rounded-2xl border transition-all ${racePriorities[race.id] === 'A' ? 'border-yellow-200 bg-yellow-50/30' : 'border-slate-100 bg-white'}`}>
                        <div className="flex justify-between items-start">
                            <div className="space-y-1">
                                <div className="flex items-center gap-2">
                                    <span className="text-[10px] font-black text-blue-500">{race.date}</span>
                                    {racePriorities[race.id] && <span className="text-[8px] font-black px-1.5 py-0.5 rounded bg-slate-800 text-white">{racePriorities[race.id]}</span>}
                                </div>
                                <h4 className="text-xs font-bold text-slate-700 leading-tight">{race.title}</h4>
                            </div>
                            <button onClick={() => toggleRace(race.id)} className="text-slate-300 hover:text-red-500"><Trash2 className="w-4 h-4" /></button>
                        </div>
                    </div>
                    ))}
                </div>

                {myPlan.length > 0 && (
                    <div className="mt-6 pt-6 border-t border-slate-100 space-y-2 text-xs font-bold">
                        <div className="flex justify-between text-slate-500"><span>Iscrizioni</span><span>€ {budgetTotals.registration.toFixed(2)}</span></div>
                        <div className="flex justify-between text-emerald-600 text-sm font-black"><span>TOTALE STIMATO</span><span>€ {budgetTotals.total.toFixed(2)}</span></div>
                    </div>
                )}
            </div>
          </div>
        </div>

        <div className="lg:col-span-8 space-y-6">
            {nextObjective && timeLeft && (
                <div className="bg-gradient-to-r from-red-600 to-red-700 rounded-[3rem] p-8 text-white shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">
                    <div>
                        <span className="text-[10px] font-black uppercase tracking-widest opacity-60">Prossimo Obiettivo</span>
                        <h2 className="text-2xl font-black uppercase">{nextObjective.title}</h2>
                    </div>
                    <div className="flex gap-4 text-center">
                        <div><div className="text-3xl font-black">{timeLeft.days}</div><div className="text-[8px] font-bold uppercase opacity-60">Giorni</div></div>
                        <div className="text-2xl opacity-30">:</div>
                        <div><div className="text-3xl font-black">{timeLeft.hours}</div><div className="text-[8px] font-bold uppercase opacity-60">Ore</div></div>
                    </div>
                </div>
            )}

            <div className="flex items-center justify-between px-2">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">{filteredRaces.length} gare trovate</span>
                <div className="flex bg-slate-100 p-1 rounded-xl">
                    <button onClick={() => handleViewChange('list')} className={`px-4 py-1.5 rounded-lg text-[10px] font-black uppercase ${viewMode === 'list' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400'}`}>Lista</button>
                    <button onClick={() => handleViewChange('map')} className={`px-4 py-1.5 rounded-lg text-[10px] font-black uppercase ${viewMode === 'map' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400'}`}>Mappa</button>
                </div>
            </div>

            {viewMode === 'list' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {filteredRaces.map((race) => (
                        <RaceCard 
                            key={race.id}
                            race={race}
                            isSelected={selectedRaces.includes(race.id)}
                            priority={racePriorities[race.id] || 'C'}
                            cost={raceCosts[race.id] || 0}
                            onToggle={toggleRace}
                            onPriority={setPriority}
                            onCost={updateCost}
                            onSingleCard={generateSingleRaceCard}
                            onChecklist={setActiveChecklistRace}
                            getRankColor={getRankColor}
                        />
                    ))}
                </div>
            ) : (
                <div className="h-[600px] rounded-[3rem] overflow-hidden border-4 border-white shadow-xl">
                    <MapContainer center={[41.8719, 12.5674]} zoom={6} className="h-full w-full">
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                        {filteredRaces.map(race => race.mapCoords && (
                            <Marker key={race.id} position={race.mapCoords} icon={getCachedIcon(race.type, selectedRaces.includes(race.id), racePriorities[race.id])}>
                                <Popup>
                                    <div className="p-2 min-w-[150px]">
                                        <h4 className="font-bold text-sm">{race.title}</h4>
                                        <button onClick={() => toggleRace(race.id)} className="w-full mt-2 py-1 bg-blue-600 text-white rounded text-[10px] font-black uppercase">{selectedRaces.includes(race.id) ? 'Rimuovi' : 'Aggiungi'}</button>
                                    </div>
                                </Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                </div>
            )}
        </div>
      </main>

      {activeChecklistRace && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
              <div className="bg-white rounded-[2.5rem] p-8 max-w-md w-full shadow-2xl">
                  <h3 className="text-xl font-black text-slate-800 mb-6 uppercase">Checklist {activeChecklistRace.type}</h3>
                  <div className="space-y-3">{getEquipment(activeChecklistRace.type).map((item, i) => (<div key={i} className="p-3 bg-slate-50 rounded-xl text-sm font-bold text-slate-600 flex items-center gap-3"><div className="w-4 h-4 rounded border-2 border-slate-300"></div>{item}</div>))}</div>
                  <button onClick={() => setActiveChecklistRace(null)} className="w-full mt-8 py-4 bg-slate-900 text-white rounded-2xl text-xs font-black uppercase">Chiudi</button>
              </div>
          </div>
      )}

      {pendingConfirmId && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
              <div className="bg-white rounded-[2.5rem] p-8 max-w-md w-full text-center">
                  <h3 className="text-xl font-black mb-4">Gara molto vicina!</h3>
                  <p className="text-slate-500 mb-8 font-medium">Recupero inferiore a 3 giorni. Continuare?</p>
                  <div className="flex gap-3">
                      <button onClick={() => setPendingConfirmId(null)} className="flex-1 py-4 bg-slate-100 rounded-2xl font-black text-xs uppercase">Annulla</button>
                      <button onClick={() => addRaceFinal(pendingConfirmId)} className="flex-1 py-4 bg-blue-600 text-white rounded-2xl font-black text-xs uppercase">Conferma</button>
                  </div>
              </div>
          </div>
      )}

      {activeSingleRace && (
          <div style={{ position: 'absolute', left: '-9999px', top: 0 }}>
              <div ref={singleCardRef} className="w-[1080px] h-[1080px] bg-slate-900 p-20 flex flex-col items-center justify-center text-white text-center">
                  <h1 className="text-8xl font-black uppercase mb-10">{activeSingleRace.title}</h1>
                  <div className="text-4xl font-bold text-red-500 mb-10">MTT MILANO TRIATHLON TEAM</div>
                  <div className="text-6xl font-black bg-white/10 px-10 py-5 rounded-3xl">{activeSingleRace.date}</div>
              </div>
          </div>
      )}
    </div>
  );
};

export default App;
