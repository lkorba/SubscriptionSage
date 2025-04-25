// i18next initialization and configuration
document.addEventListener('DOMContentLoaded', function() {
  // Initialize i18next
  i18next
    .use(i18nextBrowserLanguageDetector)
    .use(i18nextHttpBackend)
    .init({
      fallbackLng: 'en',
      debug: false,
      detection: {
        order: ['querystring', 'cookie', 'localStorage', 'navigator'],
        lookupQuerystring: 'lang',
        lookupCookie: 'i18next',
        lookupLocalStorage: 'i18nextLng',
        caches: ['localStorage', 'cookie']
      },
      backend: {
        loadPath: '/static/locales/{{lng}}/translation.json'
      }
    }, function(err, t) {
      // Initialize jQuery-i18next
      jqueryI18next.init(i18next, $, {
        handleName: 'i18n'
      });
      
      updateContent();
      
      // If user is logged in, set the language to their preference
      const userLang = document.querySelector('meta[name="user-language"]')?.content;
      if (userLang && userLang !== i18next.language) {
        changeLanguage(userLang);
      }
    });
  
  // Function to update content when language changes
  function updateContent() {
    // Update document title if there's a title key
    const titleKey = $('title').attr('data-i18n');
    if (titleKey) {
      document.title = i18next.t(titleKey);
    }
    
    // Localize DOM elements
    $('[data-i18n]').i18n();
    
    // Update language dropdown
    const currentLang = document.getElementById('current-language');
    if (currentLang) {
      currentLang.textContent = {
        'en': 'English',
        'pl': 'Polski',
        'cs': 'Čeština'
      }[i18next.language] || 'English';
    }
    
    // Trigger a custom event for other components to react to language changes
    document.dispatchEvent(new CustomEvent('languageChanged', { 
      detail: { language: i18next.language } 
    }));
  }
  
  // Listen for language changes
  i18next.on('languageChanged', () => {
    updateContent();
  });
  
  // Expose the changeLanguage function globally
  window.changeLanguage = function(lang) {
    i18next.changeLanguage(lang);
  };
});

// Helper function to format dates according to current language
function formatDate(date, format) {
  if (!date) return '';
  
  const lang = i18next.language;
  let options = {};
  
  switch(format) {
    case 'short':
      options = { year: 'numeric', month: 'numeric', day: 'numeric' };
      break;
    case 'long':
      options = { year: 'numeric', month: 'long', day: 'numeric' };
      break;
    case 'relative':
      // For relative time, we'll use a custom implementation
      return getRelativeTimeString(date, lang);
    default:
      options = { year: 'numeric', month: 'numeric', day: 'numeric' };
  }
  
  return new Date(date).toLocaleDateString(lang, options);
}

// Helper function to format currency according to current language and currency
function formatCurrencyI18n(amount, currency) {
  if (amount === null || amount === undefined) return '';
  
  const lang = i18next.language;
  const formatter = new Intl.NumberFormat(lang, {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2
  });
  
  return formatter.format(amount);
}

// Helper function for relative time formatting
function getRelativeTimeString(date, lang) {
  const now = new Date();
  const dateObj = new Date(date);
  const diffMs = dateObj - now;
  const diffSec = Math.round(diffMs / 1000);
  const diffMin = Math.round(diffSec / 60);
  const diffHour = Math.round(diffMin / 60);
  const diffDay = Math.round(diffHour / 24);
  
  // Use i18next for translations
  if (diffDay > 0) {
    return i18next.t('time.in_days', { count: diffDay });
  } else if (diffDay < 0) {
    return i18next.t('time.days_ago', { count: Math.abs(diffDay) });
  } else if (diffHour > 0) {
    return i18next.t('time.in_hours', { count: diffHour });
  } else if (diffHour < 0) {
    return i18next.t('time.hours_ago', { count: Math.abs(diffHour) });
  } else if (diffMin > 0) {
    return i18next.t('time.in_minutes', { count: diffMin });
  } else if (diffMin < 0) {
    return i18next.t('time.minutes_ago', { count: Math.abs(diffMin) });
  } else {
    return i18next.t('time.just_now');
  }
}

// Expose formatting helpers globally
window.i18nHelpers = {
  formatDate: formatDate,
  formatCurrency: formatCurrencyI18n
};
