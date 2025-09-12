import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

/**
 * Component displaying a list of events/volunteer opportunities.
 *
 * Users can sign up for an event by clicking the sign‑up button. If
 * they are not logged in they will be redirected to the login page.
 */
export default function EventsPage() {
  const { t, i18n } = useTranslation();
  const { api, token } = useAuth();
  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [hero, setHero] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [heroError, setHeroError] = useState(null);
  const [selected, setSelected] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 9;

  useEffect(() => {
    async function fetchData() {
      try {
        const heroReq = api.get('events-page/', { params: { lang: i18n.language } })
          .then((r) => setHero(r.data))
          .catch((e) => { console.error(e); setHeroError('Failed to load header'); });
        const eventsReq = api.get('events/', { params: { lang: i18n.language, page, page_size: pageSize } })
          .then((r) => {
            const data = r.data || {};
            setEvents(data.results || data || []);
            if (typeof data.total_pages === 'number') setTotalPages(data.total_pages || 1);
          })
          .catch((e) => { console.error(e); setError('Failed to fetch events'); });
        await Promise.allSettled([heroReq, eventsReq]);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [api, i18n.language, page]);

  const handleSignup = async (eventId) => {
    if (!token) {
      navigate('/login');
      return;
    }
    try {
      await api.post(`events/${eventId}/register/`);
      // Refresh events to update availability
      const response = await api.get('events/', { params: { lang: i18n.language } });
      setEvents(response.data);
      alert('Successfully registered!');
    } catch (err) {
      if (err.response && err.response.data) {
        alert(err.response.data.detail);
      } else {
        alert('An error occurred.');
      }
    }
  };

  if (loading) return <div className="p-4">{t('loading')}</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  const heroTitle = hero?.title || 'Upcoming Events';
  const heroSubtitle = hero?.subtitle || 'Join community gatherings, volunteer days, and workshops. New dates drop regularly — check back soon!';
  const placeholders = hero?.placeholders || [];

  return (
    <main>
      {/* Hero */}
      <section className="relative h-56 md:h-72 w-full overflow-hidden">
        {hero?.hero_image ? (
          <img
            src={hero.hero_image}
            alt=""
            fetchpriority="high"
            decoding="async"
            className="absolute inset-0 w-full h-full object-cover"
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-primary/90 via-accent/80 to-secondary/90" />
        )}
        <div className="absolute inset-0 bg-black/20" />
        <div className="relative h-full container mx-auto px-4 md:px-8 flex items-end pb-6">
          <div>
            <h1 className="font-display text-white text-3xl md:text-5xl tracking-tight drop-shadow">{heroTitle}</h1>
            <p className="mt-1.5 max-w-2xl text-white/90">{heroSubtitle}</p>
          </div>
        </div>
      </section>

      <section className="container mx-auto p-4 md:p-8">
        {error && <p className="text-red-600 mb-3">{error}</p>}
        {events.length === 0 ? (
          <div>
            <p className="text-ink/80 mb-4">{t('no_events', 'No upcoming events yet. Check back soon or follow our socials!')}</p>
            {placeholders.length > 0 ? (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {placeholders.map((ph, idx) => (
                  <div key={idx} className="rounded-lg border border-ink/10 dark:border-white/10 shadow-sm overflow-hidden bg-white dark:bg-[#111216]">
                    {ph.image ? (
                      <div className="h-40 bg-center bg-cover" style={{ backgroundImage: `url(${ph.image})` }} />
                    ) : (
                      <div className="h-40 bg-gradient-to-br from-primary/20 via-accent/20 to-secondary/20" />
                    )}
                    <div className="p-4">
                      <h3 className="text-lg font-semibold mb-1 text-ink dark:text-white">{ph.title}</h3>
                      {ph.description && (
                        <p className="text-sm text-ink/80 dark:text-white/70 mb-3">{ph.description}</p>
                      )}
                      {ph.cta_url && (
                        <a href={ph.cta_url} className="inline-block text-primary hover:underline">
                          {ph.cta_label || t('learn_more', 'Learn more')}
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="rounded-lg border border-ink/10 dark:border-white/10 shadow-sm overflow-hidden bg-white dark:bg-[#111216]">
                    <div className="h-28 bg-gradient-to-br from-primary/20 via-accent/20 to-secondary/20" />
                    <div className="p-4">
                      <div className="h-5 w-40 bg-ink/10 dark:bg-white/10 rounded mb-2" />
                      <div className="h-4 w-24 bg-ink/10 dark:bg-white/10 rounded mb-3" />
                      <div className="h-4 w-full bg-ink/10 dark:bg-white/10 rounded mb-2" />
                      <div className="h-4 w-3/4 bg-ink/10 dark:bg-white/10 rounded mb-4" />
                      <button className="bg-ink/10 dark:bg-white/10 text-ink/50 dark:text-white/50 cursor-not-allowed px-4 py-2 rounded">{t('signup')}</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {events.map((ev) => (
              <div
                key={ev.id}
                className="card p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <h2 className="text-xl font-bold mb-2">
                  {ev.title || ev.title_en || ev.title_ja}
                </h2>
                <p className="text-sm muted mb-1">
                  {new Date(ev.start_datetime).toLocaleString(i18n.language === 'ja' ? 'ja-JP' : 'en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </p>
                {ev.location && (
                  <p className="text-sm muted mb-1">{ev.location}</p>
                )}
                <p className="text-sm mb-3">
                  {ev.description || ev.description_en || ev.description_ja}
                </p>
                {ev.capacity && (
                  <p className="text-sm muted mb-2">
                    {ev.available_slots} / {ev.capacity} slots remaining
                  </p>
                )}
                <div className="flex gap-2">
                  <button onClick={() => setSelected(ev)} className="btn-ghost">
                    {t('more_details', 'More details')}
                  </button>
                  <button
                    onClick={() => handleSignup(ev.id)}
                    className="btn-primary"
                    disabled={ev.capacity && ev.available_slots === 0}
                  >
                    {ev.capacity && ev.available_slots === 0 ? 'Full' : t('signup')}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        <div className="mt-6 flex items-center justify-center gap-3">
          <button
            className="btn-ghost"
            disabled={page <= 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
          >
            Prev
          </button>
          <span className="muted">Page {page} of {totalPages}</span>
          <button
            className="btn-ghost"
            disabled={page >= totalPages}
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          >
            Next
          </button>
        </div>
      </section>

      {/* Slide-over details drawer */}
      {selected && (
        <div className="fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/40" onClick={() => setSelected(null)} />
          <aside className="absolute right-0 top-0 h-full w-full max-w-md bg-white dark:bg-[#0b0b0e] shadow-xl transform transition-transform translate-x-0">
            <div className="flex items-center justify-between p-4 border-b border-ink/10 dark:border-white/10">
              <h3 className="font-display text-xl text-ink dark:text-white">{selected.title || selected.title_en || selected.title_ja}</h3>
              <button onClick={() => setSelected(null)} aria-label="Close" className="p-2 rounded hover:bg-ink/5 dark:hover:bg-white/10">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="p-4 space-y-3 overflow-y-auto h-[calc(100%-56px)]">
              <p className="text-sm text-ink/70 dark:text-white/70">
                {new Date(selected.start_datetime).toLocaleString(i18n.language === 'ja' ? 'ja-JP' : 'en-US', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                {selected.location ? ` • ${selected.location}` : ''}
              </p>
              <p className="text-ink dark:text-white">{selected.description || selected.description_en || selected.description_ja}</p>
              <div className="grid grid-cols-2 gap-2">
                {(selected.images || []).map((im, idx) => (
                  <figure key={idx} className="bg-ink/5 dark:bg-white/10 rounded overflow-hidden">
                    <img src={im.url} alt={im.caption_en || ''} loading="lazy" decoding="async" className="w-full h-32 object-cover" />
                    {(im.caption_en || im.caption_ja) && (
                      <figcaption className="p-1 text-xs text-ink/70 dark:text-white/70">{i18n.language === 'ja' ? (im.caption_ja || im.caption_en) : (im.caption_en)}</figcaption>
                    )}
                  </figure>
                ))}
              </div>
              <div className="pt-2">
                <button onClick={() => handleSignup(selected.id)} className="bg-primary text-white px-4 py-2 rounded">
                  {t('signup')}
                </button>
              </div>
            </div>
          </aside>
        </div>
      )}
    </main>
  );
}
