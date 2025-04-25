// Simple translation system
document.addEventListener('DOMContentLoaded', function() {
  // Default language
  let currentLanguage = 'en';
  
  // Try to get language from localStorage
  const storedLanguage = localStorage.getItem('language');
  if (storedLanguage) {
    currentLanguage = storedLanguage;
  }
  
  // Try to get language from user preferences if logged in
  const userLang = document.querySelector('meta[name="user-language"]')?.content;
  if (userLang) {
    currentLanguage = userLang;
  }
  
  // Update UI with current language
  updateLanguageUI(currentLanguage);
  
  // Load translations
  loadTranslations(currentLanguage);
  
  // Global change language function
  window.changeLanguage = function(lang) {
    if (lang && (lang === 'en' || lang === 'pl' || lang === 'cs')) {
      currentLanguage = lang;
      localStorage.setItem('language', lang);
      
      // Update UI and load translations
      updateLanguageUI(lang);
      loadTranslations(lang);
      
      // If user is logged in, save preference
      const saveLanguageUrl = document.querySelector('meta[name="save-language-url"]')?.content;
      if (saveLanguageUrl) {
        fetch(saveLanguageUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.content
          },
          body: JSON.stringify({ language: lang })
        });
      }
    }
  };
  
  // Helper function to update language UI elements
  function updateLanguageUI(lang) {
    const languageNames = {
      'en': 'English',
      'pl': 'Polski',
      'cs': 'Čeština'
    };
    
    const currentLangElem = document.getElementById('current-language');
    if (currentLangElem) {
      currentLangElem.textContent = languageNames[lang] || 'English';
    }
  }
  
  // Load and apply translations
  function loadTranslations(lang) {
    fetch(`/static/locales/${lang}/translation.json`)
      .then(response => response.json())
      .then(translations => {
        applyTranslations(translations);
        
        // Trigger custom event for other components
        document.dispatchEvent(new CustomEvent('languageChanged', { 
          detail: { language: lang } 
        }));
      })
      .catch(error => {
        console.error('Error loading translations:', error);
      });
  }
  
  // Apply translations to elements with data-i18n attribute
  function applyTranslations(translations) {
    // Get all elements with data-i18n attribute
    const elements = document.querySelectorAll('[data-i18n]');
    
    elements.forEach(element => {
      const key = element.getAttribute('data-i18n');
      const translation = getNestedTranslation(translations, key);
      
      if (translation) {
        // If the element is an input with placeholder, set the placeholder
        if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
          element.placeholder = translation;
        } 
        // Otherwise set the text content
        else {
          element.textContent = translation;
        }
      }
    });
  }
  
  // Get nested translation by dot notation
  function getNestedTranslation(obj, path) {
    return path.split('.').reduce((p, c) => (p && p[c]) ? p[c] : null, obj);
  }
});

// Helper function to format dates
function formatDate(date, format) {
  if (!date) return '';
  
  const lang = localStorage.getItem('language') || 'en';
  let options = {};
  
  switch(format) {
    case 'short':
      options = { year: 'numeric', month: 'numeric', day: 'numeric' };
      break;
    case 'long':
      options = { year: 'numeric', month: 'long', day: 'numeric' };
      break;
    default:
      options = { year: 'numeric', month: 'numeric', day: 'numeric' };
  }
  
  return new Date(date).toLocaleDateString(lang, options);
}

// Helper function to format currency
function formatCurrency(amount, currency) {
  if (amount === null || amount === undefined) return '';
  
  const lang = localStorage.getItem('language') || 'en';
  const formatter = new Intl.NumberFormat(lang, {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2
  });
  
  return formatter.format(amount);
}

// Expose formatting helpers globally
window.i18nHelpers = {
  formatDate: formatDate,
  formatCurrency: formatCurrency
};
