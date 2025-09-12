import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';

/**
 * Registration page.
 *
 * Allows new users to create an account by providing a username,
 * email and password. On success the user is logged in automatically
 * and redirected to the home page.
 */
export default function RegisterPage() {
  const { t } = useTranslation();
  const { register } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    try {
      await register(username, email, password);
      navigate('/');
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || 'Registration failed');
      } else {
        setError('Registration failed');
      }
    }
  };

  return (
    <main className="container mx-auto p-4 md:p-8 max-w-lg">
      <h1 className="text-3xl font-bold mb-4 text-primary">{t('register')}</h1>
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
          <label htmlFor="email" className="block text-sm font-medium mb-1">
            {t('email')}
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
        <div>
          <label htmlFor="confirm" className="block text-sm font-medium mb-1">
            {t('confirm_password')}
          </label>
          <input
            id="confirm"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full rounded px-3 py-2 border"
            required
          />
        </div>
        <button type="submit" className="btn-primary">
          {t('register')}
        </button>
      </form>
      <p className="mt-4 text-sm">
        {t('already_have_account')}{' '}
        <Link to="/login" className="text-primary underline">
          {t('login')}
        </Link>
      </p>
    </main>
  );
}
