import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';

/**
 * Home page component.
 *
 * Fetches the mission statement from the backend and displays it. It
 * supports bilingual content by requesting the appropriate language
 * based on the current i18n locale. A hero image is shown at the top
 * if provided by the backend.
 */
export default function HomePage() {
  const { t, i18n } = useTranslation();
  const { api } = useAuth();
  const [mission, setMission] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMission() {
      try {
        const response = await api.get('mission/', {
          params: { lang: i18n.language },
        });
        setMission(response.data);
      } catch (error) {
        console.error('Failed to fetch mission', error);
      } finally {
        setLoading(false);
      }
    }
    fetchMission();
  }, [api, i18n.language]);

  const title = mission?.title || mission?.title_en || mission?.title_ja || 'House of Bijou';
  const body = mission?.body || mission?.body_en || mission?.body_ja ||
    'House of Bijou celebrates the shared roots and solidarity between African/Black and Asian communities.';

  return (
    <main>
      {/* Hero: uses backend image if available, otherwise brand gradient */}
      <section className="relative h-72 md:h-[28rem] w-full overflow-hidden">
        {mission?.hero_image ? (
          <img
            src={mission.hero_image}
            alt=""
            fetchpriority="high"
            decoding="async"
            className="absolute inset-0 w-full h-full object-cover"
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-primary/90 via-accent/80 to-secondary/90" />
        )}
        <div className="absolute inset-0 bg-black/20" />
        <div className="relative h-full container mx-auto px-4 md:px-8 flex items-end pb-8">
          <div>
            <h1 className="font-display text-white text-4xl md:text-6xl tracking-tight drop-shadow">
              {title}
            </h1>
            <p className="mt-2 max-w-2xl text-white/90 text-base md:text-lg">
              {body}
            </p>
            {/* Socials */}
            {t('instagram_url', '') && (
              <div className="mt-3">
                <a
                  href={t('instagram_url', '')}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-white/90 hover:text-white focus:outline-none focus:ring-2 focus:ring-white/60 rounded-full px-3 py-1 bg-white/10 hover:bg-white/15 backdrop-blur-sm"
                  aria-label="Instagram"
                >
                  <i className="fa-brands fa-instagram"></i>
                  <span className="text-sm">Instagram</span>
                </a>
              </div>
            )}
          </div>
        </div>
      </section>

      <div className="container mx-auto p-4 md:p-8">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <h2 className="font-display text-2xl md:text-3xl mb-3">{t('events')}</h2>
            <p className="muted mb-4">{t('join_our_events', 'Join our events and volunteer opportunities.')}</p>
            <a href="/events" className="btn-primary">{t('browse_events', 'Browse events')}</a>
          </div>
          <div className="card p-4">
            <h2 className="font-display text-xl mb-2">{t('cleaning', 'Airbnb Cleaning')}</h2>
            <p className="muted mb-3">{t('cleaning_blurb', 'Professional, reliable short-stay cleaning by members of the house.')}</p>
            <a href="/cleaning" className="link text-primary hover:underline">{t('learn_more', 'Learn more')}</a>
          </div>
        </div>
      </div>
    </main>
  );
}
