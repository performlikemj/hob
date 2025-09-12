import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';

/**
 * Login page.
 *
 * Allows users to authenticate and obtain a token. On successful
 * login, the user is redirected to the home page. Displays error
 * messages on failure.
 */
export default function LoginPage() {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await login(username, password);
      navigate('/');
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || 'Login failed');
      } else {
        setError('Login failed');
      }
    }
  };

  return (
    <main className="container mx-auto p-4 md:p-8 max-w-lg">
      <h1 className="text-3xl font-bold mb-4 text-primary">{t('login')}</h1>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="username" className="block text-sm font-medium mb-1">
            {t('username')}
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full rounded px-3 py-2 border"
            required
          />
        </div>
        <div>
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            {t('password')}
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded px-3 py-2 border"
            required
          />
        </div>
        <button type="submit" className="btn-primary">
          {t('login')}
        </button>
      </form>
      <p className="mt-4 text-sm">
        {t('no_account')}{' '}
        <Link to="/register" className="text-primary underline">
          {t('register')}
        </Link>
      </p>
    </main>
  );
}
