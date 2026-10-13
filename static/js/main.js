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

// ============================================
// PHOTO UPLOAD PREVIEW
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photoInput');
    const photoPreview = document.getElementById('photoPreview');
    const fileName = document.getElementById('fileName');
    
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            // Update label text
            if (fileName) {
                fileName.textContent = file.name;
            }
            
            // Preview gambar
            if (photoPreview && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    // Ganti div placeholder jadi img
                    if (photoPreview.tagName === 'DIV') {
                        const newImg = document.createElement('img');
                        newImg.id = 'photoPreview';
                        newImg.className = 'photo-preview';
                        newImg.src = event.target.result;
                        newImg.alt = 'Preview';
                        photoPreview.replaceWith(newImg);
                    } else {
                        photoPreview.src = event.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

// ============================================
// TOAST NOTIFICATION SYSTEM
// ============================================

let toastTimer = null;

function showToast(title, message, type = 'success', duration = 3000) {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toastIcon');
    const titleEl = document.getElementById('toastTitle');
    const messageEl = document.getElementById('toastMessage');
    const progressBar = document.getElementById('toastProgressBar');
    
    if (!toast) return;
    
    // Reset class
    toast.className = 'toast';
    toast.classList.add(`toast-${type}`);
    
    // Set content
    titleEl.textContent = title;
    messageEl.textContent = message;
    
    // Set icon
   if (type === 'success') {
       icon.textContent = '✓';
   } else if (type === 'error') {
       icon.textContent = '✕';
   } else if (type === 'info') {
       icon.textContent = 'ℹ';
   }
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('active');
    }, 10);
    
    // Reset progress bar
    progressBar.style.transition = 'none';
    progressBar.style.width = '0%';
    void progressBar.offsetWidth;
    
    // Animate progress bar
    progressBar.style.transition = `width ${duration}ms linear`;
    progressBar.style.width = '100%';
    
    // Auto-close
    clearTimeout(toastTimer);
    toastTimer = setTimeout(closeToast, duration);
}

function closeToast() {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    clearTimeout(toastTimer);
    toast.classList.remove('active');
}

// ============================================
// AUTO-UPLOAD FOTO PROFIL (via AJAX)
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photoInput');
    
    if (photoInput) {
        photoInput.addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            // Validasi ukuran (max 5 MB)
            if (file.size > 5 * 1024 * 1024) {
                showToast('File Terlalu Besar', 'Maksimal 5 MB.', 'error');
                photoInput.value = '';
                return;
            }
            
            // Validasi tipe
            if (!file.type.startsWith('image/')) {
                showToast('Format Salah', 'Pilih file gambar (JPG, PNG, WEBP, GIF).', 'error');
                photoInput.value = '';
                return;
            }
            
            // Update label ke loading state
            const fileName = document.getElementById('fileName');
            const photoPreview = document.getElementById('photoPreview');
            
            if (fileName) {
                fileName.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
            }
            
            // Buat FormData
            const formData = new FormData();
            formData.append('photo', file);
            
            try {
                // Kirim ke server via fetch
                const response = await fetch('/profile/edit/photo', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Update preview foto
                    if (photoPreview) {
                        if (photoPreview.tagName === 'DIV') {
                            // Ganti div placeholder dengan img
                            const newImg = document.createElement('img');
                            newImg.id = 'photoPreview';
                            newImg.className = 'photo-preview';
                            newImg.src = data.foto_url + '?t=' + Date.now(); // cache-bust
                            newImg.alt = 'Preview';
                            photoPreview.replaceWith(newImg);
                        } else {
                            photoPreview.src = data.foto_url + '?t=' + Date.now();
                        }
                    }
                    
                    // Reset label
                    if (fileName) {
                        fileName.textContent = 'Pilih Foto Lain (Max 5 MB)';
                    }
                    
                    // Update UI — sembunyikan tombol pilih foto, tampilkan tombol hapus
                    const photoInputWrap = document.getElementById('photoInputWrap');
                    const photoDeleteWrap = document.getElementById('photoDeleteWrap');

                    if (photoInputWrap) {
                        photoInputWrap.style.display = 'none';
                    }

                    if (photoDeleteWrap) {
                        photoDeleteWrap.style.display = 'block';
                    }

                    // Tampilkan toast
                    showToast('Foto Berhasil Diupload!', 'Foto profil kamu udah diganti.', 'success', 3000);

                    // ✨ RELOAD DIHAPUS — biar UX smooth tanpa refresh
                    
                } else {
                    // Error dari server
                    if (fileName) {
                        fileName.textContent = 'Pilih Foto (Max 5 MB)';
                    }
                    showToast('Upload Gagal', data.message || 'Coba lagi.', 'error');
                    photoInput.value = '';
                }
                
            } catch (error) {
                console.error('Upload error:', error);
                
                if (fileName) {
                    fileName.textContent = 'Pilih Foto (Max 5 MB)';
                }
                showToast('Upload Gagal', 'Ada masalah koneksi. Coba lagi.', 'error');
                photoInput.value = '';
            }
        });
    }
});

