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
    } else if (type === 'error') {
        icon.textContent = '✕';
        icon.classList.add('error');
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

// ============================================
// PAGE TRANSITION — Smooth Fade antar Halaman
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    
    // Skip kalau user gak mau animasi
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;
    
    // Handle semua link internal
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href]');
        
        // Skip kalau:
        // - Bukan link
        // - Link external (http)
        // - Link target="_blank"
        // - Link download
        // - Link dengan href="#"
        // - Link dengan anchor (#)
        // - Modifier key (Ctrl/Cmd/Shift untuk buka tab baru)
        // - Sudah dalam proses exit
        if (!link ||
            link.hostname !== window.location.hostname ||
            link.target === '_blank' ||
            link.hasAttribute('download') ||
            link.getAttribute('href') === '#' ||
            link.getAttribute('href').startsWith('#') ||
            e.ctrlKey || e.metaKey || e.shiftKey ||
            document.body.classList.contains('page-exit')) {
            return;
        }
        
        // Prevent default & trigger fade out
        e.preventDefault();
        
        document.body.classList.add('page-exit');
        
        // Navigate setelah fade out kelar (200ms sesuai CSS)
        setTimeout(() => {
            window.location.href = link.href;
        }, 200);
    });
    
    // Handle browser back/forward — pastiin fade in lagi
    window.addEventListener('pageshow', function() {
        document.body.classList.remove('page-exit');
    });
});

// ============================================
// HERO POOL — Toggle, Search, Filter Role
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const heroGrid = document.getElementById('heroGrid');
    if (!heroGrid) return;  // Bukan halaman edit profil
    
    const heroCards = heroGrid.querySelectorAll('.hero-pick-card');
    const heroCounter = document.getElementById('heroCounter');
    const searchInput = document.getElementById('heroSearch');
    const roleChips = document.querySelectorAll('.role-chip');
    const emptyState = document.getElementById('heroEmptyState');
    
    // ============================================
    // 1. KLIK HERO → TOGGLE SELECTED
    // ============================================
    heroGrid.addEventListener('click', function(e) {
        // Skip kalau klik di input (winrate/match)
        if (e.target.tagName === 'INPUT') return;
        
        const card = e.target.closest('.hero-pick-card');
        if (!card) return;
        
        const checkbox = card.querySelector('.hero-checkbox');
        const statsWrap = card.querySelector('.hero-pick-stats');
        
        // Toggle
        const isNowSelected = !card.classList.contains('selected');
        
        const dataInput = card.querySelector('.hero-data-input');

        if (isNowSelected) {
            card.classList.add('selected');
            if (checkbox) checkbox.checked = true;
            if (dataInput) dataInput.disabled = false;
            if (statsWrap) statsWrap.style.display = 'grid';
        } else {
            card.classList.remove('selected');
            if (checkbox) checkbox.checked = false;
            if (dataInput) dataInput.disabled = true;
            if (statsWrap) statsWrap.style.display = 'none';
        }
        
        updateCounter();
    });
    
    // ============================================
    // 2. UPDATE COUNTER
    // ============================================
    function updateCounter() {
        if (!heroCounter) return;
        const selectedCount = heroGrid.querySelectorAll('.hero-pick-card.selected').length;
        heroCounter.textContent = selectedCount;
    }
    
    // Init counter saat page load
    updateCounter();
    
    // ============================================
    // 3. SEARCH BAR (debounced 250ms)
    // ============================================
    let searchTimeout = null;
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(applyFilters, 250);
        });
    }
    
    // ============================================
    // 4. FILTER ROLE (chip buttons)
    // ============================================
    let activeRole = 'all';
    
    roleChips.forEach(chip => {
        chip.addEventListener('click', function() {
            // Update active state
            roleChips.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            
            activeRole = this.dataset.role || 'all';
            applyFilters();
        });
    });
    
    // ============================================
    // 5. APPLY FILTERS (search + role)
    // ============================================
    function applyFilters() {
        const searchTerm = (searchInput?.value || '').toLowerCase().trim();
        let visibleCount = 0;
        
        heroCards.forEach(card => {
            const heroName = (card.dataset.heroName || '').toLowerCase();
            const heroRole = (card.dataset.heroRole || '').toLowerCase();
            
            // Cek search match
            const searchMatch = !searchTerm || heroName.includes(searchTerm);
            
            // Cek role match — CSV string, jadi cek contains
            let roleMatch = true;
            if (activeRole !== 'all') {
                // heroRole format: "mage,tank" atau "fighter"
                const roles = heroRole.split(',').map(r => r.trim());
                roleMatch = roles.includes(activeRole.toLowerCase());
            }
            
            // Show/hide via display
            if (searchMatch && roleMatch) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Empty state
        if (emptyState) {
            emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    }
    
    // ============================================
    // 6. INISIALISASI — counter dari hero yang udah selected
    // ============================================
    // Pastikan stats wrap muncul untuk hero yang udah dipilih dari database
    heroCards.forEach(card => {
        const checkbox = card.querySelector('.hero-checkbox');
        const statsWrap = card.querySelector('.hero-pick-stats');
        
        if (checkbox && checkbox.checked) {
            card.classList.add('selected');
            if (statsWrap) statsWrap.style.display = 'grid';
        }
    });
    
    updateCounter();
});

// ============================================
// HAPUS FOTO — Event Listener (Fix Nested Form)
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const deletePhotoBtn = document.getElementById('deletePhotoBtn');
    
    if (!deletePhotoBtn) return;
    
    deletePhotoBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Confirm modal
        if (typeof showConfirm === 'function') {
            showConfirm(
                'Yakin Hapus Foto?',
                'Tindakan ini gak bisa dibatalin. Foto profil kamu bakal ilang permanen.',
                function() {
                    // Bikin form baru — di LUAR form utama
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = '/profile/edit/photo/delete';
                    document.body.appendChild(form);
                    form.submit();
                },
                {
                    icon: '⚠',
                    okText: 'HAPUS'
                }
            );
        } else {
            if (confirm('Yakin hapus foto profil?')) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/profile/edit/photo/delete';
                document.body.appendChild(form);
                form.submit();
            }
        }
    });
});


