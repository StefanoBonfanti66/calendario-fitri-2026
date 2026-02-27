// Contenuto corretto in base alla nuova struttura
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from '../components/Layout';
import DashboardPage from './DashboardPage';
import TeamCalendarPage from './TeamCalendarPage';
import Auth from './Auth';

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<Auth />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<DashboardPage />} />
        <Route path="calendario-team" element={<TeamCalendarPage />} />
      </Route>
    </Routes>
  );
};

export default App;