// ============================================
// CONFIRM MODAL SYSTEM
// ============================================

let confirmCallback = null;

function showConfirm(title, message, onConfirm, options = {}) {
    const overlay = document.getElementById('confirmOverlay');
    const icon = document.getElementById('confirmIcon');
    const titleEl = document.getElementById('confirmTitle');
    const messageEl = document.getElementById('confirmMessage');
    const okBtn = document.getElementById('confirmOkBtn');
    const cancelBtn = document.getElementById('confirmCancelBtn');
    
    if (!overlay) return;
    
    // Set content
    titleEl.textContent = title;
    messageEl.textContent = message;
    icon.textContent = options.icon || '⚠';
    
    // Custom OK button text + icon
    if (options.okText) {
        okBtn.innerHTML = `<i class="fa-solid fa-trash"></i> ${options.okText}`;
    }
    
    // Set callback
    confirmCallback = onConfirm;
    
    // Show
    overlay.classList.add('active');
    
    // Handlers (remove dulu biar gak numpuk)
    okBtn.onclick = () => {
        overlay.classList.remove('active');
        if (confirmCallback) confirmCallback();
        confirmCallback = null;
    };
    
    cancelBtn.onclick = () => {
        overlay.classList.remove('active');
        confirmCallback = null;
    };
    
    overlay.onclick = (e) => {
        if (e.target === overlay) {
            overlay.classList.remove('active');
            confirmCallback = null;
        }
    };
}

// Close confirm on Esc
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const overlay = document.getElementById('confirmOverlay');
        if (overlay && overlay.classList.contains('active')) {
            overlay.classList.remove('active');
            confirmCallback = null;
        }
    }
});

// ============================================
// HANDLE DELETE PHOTO — pakai custom confirm modal
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const deletePhotoBtn = document.getElementById('deletePhotoBtn');
    const deletePhotoForm = document.getElementById('deletePhotoForm');
    
    if (deletePhotoBtn && deletePhotoForm) {
        deletePhotoBtn.addEventListener('click', function() {
            showConfirm(
                'Yakin Hapus Foto?',
                'kalo udah di hapus tinggal pilih foto lagi aja der.',
                function() {
                    // Kalau user klik HAPUS → submit form
                    deletePhotoForm.submit();
                },
                {
                    icon: '⚠',
                    okText: 'HAPUS'
                }
            );
        });
    }
});

// ============================================
// ALL ROLE TOGGLE — Show/Hide Role 2 & 3
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const allRoleCheckbox = document.getElementById('allRoleCheckbox');
    const roleFieldsWrap = document.getElementById('roleFieldsWrap');
    
    if (allRoleCheckbox && roleFieldsWrap) {
        allRoleCheckbox.addEventListener('change', function() {
            if (this.checked) {
                // Sembunyiin role fields
                roleFieldsWrap.style.opacity = '0';
                roleFieldsWrap.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    roleFieldsWrap.style.display = 'none';
                }, 200);
            } else {
                // Munculin role fields
                roleFieldsWrap.style.display = 'block';
                
                // Force reflow
                void roleFieldsWrap.offsetWidth;
                
                roleFieldsWrap.style.opacity = '1';
                roleFieldsWrap.style.transform = 'translateY(0)';
            }
        });
    }
});

// ============================================
// COMING SOON TOAST — buat tombol yang belum berfungsi
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const comingSoonBtns = document.querySelectorAll('[data-feature]');
    
    comingSoonBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const featureName = this.dataset.feature || 'Fitur ini';
            showToast(
                `${featureName} — Coming Soon!`,
                'Fitur ini lagi dalam pengembangan. Stay tuned!',
                'info',
                3000
            );
        });
    });
});