// ============================================
// CLIP HANDLER — Add + Delete (AJAX)
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('[MGJ] Binding clip handlers...');
    
    // === ADD CLIP ===
    const addClipBtn = document.getElementById('addClipBtn');
    const clipLinkInput = document.getElementById('clipLink');
    const clipPreview = document.getElementById('clipPreview');
    const clipPreviewImg = document.getElementById('clipPreviewImg');
    const clipPreviewFallback = document.getElementById('clipPreviewFallback');
    
    // Preview thumbnail saat user ketik link YouTube
    if (clipLinkInput) {
        clipLinkInput.addEventListener('input', function() {
            const link = this.value.trim();
            const youtubeRegex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([\w-]{11})/;
            const match = link.match(youtubeRegex);
            
            if (match && clipPreview && clipPreviewImg) {
                const videoId = match[1];
                clipPreviewImg.src = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
                clipPreview.style.display = 'block';
                if (clipPreviewFallback) clipPreviewFallback.style.display = 'none';
            } else if (clipPreview) {
                clipPreview.style.display = 'none';
            }
        });
    }
    
    if (addClipBtn) {
        addClipBtn.addEventListener('click', async function() {
            const judul = document.getElementById('clipJudul').value.trim();
            const link = document.getElementById('clipLink').value.trim();
            
            if (!judul || !link) {
                showToast('Data Belum Lengkap', 'Judul dan link wajib diisi.', 'error');
                return;
            }
            
            addClipBtn.disabled = true;
            addClipBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> MENYIMPAN...';
            
            try {
                const formData = new URLSearchParams();
                formData.append('judul', judul);
                formData.append('link', link);
                
                const response = await fetch('/profile/edit/clip', {
                    method: 'POST',
                    body: formData,
                    credentials: 'include',
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('clipJudul').value = '';
                    document.getElementById('clipLink').value = '';
                    if (clipPreview) clipPreview.style.display = 'none';
                    
                    showToast('Clip Ditambahkan!', 'Clip berhasil diupload.', 'success', 2000);
                    
                    // Reload halaman biar clip muncul di list (data aman di database)
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showToast('Gagal', data.message || 'Coba lagi.', 'error');
                    addClipBtn.disabled = false;
                    addClipBtn.innerHTML = '<i class="fa-solid fa-plus"></i> TAMBAH CLIP';
                }
            } catch (error) {
                console.error(error);
                showToast('Error', 'Ada masalah koneksi.', 'error');
                addClipBtn.disabled = false;
                addClipBtn.innerHTML = '<i class="fa-solid fa-plus"></i> TAMBAH CLIP';
            }
        });
    }
    
    // === DELETE CLIP ===
    document.querySelectorAll('.btn-delete-clip').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const clipId = this.dataset.clipId;
            
            showConfirm(
                'Hapus Clip?',
                'Yakin hapus clip ini?',
                function() {
                    fetch('/profile/edit/clip/delete/' + clipId, {
                        method: 'POST',
                        credentials: 'include',
                    })
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            showToast('Clip Dihapus', 'Berhasil.', 'success', 2000);
                            setTimeout(() => window.location.reload(), 1000);
                        } else {
                            showToast('Gagal', data.message || 'Coba lagi.', 'error');
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        showToast('Error', 'Gagal hapus.', 'error');
                    });
                },
                { icon: '⚠', okText: 'HAPUS' }
            );
        });
    });
});


