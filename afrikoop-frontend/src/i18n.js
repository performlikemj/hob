import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './locales/en/translation.json';
import ja from './locales/ja/translation.json';

// Set up the translations for English and Japanese. Additional languages
// can be added by creating new JSON files under ``locales/<lang>/``
// and importing them here.
const resources = {
  en: {
    translation: en,
  },
  ja: {
    translation: ja,
  },
};

// Helper to load server-managed translations and merge into i18next.
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/';

async function loadServerTranslations(lang, namespaces = ['common']) {
  try {
    const url = `${API_BASE}i18n/${lang}/?ns=${encodeURIComponent(namespaces.join(','))}`;
    const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) return;
    const data = await res.json();
    // Merge into the default 'translation' namespace so existing keys work.
    i18n.addResourceBundle(lang, 'translation', data, true, true);
  } catch (_) {
    // ignore network/backend errors and keep fallbacks
  }
}

i18n.use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: { escapeValue: false },
  })
  .then(() => {
    // Initial load for current language
    loadServerTranslations(i18n.language);
  });

// Refresh translations when the language changes
i18n.on('languageChanged', (lng) => {
  loadServerTranslations(lng);
});

export default i18n;
