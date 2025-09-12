import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';
import LanguageSwitcher from './LanguageSwitcher';
import ThemeToggle from './ThemeToggle';
import { logos } from '../assets/logos';

/**
 * Navigation bar component.
 *
 * Displays navigation links to the main pages (home, events, cleaning
 * service) and handles authentication actions. If a user is logged in
 * (i.e. there is a token), a logout button is shown instead of the
 * login/register links.
 */
export default function Navbar() {
  const { t } = useTranslation();
  const { token, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const closeMenu = () => setOpen(false);

  const NavLinks = ({ onClick }) => (
    <>
      <Link to="/" className="text-ink dark:text-white hover:text-primary" onClick={onClick}>
        {t('home')}
      </Link>
      <Link to="/events" className="text-ink dark:text-white hover:text-primary" onClick={onClick}>
        {t('events')}
      </Link>
      <Link to="/cleaning" className="text-ink dark:text-white hover:text-primary" onClick={onClick}>
        <span className="lg:hidden">{t('cleaning_short', 'Cleaning')}</span>
        <span className="hidden lg:inline">{t('cleaning', 'Cleaning Service')}</span>
      </Link>
      {token ? (
        <button
          onClick={() => {
            logout();
            navigate('/');
            if (onClick) onClick();
          }}
          className="text-ink dark:text-white hover:text-primary focus:outline-none text-left"
        >
          {t('logout')}
        </button>
      ) : (
        <>
          <Link to="/login" className="text-ink dark:text-white hover:text-primary" onClick={onClick}>
            {t('login')}
          </Link>
          <Link to="/register" className="text-ink dark:text-white hover:text-primary" onClick={onClick}>
            {t('register')}
          </Link>
        </>
      )}
    </>
  );

  return (
    <header className="bg-paper dark:bg-[#0b0b0e] shadow-md border-b border-ink/10 dark:border-white/10">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group flex-shrink-0" aria-label="House of Bijou home">
          <span className="sr-only">House of Bijou</span>
          {/* Gradient frame nodding to Afrikasia crossover (magenta → gold → teal) */}
          <div className="p-[2px] rounded-md bg-gradient-to-br from-primary via-accent to-secondary">
            <img
              src={logos.cropped || logos.primary}
              alt="House of Bijou logo"
              className="h-12 w-auto object-contain rounded-[6px] block"
            />
          </div>
          {/* Wordmark visible on lg+ screens for balance */}
          <span className="hidden lg:inline font-display text-xl text-ink dark:text-white tracking-wide">
            House of Bijou
          </span>
        </Link>
        {/* Desktop nav */}
        <nav className="hidden md:flex flex-1 items-center justify-end gap-3 md:gap-4 lg:gap-6 whitespace-nowrap">
          <NavLinks />
          <LanguageSwitcher />
          <ThemeToggle />
        </nav>

        {/* Mobile toggle */}
        <button
          className="md:hidden inline-flex items-center justify-center p-2 rounded-md border border-ink/10 dark:border-white/10 text-ink dark:text-white hover:bg-ink/5 dark:hover:bg-white/10"
          aria-controls="mobile-menu"
          aria-expanded={open ? 'true' : 'false'}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 24 24" fill="none" strokeWidth="2">
              <defs>
                <linearGradient id="bijouGradNavClose" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#e11d48" />
                  <stop offset="50%" stopColor="#eab308" />
                  <stop offset="100%" stopColor="#0f766e" />
                </linearGradient>
              </defs>
              <path stroke="url(#bijouGradNavClose)" strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 24 24" fill="none" strokeWidth="2">
              <defs>
                <linearGradient id="bijouGradNavOpen" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#e11d48" />
                  <stop offset="50%" stopColor="#eab308" />
                  <stop offset="100%" stopColor="#0f766e" />
                </linearGradient>
              </defs>
              <path stroke="url(#bijouGradNavOpen)" strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
          <span className="sr-only">Toggle navigation</span>
        </button>
      </div>

      {/* Mobile menu panel */}
      {open && (
        <div id="mobile-menu" className="md:hidden border-t border-ink/10 dark:border-white/10 bg-paper dark:bg-[#0b0b0e]">
          <div className="container mx-auto px-4 py-3 flex flex-col gap-3">
            <NavLinks onClick={closeMenu} />
            <div className="pt-2">
              <div className="flex items-center gap-3">
                <LanguageSwitcher />
                <ThemeToggle />
              </div>
            </div>
          </div>
        </div>
      )}
      {/* Thin gradient accent under header */}
      <div className="h-0.5 w-full bg-gradient-to-r from-primary via-accent to-secondary" />
    </header>
  );
}
