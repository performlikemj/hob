import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';

/**
 * Contact form component.
 *
 * Sends inquiries to the backend. Shows a success message upon
 * successful submission. Form fields are controlled and labels are
 * translated.
 */
export default function ContactForm() {
  const { t } = useTranslation();
  const { api } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('contact/', { name, email, message });
      setStatus('success');
      setName('');
      setEmail('');
      setMessage('');
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-xl">
      {status === 'success' && (
        <p className="text-green-600 mb-2">Thank you for your message!</p>
      )}
      {status === 'error' && (
        <p className="text-red-600 mb-2">There was a problem sending your message.</p>
      )}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1" htmlFor="name">
          {t('name')}
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full rounded px-3 py-2 border"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1" htmlFor="email">
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
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1" htmlFor="message">
          {t('message')}
        </label>
        <textarea
          id="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="w-full rounded px-3 py-2 border"
          rows="5"
          required
        />
      </div>
      <button type="submit" className="btn-primary">
        {t('submit')}
      </button>
    </form>
  );
}
