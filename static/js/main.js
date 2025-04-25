// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
  // Initialize tooltips
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
  
  // Set default form currency from user preference
  const userPreferredCurrency = document.querySelector('meta[name="user-currency"]')?.content;
  if (userPreferredCurrency) {
    const currencySelects = document.querySelectorAll('select[name="currency"]');
    currencySelects.forEach(select => {
      if (select && !select.value) {
        select.value = userPreferredCurrency;
      }
    });
  }
  
  // Format currency inputs
  const amountInputs = document.querySelectorAll('input[name="amount"]');
  amountInputs.forEach(input => {
    input.addEventListener('blur', formatCurrencyValue);
  });
  
  // Form validation
  const forms = document.querySelectorAll('.needs-validation');
  forms.forEach(form => {
    form.addEventListener('submit', function(event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
});

// Format currency values
function formatCurrencyValue(e) {
  const input = e.target;
  if (input.value) {
    const value = parseFloat(input.value);
    if (!isNaN(value)) {
      input.value = value.toFixed(2);
    }
  }
}

// This function is now defined in i18n.js
// changeLanguage(lang) { ... }

// Currency conversion helper
function convertCurrency(amount, fromCurrency, toCurrency) {
  // Get exchange rates from the data attribute or API
  const exchangeRates = window.exchangeRates || {};
  
  if (fromCurrency === toCurrency) {
    return amount;
  }
  
  // Direct conversion
  if (exchangeRates[fromCurrency] && exchangeRates[fromCurrency][toCurrency]) {
    return amount * exchangeRates[fromCurrency][toCurrency];
  }
  
  // Convert via USD if direct rate not available
  if (exchangeRates[fromCurrency]?.USD && exchangeRates.USD?.[toCurrency]) {
    const amountInUSD = amount * exchangeRates[fromCurrency].USD;
    return amountInUSD * exchangeRates.USD[toCurrency];
  }
  
  // If no conversion possible, return original amount
  console.warn(`Could not convert from ${fromCurrency} to ${toCurrency}`);
  return amount;
}

// Format currency for display
function formatCurrency(amount, currency) {
  const currencySymbols = {
    'USD': '$',
    'EUR': '€',
    'CZK': 'Kč',
    'PLN': 'zł'
  };
  
  const symbol = currencySymbols[currency] || currency;
  
  if (currency === 'CZK' || currency === 'PLN') {
    return `${amount.toFixed(2)} ${symbol}`;
  } else {
    return `${symbol}${amount.toFixed(2)}`;
  }
}
