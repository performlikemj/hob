import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';
import ContactForm from './ContactForm';

/**
 * Cleaning service page.
 *
 * Displays descriptive information about the cleaning business and a
 * contact form allowing visitors to send inquiries. The content is
 * pulled from the backend with support for both languages.
 */
export default function CleaningPage() {
  const { t, i18n } = useTranslation();
  const { api } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lightbox, setLightbox] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await api.get('cleaning-service/', {
          params: { lang: i18n.language },
        });
        setData(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [api, i18n.language]);

  const title = data?.title || data?.title_en || data?.title_ja || t('cleaning', 'Cleaning Service');
  const description =
    data?.description ||
    data?.description_en ||
    data?.description_ja ||
    t(
      'cleaning_blurb',
      'Professional, reliable short-stay cleaning by members of the house. Flexible scheduling and hotel-standard turnover.'
    );
  const features = data?.features || [];
  const ctaText = data?.cta || t('cleaning_cta', 'Tell us your schedule and property details — we’ll get back with a quote.');
  const gallery = data?.gallery || [];
  
  if (loading) return <div className="p-4">{t('loading')}</div>;

  return (
    <main>
      {/* Hero */}
      <section className="relative h-56 md:h-72 w-full overflow-hidden">
        {data?.image ? (
          <img
            src={data.image}
            alt=""
            fetchpriority="high"
            decoding="async"
            className="absolute inset-0 w-full h-full object-cover"
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-primary/90 via-accent/80 to-secondary/90" />
        )}
        <div className="absolute inset-0 bg-black/30" />
        <div className="relative h-full container mx-auto px-4 md:px-8 flex items-end pb-6">
          <div>
            <h1 className="font-display text-white text-3xl md:text-5xl tracking-tight drop-shadow">{title}</h1>
            <p className="mt-1.5 max-w-3xl text-white/90">{description}</p>
          </div>
        </div>
      </section>

      <section className="container mx-auto p-4 md:p-8">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <div className="card p-5 shadow-sm">
              <h2 className="font-display text-xl mb-2">{t('services', 'Services')}</h2>
              {features.length > 0 ? (
                <ul className="grid sm:grid-cols-2 gap-3 muted">
                  {features.map((f, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className={`mt-1 h-2 w-2 rounded-full ${
                        f.color === 'accent' ? 'bg-accent' : f.color === 'secondary' ? 'bg-secondary' : 'bg-primary'
                      }`} />
                      {f.text}
                    </li>
                  ))}
                </ul>
              ) : (
                <ul className="grid sm:grid-cols-2 gap-3 muted">
                  <li className="flex items-start gap-2"><span className="mt-1 h-2 w-2 rounded-full bg-primary" />{t('service_turnover', 'Full turnover: linens, bathroom, kitchen, reset staging')}</li>
                  <li className="flex items-start gap-2"><span className="mt-1 h-2 w-2 rounded-full bg-accent" />{t('service_supplies', 'Restock consumables and basic supplies')}</li>
                  <li className="flex items-start gap-2"><span className="mt-1 h-2 w-2 rounded-full bg-secondary" />{t('service_schedule', 'Flexible scheduling and quick response')}</li>
                  <li className="flex items-start gap-2"><span className="mt-1 h-2 w-2 rounded-full bg-primary" />{t('service_reporting', 'Photo reporting on completion (optional)')}</li>
                </ul>
              )}
            </div>

            {gallery.length > 0 && (
              <div className="mt-6">
                <h2 className="font-display text-xl text-ink mb-2">{t('gallery', 'Our Work')}</h2>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {gallery.slice(0, 3).map((g, idx) => (
                    <button
                      key={idx}
                      onClick={() => setLightbox(g)}
                      className="block rounded overflow-hidden focus:outline-none focus:ring-2 focus:ring-primary"
                      aria-label={g.caption_en || g.caption_ja || 'gallery image'}
                    >
                      <img src={g.url} alt={g.caption_en || ''} loading="lazy" decoding="async" sizes="(min-width: 768px) 33vw, 50vw" className="w-full h-28 md:h-32 object-cover" />
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
          <div className="card p-5 shadow-sm">
            <h2 className="font-display text-xl mb-2">{t('contact_us')}</h2>
            <p className="muted mb-3">{ctaText}</p>
            <ContactForm />
          </div>
        </div>
      </section>

      {lightbox && (
        <div className="fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/50" onClick={() => setLightbox(null)} />
          <div className="absolute inset-0 flex items-center justify-center p-4">
            <figure className="bg-white dark:bg-[#0b0b0e] rounded shadow-xl max-w-3xl w-full">
              <img src={lightbox.url} alt={lightbox.caption_en || ''} className="w-full h-auto max-h-[70vh] object-contain" />
              {(lightbox.caption_en || lightbox.caption_ja) && (
                <figcaption className="p-3 text-sm text-ink/80 dark:text-white/80">
                  {i18n.language === 'ja' ? (lightbox.caption_ja || lightbox.caption_en) : (lightbox.caption_en)}
                </figcaption>
              )}
            </figure>
          </div>
        </div>
      )}
    </main>
  );
}
