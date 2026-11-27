# 🎮 MyGamingJourney

Platform Portofolio Esport untuk Player Mobile Legends: Bang Bang di Indonesia.

**"Show Your Skill. Get Scouted."**

[![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-3.1.1-4A44C6)](https://flask-sqlalchemy.palletsprojects.com/)
[![Flask-Login](https://img.shields.io/badge/Flask--Login-0.6.3-2E7D32)](https://flask-login.readthedocs.io/)
[![MySQL](https://img.shields.io/badge/MySQL-PyMySQL-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLite](https://img.shields.io/badge/SQLite-optional-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

## 📖 Deskripsi
MyGamingJourney adalah aplikasi web yang dibangun untuk membantu para gamer MLBB membangun portofolio profesional. Aplikasi ini memungkinkan pemain untuk mendaftarkan akun, menampilkan hero pool, menyimpan highlight clip, mencatat prestasi, dan memudahkan Coach/Scout menemukan talenta berbakat.

## ✨ Fitur Utama
- **Autentikasi Aman**: Register & Login dengan hashing password (Werkzeug).
- **Manajemen Profil**: Edit biodata, rank, role (single/multi/all-role), dan status ketersediaan tim.
- **Hero Pool**: Pilih dari **133 hero MLBB** lengkap beserta statistik Winrate & Total Match.
- **Highlight Clip**: Simpan link video YouTube/TikTok/IG. Dilengkapi sistem **Vote (Upvote/Downvote)** yang mencegah *double-vote*.
- **Achievement**: Catat prestasi turnamen dengan upload foto bukti (AJAX upload tanpa reload).
- **Gamer Directory**: Cari pemain berbakat dengan fitur *Live Search*.
- **UI/UX**: Tema *Neon Cyberpunk*, animasi AOS, *Toast Notification*, *Modal Confirm*, dan *Page Transition*.
- **Testing**: Dilengkapi *Unit Testing* menggunakan `pytest` (Auth, Model, Routing).

## 🛠️ Tech Stack
- **Backend**: Python 3 (Flask, Flask-Login, SQLAlchemy)
- **Database**: MySQL (Production) / SQLite (Testing)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6)
- **Testing**: Pytest

## ⚙️ Cara Menjalankan (Local)
1. Clone repo ini: `git clone https://github.com/softstatick/mygamingjourney.git`
2. Buat virtual environment: `python -m venv .venv`
3. Aktifkan venv: `.venv\Scripts\Activate.ps1` (Windows PowerShell) atau `source .venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Buat file `.env` di root, isi dengan:
   ```env
   SECRET_KEY=rahasia-super-aman
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=mygamingjourney
   ```

## ▶️ Jalankan Server

```powershell
python app.py
```

Buka http://localhost:5000. Set `FLASK_DEBUG=1` untuk mode debug, `FLASK_PORT` untuk ubah port.

## 🛠️ Troubleshooting (PowerShell)

**`RuntimeError: SECRET_KEY tidak di-set`** — `SECRET_KEY` wajib. Pastikan `.env` di root (sudah gitignored) berisi `SECRET_KEY=...`, atau sekali-pakai `$env:SECRET_KEY="kunci"; python app.py`. PowerShell pakai `$env:NAMA=...`, bukan `NAMA=...`.

**Virtualenv** — aktifkan dengan `.venv\Scripts\Activate.ps1`, bukan `activate`/`activate.bat` (itu buat cmd). Kalau *"running scripts is disabled"*: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Cek `(Get-Command python).Source`, atau `.venv\Scripts\python.exe app.py`.

**`can't open file ... app.py`** — `cd` dulu ke root project.

**Error database** — pastikan MySQL jalan & database `mygamingjourney` ada; atau pakai SQLite `$env:DATABASE_URL="sqlite:///mygamingjourney.db"`.
