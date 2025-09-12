import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import EventsPage from './components/EventsPage';
import CleaningPage from './components/CleaningPage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';

/**
 * Main application component.
 *
 * Sets up the navigation bar and defines client side routes. Each route
 * corresponds to one of the pages in the site. Unknown routes
 * fallback to the home page.
 */
export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/cleaning" element={<CleaningPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        {/* Catch‑all route */}
        <Route path="*" element={<HomePage />} />
      </Routes>
    </>
  );
}