// ============================================
// ACHIEVEMENT HANDLER — Add + Delete (AJAX)
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('[MGJ] Binding achievement handlers...');
    
    // === ADD ACHIEVEMENT ===
    const addAchievementBtn = document.getElementById('addAchievementBtn');
    
    if (addAchievementBtn) {
        addAchievementBtn.addEventListener('click', async function() {
            const judul = document.getElementById('achJudul').value.trim();
            const deskripsi = document.getElementById('achDeskripsi').value.trim();
            const tanggal = document.getElementById('achTanggal').value;
            
            if (!judul) {
                showToast('Judul Kosong', 'Judul achievement wajib diisi.', 'error');
                return;
            }
            
            addAchievementBtn.disabled = true;
            addAchievementBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> MENYIMPAN...';
            
            try {
                const formData = new URLSearchParams();
                formData.append('judul', judul);
                formData.append('deskripsi', deskripsi);
                formData.append('tanggal', tanggal);
                
                const response = await fetch('/profile/edit/achievement', {
                    method: 'POST',
                    body: formData,
                    credentials: 'include',
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('achJudul').value = '';
                    document.getElementById('achDeskripsi').value = '';
                    document.getElementById('achTanggal').value = '';
                    
                    showToast('Achievement Ditambahkan!', 'Prestasi tersimpan.', 'success', 2000);
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showToast('Gagal', data.message || 'Coba lagi.', 'error');
                    addAchievementBtn.disabled = false;
                    addAchievementBtn.innerHTML = '<i class="fa-solid fa-trophy"></i> TAMBAH ACHIEVEMENT';
                }
            } catch (error) {
                console.error(error);
                showToast('Error', 'Ada masalah koneksi.', 'error');
                addAchievementBtn.disabled = false;
                addAchievementBtn.innerHTML = '<i class="fa-solid fa-trophy"></i> TAMBAH ACHIEVEMENT';
            }
        });
    }
    
    // === DELETE ACHIEVEMENT ===
    document.querySelectorAll('.btn-delete-ach').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const achId = this.dataset.achId;
            
            showConfirm(
                'Hapus Achievement?',
                'Yakin hapus achievement ini?',
                function() {
                    fetch('/profile/edit/achievement/delete/' + achId, {
                        method: 'POST',
                        credentials: 'include',
                    })
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            showToast('Achievement Dihapus', 'Berhasil.', 'success', 2000);
                            setTimeout(() => window.location.reload(), 1000);
                        } else {
                            showToast('Gagal', data.message || 'Coba lagi.', 'error');
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        showToast('Error', 'Gagal hapus.', 'error');
                    });
                },
                { icon: '⚠', okText: 'HAPUS' }
            );
        });
    });
});


// ============================================
// BROWSE GAMER — Live Search
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('gamerSearch');
    const gamerGrid = document.getElementById('gamerGrid');
    const emptyState = document.getElementById('gamerEmptyState');

    if (!searchInput || !gamerGrid) return; // Bukan halaman browse

    const gamerCards = gamerGrid.querySelectorAll('.gamer-card');

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        let visibleCount = 0;

        gamerCards.forEach(card => {
            // Ambil data-name (isinya: "username nickname")
            const gamerName = card.dataset.name || '';
            
            if (gamerName.includes(searchTerm)) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Tampilkan empty state kalau gak ada hasil
        if (emptyState) {
            emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    });
});