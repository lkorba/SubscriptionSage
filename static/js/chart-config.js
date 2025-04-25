// Chart.js Configuration
document.addEventListener('DOMContentLoaded', function() {
  // Set default Chart.js configuration
  Chart.defaults.color = '#fff';
  Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
  Chart.defaults.font.family = "'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', sans-serif";
  
  // Custom color themes for charts
  window.chartColors = {
    primary: 'rgba(13, 110, 253, 0.8)',
    success: 'rgba(25, 135, 84, 0.8)',
    danger: 'rgba(220, 53, 69, 0.8)',
    warning: 'rgba(255, 193, 7, 0.8)',
    info: 'rgba(13, 202, 240, 0.8)',
    secondary: 'rgba(108, 117, 125, 0.8)',
    light: 'rgba(248, 249, 250, 0.8)',
    dark: 'rgba(33, 37, 41, 0.8)',
    // Custom colors for charts
    blue: 'rgba(54, 162, 235, 0.8)',
    red: 'rgba(255, 99, 132, 0.8)',
    green: 'rgba(75, 192, 192, 0.8)',
    yellow: 'rgba(255, 206, 86, 0.8)',
    purple: 'rgba(153, 102, 255, 0.8)',
    orange: 'rgba(255, 159, 64, 0.8)'
  };
  
  // Default chart color palettes
  window.colorPalettes = {
    // For pie/doughnut charts
    categorical: [
      window.chartColors.red,
      window.chartColors.blue,
      window.chartColors.yellow,
      window.chartColors.green,
      window.chartColors.purple,
      window.chartColors.orange
    ],
    // For bar/line charts (can be expanded)
    sequential: [
      window.chartColors.primary,
      window.chartColors.success,
      window.chartColors.info,
      window.chartColors.warning,
      window.chartColors.danger
    ]
  };
  
  // Custom tooltip formatting
  const currencyFormatter = new Intl.NumberFormat(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
  
  // Helper function to create consistent tooltip for currency values
  window.currencyTooltip = function(context) {
    let label = context.dataset.label || '';
    if (label) {
      label += ': ';
    }
    
    if (context.parsed.y !== null) {
      const userCurrency = document.querySelector('meta[name="user-currency"]')?.content || 'USD';
      label += currencyFormatter.format(context.parsed.y) + ' ' + userCurrency;
    }
    return label;
  };
  
  // Helper function to create responsive charts
  window.createResponsiveChart = function(chartId, type, data, options) {
    const ctx = document.getElementById(chartId);
    if (!ctx) return null;
    
    // Apply responsive options
    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#fff',
            padding: 10,
            usePointStyle: true,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(33, 37, 41, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 10,
          cornerRadius: 4,
          displayColors: true
        }
      }
    };
    
    // Merge default options with provided options
    const mergedOptions = deepMerge(defaultOptions, options || {});
    
    // Create and return chart
    return new Chart(ctx, {
      type: type,
      data: data,
      options: mergedOptions
    });
  };
  
  // Helper function to deep merge objects
  function deepMerge(target, source) {
    const output = Object.assign({}, target);
    
    if (isObject(target) && isObject(source)) {
      Object.keys(source).forEach(key => {
        if (isObject(source[key])) {
          if (!(key in target)) {
            Object.assign(output, { [key]: source[key] });
          } else {
            output[key] = deepMerge(target[key], source[key]);
          }
        } else {
          Object.assign(output, { [key]: source[key] });
        }
      });
    }
    
    return output;
  }
  
  function isObject(item) {
    return (item && typeof item === 'object' && !Array.isArray(item));
  }
});
