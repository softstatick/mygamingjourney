// ============================================
// MYGAMINGJOURNEY — MAIN JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== INIT AOS ====================
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100,
        });
    }
    
    // ==================== THEME TOGGLE ====================
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('mgj-theme') || 'dark';
    
    // Apply saved theme on load
    if (savedTheme === 'light') {
        document.body.classList.add('light');
        updateThemeIcon('light');
    }
    
    // Handle toggle click
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const isLight = document.body.classList.toggle('light');
            const newTheme = isLight ? 'light' : 'dark';
            localStorage.setItem('mgj-theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }
});

// Update icon based on theme
function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;
    
    const icon = themeToggle.querySelector('i');
    if (!icon) return;
    
    if (theme === 'light') {
        icon.className = 'fa-solid fa-moon';
    } else {
        icon.className = 'fa-solid fa-sun';
    }
}