# Samjna – Flask Web UI

## Architecture – Persistent Camera Across Screens

This app uses a **single-page assessment shell** (`/assessment`) to exactly
match the Tkinter app's camera lifecycle: the original opens
`cv2.VideoCapture(0)` **once** at Face Calibration and keeps it alive for the
entire session (`CameraManager` singleton) — no screen ever re-opens it.

A browser cannot keep a `MediaStream` alive across a full page navigation
(each page load is a fresh JS context), so the only faithful way to replicate
"camera stays active across screens" is a single persistent page that swaps
content via `fetch()` instead of `window.location` redirects:

```
/consent              ← normal page, no camera
        ↓ (redirect)
/assessment            ← SPA shell loads ONCE; mounts global camera preview
        ↓ fetch (no reload)
  Face Calibration      ← getUserMedia() called HERE, exactly once
        ↓ fetch (no reload)
  Eye Calibration        ← reuses the same MediaStream, no new getUserMedia()
        ↓ fetch (no reload)
  Interview Q1 … Q11      ← reuses the same MediaStream for every recording
        ↓ fetch (no reload)
  PSS Test                  ← no recording (matches Tkinter — PSS never touches camera)
        ↓ fetch (no reload)
  Thank You                  ← releases all MediaStream tracks (session end)
```

`static/js/assessment_shell.js` owns the one `MediaStream` object
(`window.Samjna.getStream()`); every other fragment reads it but never calls
`getUserMedia()` itself. If a track ends unexpectedly (device unplugged,
permission revoked), the shell auto-attempts a single reconnect.

All original Flask routes are preserved unchanged (`/face-calibration`,
`/eye-calibration`, `/interview/<phase>/<q>`, `/pss`, `/thank-you`, `/admin`,
etc.) — they now render **fragments** when called via the shell's `fetch()`
(detected via the `X-Requested-With: XMLHttpRequest` header) and fall back to
a redirect-into-the-shell page when visited directly (e.g. bookmark, refresh).

---

## Project Structure

```
flask_app/
├── app.py                  # Flask routes (UI layer only)
├── models.py               # SQLAlchemy DB models
├── requirements.txt
├── Procfile                # Railway deployment
├── railway.json
├── nixpacks.toml
├── utils/
│   ├── __init__.py
│   ├── questions.py         # ← UNCHANGED from original project
│   ├── output_manager.py    # Output/<Name>_<ts>/ folder + file writer, with logging
│   └── media_convert.py     # FFmpeg WebM → MP4/WAV conversion, with logging
├── static/
│   ├── css/main.css
│   └── js/
│       ├── main.js
│       └── assessment_shell.js   # Owns the single persistent MediaStream
└── templates/
    ├── base.html
    ├── consent.html
    ├── assessment_shell.html      # SPA shell (mounts global camera preview)
    ├── face_calibration.html      # Fallback redirect → /assessment
    ├── eye_calibration.html       # Fallback redirect → /assessment
    ├── interview.html             # Fallback redirect → /assessment
    ├── pss_test.html              # Fallback redirect → /assessment
    ├── thank_you.html
    ├── admin.html
    ├── admin_session.html
    └── fragments/                 # Rendered into the SPA shell via fetch()
        ├── face_calibration_fragment.html   # getUserMedia() called HERE only
        ├── eye_calibration_fragment.html    # reuses existing stream
        ├── interview_fragment.html          # reuses existing stream, records
        ├── pss_test_fragment.html           # no camera; fixed radio grouping
        └── thank_you_fragment.html          # releases all MediaStream tracks
```

---

## Logging

All camera/recording/upload/conversion events are logged server-side via
Python's `logging` module (logger name `"samjna"`), and client-side via
`console.log`/`console.warn` prefixed `[Samjna]`. Covered events:

- Camera/microphone initialization (success/failure, per session — once)
- MediaRecorder start/stop for every question (video + audio separately)
- Video upload received → FFmpeg conversion → success/failure
- Audio upload received → FFmpeg conversion → success/failure
- Output folder/file paths created
- Stream loss + reconnect attempts

