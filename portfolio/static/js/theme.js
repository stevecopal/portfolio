// Theme Toggle Functionality
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const themeToggleMobile = document.getElementById('themeToggleMobile');
    const themeIcon = document.getElementById('themeIcon');
    const themeIconMobile = document.getElementById('themeIconMobile');
    const html = document.documentElement;
    
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
        html.classList.add('dark');
        updateThemeIcon(true);
    } else {
        html.classList.remove('dark');
        updateThemeIcon(false);
    }
    
    function toggleTheme() {
        html.classList.toggle('dark');
        const isDark = html.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        updateThemeIcon(isDark);
        // Notify tech-background canvas of theme change
        if (typeof window.updateTechBackgroundTheme === 'function') {
            window.updateTechBackgroundTheme();
        }
    }
    
    function updateThemeIcon(isDark) {
        // Icône Soleil en Mode Dark (pour repasser en Light) / Lune en Mode Light
        const sunPath = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />';
        const moonPath = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />';

        if (themeIcon) {
            themeIcon.innerHTML = isDark ? sunPath : moonPath;
        }
        if (themeIconMobile) {
            themeIconMobile.innerHTML = isDark ? sunPath : moonPath;
        }
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    if (themeToggleMobile) {
        themeToggleMobile.addEventListener('click', toggleTheme);
    }
    
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            html.classList.toggle('dark', e.matches);
            updateThemeIcon(e.matches);
            if (typeof window.updateTechBackgroundTheme === 'function') {
                window.updateTechBackgroundTheme();
            }
        }
    });
}

// Initialisation au chargement du DOM
document.addEventListener('DOMContentLoaded', initThemeToggle);