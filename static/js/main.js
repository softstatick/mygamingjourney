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

// ============================================
// MODAL POPUP SYSTEM
// ============================================

let modalTimer = null;

function showModal(title, message, type = 'success') {
    const overlay = document.getElementById('modalOverlay');
    const icon = document.getElementById('modalIcon');
    const titleEl = document.getElementById('modalTitle');
    const messageEl = document.getElementById('modalMessage');
    const progressBar = document.getElementById('modalProgressBar');
    
    if (!overlay) return;
    
    // Set content
    titleEl.textContent = title;
    messageEl.textContent = message;
    
    // Set icon + color based on type
    icon.className = 'modal-icon';
    if (type === 'success') {
        icon.textContent = '✓';
        icon.classList.add('success');
    } else if (type === 'welcome') {
        icon.textContent = '👋';
        icon.classList.add('welcome');
    } else if (type === 'goodbye') {
        icon.textContent = '👋';
        icon.classList.add('goodbye');
    }
    
    // Show modal
    overlay.classList.add('active');
    
    // Animate progress bar (2 seconds)
    progressBar.style.transition = 'none';
    progressBar.style.width = '0%';
    
    // Trigger reflow
    void progressBar.offsetWidth;
    
    progressBar.style.transition = 'width 2000ms linear';
    progressBar.style.width = '100%';
    
    // Auto-close after 2 seconds
    clearTimeout(modalTimer);
    modalTimer = setTimeout(closeModal, 2000);
    
    // Close on click
    overlay.onclick = closeModal;
}

function closeModal() {
    const overlay = document.getElementById('modalOverlay');
    if (!overlay) return;
    
    clearTimeout(modalTimer);
    overlay.classList.remove('active');
}

// Close on ESC key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});