Server logs print to stdout; on Railway these appear in the deployment logs.

---

## Screen Flow (identical to Tkinter)

```
Consent → Face Calibration → Eye Calibration (9-dot) →
Interview Phase 1 (Baseline, 3 Qs) →
Interview Phase 2 (Social Stress, 3 Qs) →
Interview Phase 3 (Cognitive Load, 3 Qs) →
Interview Phase 4 (Recovery, 2 Qs) →
PSS-10 Test →
Thank You / Session Complete
```

---

## Local Setup

**Requires `ffmpeg`** to be installed on your machine (used to convert the
browser's recorded WebM into proper `.mp4` / `.wav` files):

```bash
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
# Windows: download from https://ffmpeg.org/download.html and add to PATH
```

```bash
cd flask_app
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
# → Open http://localhost:5000
```

The SQLite database (`samjna.db`) is created automatically in the project folder on first run.

---

## Where Data is Stored

| Table              | Contents                                          |
|--------------------|---------------------------------------------------|
| `sessions`         | Participant name, language, event log (JSON)      |
| `gaze_records`     | 9 dot positions + click offsets per session       |
| `interview_events` | Start/end/restart events per question per phase   |
| `pss_results`      | Individual answers, total score, interpretation   |

Access all data at **`/admin`** (no login required by default).

---

## Deploy to Railway

### ⚠️ Important – Persistent Storage on Railway

Railway's filesystem is **ephemeral**: anything written to disk is wiped on
every redeploy or restart. Since this app saves real MP4/WAV recordings and
CSV/JSON files to disk, you **must** attach a Railway **Volume** for the data
to survive:

1. In your Railway project → **Settings** → **Volumes** → **New Volume**
2. Mount path: `/data`
3. Add environment variable: `OUTPUT_BASE_DIR=/data/Output`

Without this, recordings will be lost whenever Railway restarts the container.
For SQLite, also point `DATABASE_URL` at a file inside the same volume, e.g.
`sqlite:////data/samjna.db` — or better, attach a Railway PostgreSQL plugin
(see below).


### Option A – Railway CLI

```bash
npm install -g @railway/cli
railway login
railway init          # creates a new project
railway up            # deploys from current directory
```

Then in the Railway dashboard:
- Add environment variable: `SECRET_KEY=<your-random-string>`
- Railway auto-detects Python via `nixpacks.toml` and runs gunicorn

### Option B – GitHub Deploy

1. Push this folder to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
3. Select the repo → Railway auto-builds and deploys
4. Set `SECRET_KEY` in Settings → Variables

### Environment Variables

| Variable       | Required | Description                                      |
|----------------|----------|--------------------------------------------------|
| `SECRET_KEY`   | Yes      | Flask session secret (set a long random string)  |
| `DATABASE_URL` | No       | PostgreSQL URL for production (else SQLite used) |
| `OUTPUT_BASE_DIR` | Recommended on Railway | Path to a mounted Volume, e.g. `/data/Output`, so recordings survive restarts |
| `PORT`         | No       | Set automatically by Railway                     |

### Using PostgreSQL on Railway (recommended for production)

1. In Railway dashboard, click **New** → **Database** → **PostgreSQL**
2. Railway auto-sets `DATABASE_URL` — the app reads it automatically

---

## Using Collected Data with Your Existing Analysis Code

The data saved in SQLite can be accessed by your existing analysis scripts:

```python
import sqlite3, json

conn = sqlite3.connect("samjna.db")

# PSS results
for row in conn.execute("SELECT * FROM pss_results"):
    print(row)

# Gaze calibration
for row in conn.execute("SELECT * FROM gaze_records WHERE session_id=1"):
    print(row)

# Session event log
for row in conn.execute("SELECT participant_name, events_json FROM sessions"):
    events = json.loads(row[1])
    print(row[0], events)
```

Or use the existing `OutputManager` by reading from the DB and re-creating
the same CSV/JSON file structure it expects.
