import React from 'react';
import { useTranslation } from 'react-i18next';

/**
 * Language switcher component.
 *
 * Displays buttons to switch between English and Japanese. The active
 * language is highlighted. When a language button is clicked, the
 * i18n library updates the current locale and the interface refreshes
 * automatically.
 */
export default function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="flex space-x-2 items-center">
      <button
        onClick={() => changeLanguage('en')}
        className={`px-2 py-1 rounded text-sm border ${
          i18n.language === 'en' ? 'border-primary text-primary' : 'border-gray-300 text-gray-700'
        }`}
      >
        EN
      </button>
      <button
        onClick={() => changeLanguage('ja')}
        className={`px-2 py-1 rounded text-sm border ${
          i18n.language === 'ja' ? 'border-primary text-primary' : 'border-gray-300 text-gray-700'
        }`}
      >
        日本語
      </button>
    </div>
  );
}
