// Theme management
(function(){
  const theme = localStorage.getItem('aeroscope-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', theme);
  updateThemeIcon(theme);
})();

function toggleTheme(){
  const curr = document.documentElement.getAttribute('data-theme');
  const next = curr === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('aeroscope-theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme){
  const icon = document.getElementById('themeIcon');
  if(icon) icon.className = theme === 'dark' ? 'ti ti-sun' : 'ti ti-moon';
}

// Chart.js global defaults
if(typeof Chart !== 'undefined'){
  Chart.defaults.color = '#6b7fa3';
  Chart.defaults.borderColor = '#1e2d4a';
  Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif";
  Chart.defaults.font.size = 11;
}

// Animate number counting
function animateCount(el, target){
  if(!el) return;
  let cur = 0;
  const step = target / 60;
  const t = setInterval(()=>{
    cur = Math.min(cur + step, target);
    el.textContent = Math.floor(cur).toLocaleString();
    if(cur >= target) clearInterval(t);
  }, 20);
}

// Format helpers
function fmtAlt(ft){ return ft ? ft.toLocaleString() + ' ft' : '—'; }
function fmtSpd(kts){ return kts ? kts + ' kts' : '—'; }
