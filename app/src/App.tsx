import React, { useState, useEffect, useMemo, useTransition, useCallback } from "react";
import { 
  Search, Plus, Calendar, MapPin, Trash2, CheckCircle, Trophy, Filter, 
  Info, Download, Upload, Bike, Map as MapIcon, ChevronRight, Star, ExternalLink, Activity, Navigation, List, AlertTriangle, X
} from "lucide-react";
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
  mapCoords?: [number, number];
  distanceFromHome?: number | null;
}

const RaceCard = React.memo(({ 
    race, 
    isSelected, 
    priority, 
    cost, 
    onToggle, 
    onPriority, 
    onCost,
    getRankColor 
}: { 
    race: Race, 
    isSelected: boolean, 
    priority: string, 
    cost: number | string, 
    onToggle: (id: string) => void,
    onPriority: (id: string, p: string) => void,
    onCost: (id: string, c: number) => void,
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
                        </div>
                    )}
                </div>
                
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
    );
});

const App: React.FC = () => {
  const [isPending, startTransition] = useTransition();
  const [racesState, setRacesState] = useState<Race[]>([]);
  const [selectedRaces, setSelectedRaces] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("Tutti");
  const [filterRegion, setFilterRegion] = useState("Tutte");
  const [filterDistance, setFilterDistance] = useState("Tutte");
  const [homeCity, setHomeCity] = useState(localStorage.getItem("home_city") || "");
  const [viewMode, setViewMode] = useState<'list' | 'map'>('list');
  const [racePriorities, setRacePriorities] = useState<Record<string, string>>({});
  const [raceCosts, setRaceCosts] = useState<Record<string, number>>({});
  const [pendingConfirmId, setPendingConfirmId] = useState<string | null>(null);

  // Helper per calcolo distanza (memoizzato internamente)
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

  // Pre-processamento ultra-ottimizzato delle gare
  const races = useMemo(() => {
    const source = racesState.length > 0 ? racesState : (racesData as Race[]);
    return source.map(race => {
      // 1. Coordinate e Jitter
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

      // 2. Distanza da casa
      const dist = getDistance(race.location, homeCity);

      return { ...race, mapCoords, distanceFromHome: dist };
    });
  }, [racesState, homeCity, getDistance]);

  const iconCache = useMemo(() => {
    const cache: Record<string, L.DivIcon> = {};
    const types = ['Triathlon', 'Duathlon', 'Winter', 'Cross'];
    const priorities = [undefined, 'A'];
    const selectedStates = [true, false];
    types.forEach(t => {
      priorities.forEach(p => {
        selectedStates.forEach(s => {
          let color = '#3b82f6';
          if (t === 'Duathlon') color = '#f97316';
          if (t.includes('Winter')) color = '#06b6d4';
          if (t === 'Cross') color = '#10b981';
          if (s) color = '#ef4444';
          if (p === 'A') color = '#eab308';
          const key = `${t}-${p}-${s}`;
          cache[key] = L.divIcon({
            className: 'custom-div-icon',
            html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: white; font-size: 8px; font-weight: 900;">${p === 'A' ? 'A' : ''}</div>`,
            iconSize: [14, 14],
            iconAnchor: [7, 7]
          });
        });
      });
    });
    return cache;
  }, []);

  const getCachedIcon = (type: string, isSelected: boolean, priority?: string) => {
    const key = `${type.includes('Winter') ? 'Winter' : type}-${priority === 'A' ? 'A' : 'undefined'}-${isSelected}`;
    return iconCache[key] || iconCache['Triathlon-undefined-false'];
  };

  const handleViewChange = (mode: 'list' | 'map') => {
    startTransition(() => setViewMode(mode));
  };

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

  const setPriority = useCallback((id: string, p: string) => {
    setRacePriorities(prev => ({ ...prev, [id]: p }));
  }, []);

  const updateCost = useCallback((id: string, cost: number) => {
    setRaceCosts(prev => ({ ...prev, [id]: cost }));
  }, []);

  const budgetTotals = useMemo(() => {
    const selectedData = races.filter(r => selectedRaces.includes(r.id));
    const registration = selectedData.reduce((acc, r) => acc + (raceCosts[r.id] || 0), 0);
    let travel = 0;
    selectedData.forEach(r => {
        if (r.distanceFromHome) travel += (r.distanceFromHome * 2) * 0.25;
    });
    return { registration, travel, total: registration + travel };
  }, [selectedRaces, raceCosts, races]);

  const addRaceFinal = useCallback((id: string) => {
    setSelectedRaces((prev) => [...prev, id]);
    setRacePriorities(prev => ({ ...prev, [id]: 'C' }));
    setPendingConfirmId(null);
  }, []);

  const toggleRace = useCallback((id: string) => {
    if (selectedRaces.includes(id)) {
      setSelectedRaces((prev) => prev.filter((r) => r !== id));
      setRacePriorities(prev => {
          const next = {...prev};
          delete next[id];
          return next;
      });
      return;
    }
    
    const newRace = races.find(r => r.id === id);
    if (newRace) {
      const [nd, nm, ny] = newRace.date.split("-");
      const newDate = new Date(parseInt(ny), parseInt(nm) - 1, parseInt(nd));
      const tooClose = races
        .filter(r => selectedRaces.includes(r.id))
        .some(r => {
          const [rd, rm, ry] = r.date.split("-");
          const existingDate = new Date(parseInt(ry), parseInt(rm) - 1, parseInt(rd));
          const diffDays = Math.ceil(Math.abs(newDate.getTime() - existingDate.getTime()) / (1000 * 3600 * 24));
          return diffDays < 3;
        });
      
      if (tooClose) {
        setPendingConfirmId(id); // Attiva il modale grafico non bloccante
        return;
      }
    }
    addRaceFinal(id);
  }, [selectedRaces, races, addRaceFinal]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const imported = JSON.parse(event.target?.result as string);
          if (Array.isArray(imported)) {
            setRacesState(imported);
            alert("Gare caricate con successo!");
          }
        } catch (err) { alert("Errore formato JSON."); }
      };
      reader.readAsText(file);
    }
  };

  const exportPlan = () => {
    const plan = races.filter(r => selectedRaces.includes(r.id));
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(plan, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "mio_piano_fitri_2026.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  const exportToICS = () => {
    const selectedData = races.filter(r => selectedRaces.includes(r.id));
    if (selectedData.length === 0) return;
    let icsContent = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Fitri Planner//IT", "CALSCALE:GREGORIAN", "METHOD:PUBLISH"];
    selectedData.forEach(race => {
      const [d, m, y] = race.date.split("-");
      const startDate = `${y}${m}${d}`;
      const endDt = new Date(parseInt(y), parseInt(m) - 1, parseInt(d) + 1);
      const endDate = endDt.toISOString().slice(0, 10).replace(/-/g, "");
      icsContent.push("BEGIN:VEVENT");
      icsContent.push(`UID:${race.id}@fitri2026`);
      icsContent.push(`DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").split(".")[0]}Z`);
      icsContent.push(`DTSTART;VALUE=DATE:${startDate}`);
      icsContent.push(`DTEND;VALUE=DATE:${endDate}`);
      icsContent.push(`SUMMARY:${race.title.replace(/,/g, "\\,")}`);
      icsContent.push(`LOCATION:${(race.location + " " + race.region).replace(/,/g, "\\,")}`);
      const priorityLabel = racePriorities[race.id] === 'A' ? 'OBIETTIVO' : racePriorities[race.id] === 'B' ? 'Preparazione' : 'Allenamento';
      icsContent.push(`DESCRIPTION:Priorità: ${priorityLabel}\\nTipo: ${race.type}\\nSettore: ${race.category || 'N/A'}\\nRank: ${race.rank || 'N/A'}`);
      icsContent.push("END:VEVENT");
    });
    icsContent.push("END:VCALENDAR");
    const blob = new Blob([icsContent.join("\r\n")], { type: "text/calendar;charset=utf-8" });
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.setAttribute("download", "calendario_gare_2026.ics");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportToCSV = () => {
    const selectedData = races.filter(r => selectedRaces.includes(r.id));
    if (selectedData.length === 0) return;

    // Intestazioni Excel
    const headers = ["Data", "Evento", "Specialità", "Località", "Regione", "Sport", "Distanza", "Priorità", "Costo Iscrizione (€)", "Km da Casa"];
    
    const rows = selectedData.map(race => {
        const dist = getDistance(race.location, homeCity);
        return [
            race.date,
            `"${(race.event || '').replace(/"/g, '""')}"`,
            `"${race.title.replace(/"/g, '""')}"`,
            `"${race.location.replace(/"/g, '""')}"`,
            race.region,
            race.type,
            race.distance,
            racePriorities[race.id] || 'C',
            raceCosts[race.id] || 0,
            dist ? `~${dist}` : 'N/A'
        ];
    });

    const csvContent = [headers, ...rows].map(e => e.join(",")).join("\n");
    const blob = new Blob(["\ufeff" + csvContent], { type: 'text/csv;charset=utf-8;' }); // \ufeff per supporto accenti in Excel
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "piano_gare_mtt_2026.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filteredRaces = useMemo(() => {
    return races.filter((race) => {
        const matchesSearch = (race.title?.toLowerCase() || "").includes(searchTerm.toLowerCase()) || (race.location?.toLowerCase() || "").includes(searchTerm.toLowerCase());
        const matchesType = filterType === "Tutti" || race.type === filterType || (race.type === "Winter" && filterType === "Winter");
        const matchesRegion = filterRegion === "Tutte" || race.region === filterRegion;
        const matchesDistance = filterDistance === "Tutte" || race.distance === filterDistance;
        return matchesSearch && matchesType && matchesRegion && matchesDistance;
    }).sort((a,b) => {
        const dateA = a.date.split("-").reverse().join("-");
        const dateB = b.date.split("-").reverse().join("-");
        return dateA.localeCompare(dateB);
    });
  }, [races, searchTerm, filterType, filterRegion, filterDistance]);

  const myPlan = useMemo(() => {
    return races.filter((r) => selectedRaces.includes(r.id))
        .sort((a,b) => {
            const dateA = a.date.split("-").reverse().join("-");
            const dateB = b.date.split("-").reverse().join("-");
            return dateA.localeCompare(dateB);
        });
  }, [races, selectedRaces]);

  const getRankColor = useCallback((rank: string) => {
    switch(rank) {
        case 'Gold': return 'text-yellow-500 bg-yellow-50 border-yellow-100';
        case 'Silver': return 'text-slate-400 bg-slate-50 border-slate-100';
        case 'Bronze': return 'text-orange-400 bg-orange-50 border-orange-100';
        default: return 'text-blue-400 bg-blue-50 border-blue-100';
    }
  }, []);

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans selection:bg-blue-100">
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-br from-red-500 to-red-600 p-2.5 rounded-2xl text-white shadow-lg shadow-red-100 rotate-3">
              <Trophy className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-black text-slate-800 tracking-tight leading-none uppercase">Fitri 2026</h1>
              <span className="text-[10px] font-bold text-red-500 uppercase tracking-[0.2em]">MTT Milano Triathlon Team</span>
            </div>
          </div>
          <div className="flex gap-2">
            <button 
                onClick={exportPlan}
                disabled={selectedRaces.length === 0}
                className="hidden sm:flex items-center gap-2 px-5 py-2.5 bg-white border border-slate-200 text-slate-600 rounded-2xl hover:bg-slate-50 transition-all text-sm font-bold disabled:opacity-50"
            >
              <Download className="w-4 h-4" /> Esporta
            </button>
            <button 
                onClick={exportToICS}
                disabled={selectedRaces.length === 0}
                className="flex items-center gap-2 px-4 py-2 sm:px-5 sm:py-2.5 bg-blue-50 border border-blue-200 text-blue-600 rounded-2xl hover:bg-blue-100 transition-all text-sm font-bold disabled:opacity-50 disabled:bg-white disabled:border-slate-200 disabled:text-slate-400"
            >
              <Calendar className="w-4 h-4" /> <span className="hidden xs:inline">Calendario (.ics)</span>
            </button>
            <button 
                onClick={exportToCSV}
                disabled={selectedRaces.length === 0}
                className="flex items-center gap-2 px-4 py-2 sm:px-5 sm:py-2.5 bg-emerald-50 border border-emerald-200 text-emerald-600 rounded-2xl hover:bg-emerald-100 transition-all text-sm font-bold disabled:opacity-50 disabled:bg-white disabled:border-slate-200 disabled:text-slate-400"
            >
              <Download className="w-4 h-4" /> <span className="hidden xs:inline">Excel (.csv)</span>
            </button>
            <label className="flex items-center gap-2 px-5 py-2.5 bg-slate-900 text-white rounded-2xl hover:bg-slate-800 transition-all text-sm font-bold cursor-pointer shadow-xl shadow-slate-200">
              <Upload className="w-4 h-4" /> Importa
              <input type="file" className="hidden" accept=".json" onChange={handleFileUpload} />
            </label>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 sticky top-28">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                    <Filter className="w-4 h-4 text-blue-500" /> Filtri Avanzati
                </h2>
                { (searchTerm || filterType !== 'Tutti' || filterRegion !== 'Tutte') && (
                    <button 
                        onClick={() => { setSearchTerm(""); setFilterType("Tutti"); setFilterRegion("Tutte"); setFilterDistance("Tutte"); }}
                        className="text-[10px] font-bold text-blue-600 hover:underline"
                    >
                        Reset
                    </button>
                )}
            </div>
            
            <div className="space-y-5">
              <div className="relative group">
                <Search className="absolute left-4 top-3.5 w-5 h-5 text-slate-300 group-focus-within:text-blue-500 transition-colors" />
                <input
                  type="text"
                  placeholder="Cerca gara, città..."
                  className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border-2 border-transparent rounded-2xl focus:border-blue-500 focus:bg-white transition-all outline-none text-sm font-medium"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>

              <div>
                <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1 mb-2 block">Sport</label>
                <div className="flex flex-wrap gap-2">
                    {["Tutti", "Triathlon", "Duathlon", "Winter", "Cross"].map((type) => (
                    <button
                        key={type}
                        onClick={() => setFilterType(type)}
                        className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase transition-all ${
                        (filterType === type)
                            ? "bg-slate-900 text-white shadow-lg shadow-slate-200" 
                            : "bg-slate-100 text-slate-500 hover:bg-slate-200"
                        }`}
                    >
                        {type}
                    </button>
                    ))}
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                  <div>
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1 mb-2 block">La tua città (Provincia)</label>
                    <div className="relative">
                        <Navigation className="absolute left-3 top-2.5 w-4 h-4 text-slate-300" />
                        <select 
                            value={homeCity}
                            onChange={(e) => {
                                setHomeCity(e.target.value);
                                localStorage.setItem("home_city", e.target.value);
                            }}
                            className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border-none rounded-xl text-xs font-bold outline-none cursor-pointer hover:bg-slate-100 transition-colors"
                        >
                            <option value="">Seleziona Provincia...</option>
                            {Object.keys(provinceCoordinates).sort().map(p => <option key={p} value={p}>{p}</option>)}
                        </select>
                    </div>
                  </div>
                  <div>
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1 mb-2 block">Regione</label>
                    <select 
                        value={filterRegion}
                        onChange={(e) => setFilterRegion(e.target.value)}
                        className="w-full p-3 bg-slate-50 border-none rounded-2xl text-xs font-bold outline-none cursor-pointer hover:bg-slate-100 transition-colors"
                    >
                        {regions.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1 mb-2 block">Distanza</label>
                    <select 
                        value={filterDistance}
                        onChange={(e) => setFilterDistance(e.target.value)}
                        className="w-full p-3 bg-slate-50 border-none rounded-2xl text-xs font-bold outline-none cursor-pointer hover:bg-slate-100 transition-colors"
                    >
                        {distances.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                  </div>
              </div>
            </div>

            <div className="mt-10 pt-10 border-t border-slate-100">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-black text-slate-800 flex items-center gap-2">
                        Il Tuo Anno <span className="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-lg text-xs">{myPlan.length}</span>
                    </h2>
                    <Download className="w-4 h-4 text-slate-400 cursor-pointer" onClick={exportPlan} />
                </div>
                
                {myPlan.length === 0 ? (
                <div className="bg-slate-50 rounded-2xl p-8 text-center border border-dashed border-slate-200">
                    <p className="text-xs font-bold text-slate-400 leading-relaxed">
                        Seleziona le gare dalla lista per comporre il tuo calendario personalizzato.
                    </p>
                </div>
                ) : (
                <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                    {myPlan.map((race, index) => (
                    <div key={race.id} className={`group bg-white p-4 rounded-2xl border transition-all hover:shadow-sm ${racePriorities[race.id] === 'A' ? 'border-yellow-200 bg-yellow-50/30' : 'border-slate-100 hover:border-blue-200'}`}>
                        <div className="flex justify-between items-start">
                        <div className="space-y-1">
                            <div className="flex items-center gap-2">
                                <span className="text-[10px] font-black text-blue-500 uppercase">{race.date}</span>
                                {racePriorities[race.id] && (
                                    <span className={`text-[8px] font-black px-1.5 py-0.5 rounded ${
                                        racePriorities[race.id] === 'A' ? 'bg-yellow-400 text-white' :
                                        racePriorities[race.id] === 'B' ? 'bg-blue-400 text-white' :
                                        'bg-slate-400 text-white'
                                    }`}>
                                        {racePriorities[race.id]}
                                    </span>
                                )}
                            </div>
                            {race.event && (
                                <div className="text-[8px] font-black text-slate-400 uppercase tracking-widest leading-none">
                                    {race.event}
                                </div>
                            )}
                            <h4 className="text-xs font-bold text-slate-700 leading-tight group-hover:text-blue-600 transition-colors">{race.title}</h4>
                            {race.distanceFromHome !== undefined && race.distanceFromHome !== null && (
                                <div className="flex items-center gap-1.5 mt-1">
                                    <Navigation className="w-2.5 h-2.5 text-blue-400" />
                                    <span className="text-[9px] font-black text-blue-600 uppercase">~{race.distanceFromHome} KM</span>
                                </div>
                            )}
                        </div>
                        <button onClick={() => toggleRace(race.id)} className="text-slate-200 hover:text-red-500 transition-colors">
                            <Trash2 className="w-4 h-4" />
                        </button>
                        </div>
                        {index > 0 && (
                        <div className="mt-3 pt-3 border-t border-slate-50 text-[10px] text-slate-400 font-bold flex items-center gap-2">
                            <Activity className="w-3 h-3 text-slate-300" />
                            {(() => {
                                const d1 = race.date.split('-');
                                const d2 = myPlan[index-1].date.split('-');
                                const date1 = new Date(parseInt(d1[2]), parseInt(d1[1])-1, parseInt(d1[0]));
                                const date2 = new Date(parseInt(d2[2]), parseInt(d2[1])-1, parseInt(d2[0]));
                                const diff = Math.ceil(Math.abs(date1.getTime() - date2.getTime()) / (1000 * 3600 * 24));
                                return `${diff} GIORNI DI RECUPERO`;
                            })()}
                        </div>
                        )}
                    </div>
                    ))}
                </div>
                )}
            </div>

                {selectedRaces.length > 0 && (
                    <div className="mt-6 pt-6 border-t border-slate-100 space-y-3">
                        <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                            <Trophy className="w-3 h-3 text-emerald-500" /> Budget Stimato
                        </h3>
                        <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-100/50 space-y-2">
                            <div className="flex justify-between text-xs font-bold text-slate-600">
                                <span>Iscrizioni</span>
                                <span>€ {budgetTotals.registration.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-xs font-bold text-slate-600">
                                <span>Viaggio (stima)</span>
                                <span>€ {budgetTotals.travel.toFixed(2)}</span>
                            </div>
                            <div className="pt-2 border-t border-emerald-100 flex justify-between text-sm font-black text-emerald-700">
                                <span>TOTALE</span>
                                <span>€ {budgetTotals.total.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                )}
          </div>
        </div>

        <div className="lg:col-span-8 space-y-4">
            <div className="flex items-center justify-between mb-4 px-2">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                    Risultati: <b>{filteredRaces.length}</b> gare trovate
                </span>
                
                <div className="flex bg-slate-100 p-1 rounded-xl">
                    <button 
                        onClick={() => handleViewChange('list')}
                        className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-[10px] font-black uppercase transition-all ${viewMode === 'list' ? 'bg-white shadow-sm text-blue-600' : 'text-slate-400'}`}
                    >
                        <List className="w-3 h-3" /> Lista
                    </button>
                    <button 
                        onClick={() => handleViewChange('map')}
                        disabled={isPending}
                        className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-[10px] font-black uppercase transition-all ${viewMode === 'map' ? 'bg-white shadow-sm text-blue-600' : 'text-slate-400'} ${isPending ? 'animate-pulse' : ''}`}
                    >
                        <MapIcon className="w-3 h-3" /> {isPending ? 'Caricamento...' : 'Mappa'}
                    </button>
                </div>
            </div>

            {viewMode === 'list' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {filteredRaces.map((race) => (
                        <RaceCard 
                            key={race.id}
                            race={race}
                            isSelected={selectedRaces.includes(race.id)}
                            priority={racePriorities[race.id]}
                            cost={raceCosts[race.id]}
                            onToggle={toggleRace}
                            onPriority={setPriority}
                            onCost={updateCost}
                            getRankColor={getRankColor}
                        />
                    ))}
                </div>
            ) : (
                <div className="relative h-[600px] w-full">
                    <MapContainer center={[41.8719, 12.5674]} zoom={6} scrollWheelZoom={false}>
                        <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        />
                        {filteredRaces.map(race => {
                            if (!race.mapCoords) return null;
                            return (
                                <Marker 
                                    key={race.id} 
                                    position={race.mapCoords}
                                    icon={getCachedIcon(race.type, selectedRaces.includes(race.id), racePriorities[race.id])}
                                >
                                    <Popup>
                                        <div className="p-1 min-w-[150px]">
                                            <span className="text-[8px] font-black text-blue-500 uppercase">{race.date}</span>
                                            <h4 className="text-xs font-bold text-slate-800 mb-1 leading-tight">{race.title}</h4>
                                            <p className="text-[10px] text-slate-500 mb-3">{race.location}</p>
                                            <button 
                                                onClick={() => toggleRace(race.id)}
                                                className={`w-full py-1.5 rounded-lg text-[9px] font-black uppercase transition-colors ${
                                                    selectedRaces.includes(race.id) 
                                                    ? 'bg-red-50 text-red-600' 
                                                    : 'bg-blue-600 text-white'
                                                }`}
                                            >
                                                {selectedRaces.includes(race.id) ? 'Rimuovi' : 'Aggiungi'}
                                            </button>
                                        </div>
                                    </Popup>
                                </Marker>
                            );
                        })}
                    </MapContainer>
                </div>
            )}
            
            {filteredRaces.length === 0 && (
                <div className="bg-white rounded-[3rem] p-24 text-center border-2 border-dashed border-slate-100">
                    <div className="bg-slate-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                        <Info className="w-10 h-10 text-slate-200" />
                    </div>
                    <h4 className="text-slate-800 font-black uppercase tracking-widest mb-2">Nessuna Gara</h4>
                    <p className="text-slate-400 text-sm font-medium">Prova a cambiare i filtri o il termine di ricerca.</p>
                </div>
            )}
        </div>
      </main>

      {/* Modal di Conferma Non-Bloccante (Fix INP) */}
      {pendingConfirmId && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
              <div className="bg-white rounded-[2.5rem] p-8 max-w-md w-full shadow-2xl border border-slate-100 scale-in-center animate-in zoom-in-95 duration-200">
                  <div className="bg-orange-50 w-16 h-16 rounded-3xl flex items-center justify-center mb-6">
                      <AlertTriangle className="w-8 h-8 text-orange-500" />
                  </div>
                  <h3 className="text-xl font-black text-slate-800 mb-3 uppercase tracking-tight">Recupero Insufficiente</h3>
                  <p className="text-slate-500 text-sm font-medium leading-relaxed mb-8">
                      Questa gara dista <b>meno di 3 giorni</b> da un'altra già presente nel tuo piano. 
                      Sei sicuro di volerla aggiungere comunque alla tua stagione?
                  </p>
                  <div className="flex gap-3">
                      <button 
                        onClick={() => setPendingConfirmId(null)}
                        className="flex-1 py-4 rounded-2xl text-xs font-black uppercase tracking-widest text-slate-400 bg-slate-50 hover:bg-slate-100 transition-colors"
                      >
                          Annulla
                      </button>
                      <button 
                        onClick={() => addRaceFinal(pendingConfirmId)}
                        className="flex-1 py-4 rounded-2xl text-xs font-black uppercase tracking-widest text-white bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200 transition-all"
                      >
                          Conferma
                      </button>
                  </div>
              </div>
          </div>
      )}
      
      <footer className="max-w-7xl mx-auto px-4 py-12 text-center">
          <p className="text-[10px] font-bold text-slate-300 uppercase tracking-[0.4em]">
              FITRI 2026 Season Planner • MTT Milano Triathlon Team
          </p>
      </footer>
    </div>
  );
};

export default App;
