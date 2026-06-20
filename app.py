# =============================================================================
# app.py  – Samjna Flask UI
# Identical folder/file output to the Tkinter version.
# Browser records video (webm) + audio (wav) via MediaRecorder API.
# Files land on disk under Output/<Name>_<ts>/ with the same sub-folder tree.
# =============================================================================

import os, json, random, logging
from flask import send_file
import zipfile
import tempfile
from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from models import db, DBSession, GazeRecord, InterviewEvent, PSSResult
from utils.questions import (get_questions, get_pss_options,
                             get_consent_text, get_ui_labels, PSS_REVERSED)
from utils.output_manager import OutputManager
from utils.media_convert import convert_to_mp4, convert_to_wav, ffmpeg_available

# ── [ADDED] Cloudinary imports ────────────────────────────────────────────────
import cloudinary
import cloudinary.uploader

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("samjna")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "samjna-dev-secret-change-in-prod")

# ── [ADDED] Cloudinary configuration (env vars) ───────────────────────────────
# Set these three environment variables before running the app:
#   CLOUDINARY_CLOUD_NAME  – your Cloudinary cloud name
#   CLOUDINARY_API_KEY     – your Cloudinary API key
#   CLOUDINARY_API_SECRET  – your Cloudinary API secret
_cld_cloud  = os.environ.get("CLOUDINARY_CLOUD_NAME")
_cld_key    = os.environ.get("CLOUDINARY_API_KEY")
_cld_secret = os.environ.get("CLOUDINARY_API_SECRET")

if _cld_cloud and _cld_key and _cld_secret:
    cloudinary.config(
        cloud_name = _cld_cloud,
        api_key    = _cld_key,
        api_secret = _cld_secret,
        secure     = True,          # always use https URLs
    )
    logger.info("Cloudinary configured for cloud: %s", _cld_cloud)
else:
    logger.warning(
        "Cloudinary env vars not fully set "
        "(CLOUDINARY_CLOUD_NAME / CLOUDINARY_API_KEY / CLOUDINARY_API_SECRET). "
        "Uploads will be skipped; local files will be kept."
    )

_CLOUDINARY_READY = bool(_cld_cloud and _cld_key and _cld_secret)

if not ffmpeg_available():
    logger.warning("FFmpeg was NOT found on PATH at startup. "
                   "MP4/WAV conversion will fail until ffmpeg is installed.")
else:
    logger.info("FFmpeg detected on PATH — MP4/WAV conversion is available.")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get("DATABASE_URL") or
    f"sqlite:///{os.path.join(BASE_DIR, 'samjna.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# =============================================================================
# [ADDED] Cloudinary upload helper
# =============================================================================

def upload_to_cloudinary(local_path: str, resource_type: str = "auto",
                          folder: str = "samjna") -> "str | None":
    """
    Upload *local_path* to Cloudinary and return the secure URL.

    Parameters
    ----------
    local_path    : absolute path of the file to upload
    resource_type : "video" for .mp4, "raw" for .wav / other audio
                    (Cloudinary treats audio as "video" for .mp4 but "raw"
                    for WAV; pass "auto" to let the SDK decide, or be
                    explicit to avoid mis-classification)
    folder        : Cloudinary folder/prefix for organisation

    Returns
    -------
    str  – secure_url on success
    None – on any failure (caller decides what to do)
    """
    if not _CLOUDINARY_READY:
        logger.warning("upload_to_cloudinary: Cloudinary not configured — skipping upload of %s",
                       local_path)
        return None

    if not os.path.isfile(local_path):
        logger.error("upload_to_cloudinary: local file not found: %s", local_path)
        return None

    try:
        public_id = os.path.splitext(os.path.basename(local_path))[0]
        result = cloudinary.uploader.upload(
            local_path,
            resource_type = resource_type,
            folder        = folder,
            public_id     = public_id,
            overwrite     = True,
            use_filename  = True,
        )
        secure_url = result.get("secure_url")
        if secure_url:
            logger.info("Cloudinary upload SUCCESS: %s → %s", local_path, secure_url)
            return secure_url
        else:
            logger.error("Cloudinary upload returned no URL for %s; result=%s",
                         local_path, result)
            return None

    except Exception as exc:   # never crash the caller
        logger.error("Cloudinary upload FAILED for %s: %s", local_path, exc, exc_info=True)
        return None


# ── helpers ───────────────────────────────────────────────────────────────────

def cur_sess() -> "DBSession | None":
    sid = session.get("session_id")
    return db.session.get(DBSession, sid) if sid else None

def is_fragment_request() -> bool:
    """True when the SPA shell's JS is fetching a step as an HTML fragment."""
    return request.headers.get("X-Requested-With") == "XMLHttpRequest" or \
           request.args.get("fragment") == "1"

def get_om() -> "OutputManager | None":
    """Reconstruct OutputManager from Flask session (stateless between requests)."""
    info = session.get("om_info")
    if not info:
        return None
    om = OutputManager(info["participant_name"], info["timestamp"])
    om._log = info.get("log", [])
    return om

def save_om(om: OutputManager):
    session["om_info"] = {
        "participant_name": om.participant_name,
        "timestamp":        om.timestamp,
        "log":              om._log,
    }

def require_session(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not cur_sess():
            return redirect(url_for("consent"))
        return f(*args, **kwargs)
    return wrapper

# ── phase constants ───────────────────────────────────────────────────────────

PHASES = [
    {"id": "baseline",         "q_secs": 60, "prep_secs": 0,  "q_count": 3},
    {"id": "social_stress",    "q_secs": 65, "prep_secs": 15, "q_count": 3},
    {"id": "cognitive_stress", "q_secs": 70, "prep_secs": 5,  "q_count": 3},
    {"id": "recovery",         "q_secs": 60, "prep_secs": 0,  "q_count": 2},
]

PHASE_LABELS = {
    "baseline":         {"english":"Phase 1 – Baseline Calibration",
                         "tamil":"கட்டம் 1 – அடிப்படை அளவீடு",
                         "kannada":"ಹಂತ 1 – ಆಧಾರ ಅಳತೆ"},
    "social_stress":    {"english":"Phase 2 – Social Evaluation",
                         "tamil":"கட்டம் 2 – சமூக மதிப்பீடு",
                         "kannada":"ಹಂತ 2 – ಸಾಮಾಜಿಕ ಮೌಲ್ಯಮಾಪನ"},
    "cognitive_stress": {"english":"Phase 3 – Cognitive Load",
                         "tamil":"கட்டம் 3 – அறிவாற்றல் சுமை",
                         "kannada":"ಹಂತ 3 – ಅರಿವಿನ ಹೊರೆ"},
    "recovery":         {"english":"Phase 4 – Recovery",
                         "tamil":"கட்டம் 4 – மீட்சி",
                         "kannada":"ಹಂತ 4 – ಚೇತರಿಕೆ"},
}

PHASE_COLORS = {
    "baseline":         {"bg":"#0D2030","fg":"#AADDFF","border":"#1C5070"},
    "social_stress":    {"bg":"#1A0D0D","fg":"#FFCCCC","border":"#600000"},
    "cognitive_stress": {"bg":"#0F0F0F","fg":"#FFFFFF", "border":"#444444"},
    "recovery":         {"bg":"#0C1F10","fg":"#AAFFCC","border":"#1A5030"},
}

PHASE_Q_OFFSET = {
    "baseline":0, "social_stress":3, "cognitive_stress":6, "recovery":9
}

def phase_questions(phase_id, lang):
    qs = get_questions(phase_id, lang)
    if phase_id == "social_stress":
        idx = session.get("ss_indices", list(range(3)))
        return [qs[i] for i in idx if i < len(qs)]
    if phase_id == "cognitive_stress":
        idx = session.get("cog_indices", list(range(3)))
        return [qs[i] for i in idx if i < len(qs)]
    cnt = next(p["q_count"] for p in PHASES if p["id"] == phase_id)
    return qs[:cnt]

# =============================================================================
# SCREEN 1 – CONSENT
# =============================================================================

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("consent"))

@app.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        name      = request.form.get("participant_name","").strip()
        lang      = request.form.get("language","english")
        consented = request.form.get("consent_check")
        if not name:
            flash("Please enter your full name.", "error")
            return redirect(url_for("consent", lang=lang))
        if not consented:
            flash("Please accept the consent statement.", "error")
            return redirect(url_for("consent", lang=lang))

        om = OutputManager(name)

        dbs = DBSession(participant_name=name, language=lang,
                        output_dir=om.output_dir, session_ts=om.timestamp)
        db.session.add(dbs)
        db.session.commit()

        om.log_event("session", "CONSENT_GIVEN", f"{name} | lang={lang}")
        om.save_session_log()
        save_om(om)

        social_qs = get_questions("social_stress", lang)
        cog_qs    = get_questions("cognitive_stress", lang)
        session["session_id"]  = dbs.id
        session["language"]    = lang
        session["ss_indices"]  = random.sample(range(len(social_qs)), min(3, len(social_qs)))
        session["cog_indices"] = random.sample(range(len(cog_qs)),    min(3, len(cog_qs)))
        session.permanent = True
        logger.info("Consent given: participant=%s lang=%s session_id=%s", name, lang, dbs.id)
        return redirect(url_for("assessment"))

    lang = request.args.get("lang","english")
    return render_template("consent.html", lang=lang,
                           consent_text=get_consent_text(lang),
                           labels=get_ui_labels(lang))

# =============================================================================
# ASSESSMENT SHELL
# =============================================================================

@app.route("/assessment")
@require_session
def assessment():
    lang = session.get("language", "english")
    return render_template("assessment_shell.html",
                           labels=get_ui_labels(lang),
                           first_step_url=url_for("face_calibration"))

# =============================================================================
# SCREEN 2 – FACE CALIBRATION
# =============================================================================

@app.route("/face-calibration", methods=["GET","POST"])
@require_session
def face_calibration():
    if request.method == "POST":
        om = get_om()
        om.log_event("session","FACE_CALIBRATION_DONE")
        om.save_session_log()
        save_om(om)
        logger.info("Face calibration complete for session_id=%s", session.get("session_id"))
        return jsonify({"status": "ok", "next_url": url_for("eye_calibration")})

    tpl = "fragments/face_calibration_fragment.html" if is_fragment_request() else "face_calibration.html"
    return render_template(tpl, labels=get_ui_labels(session.get("language","english")))

# =============================================================================
# SCREEN 3 – EYE CALIBRATION
# =============================================================================

@app.route("/eye-calibration")
@require_session
def eye_calibration():
    tpl = "fragments/eye_calibration_fragment.html" if is_fragment_request() else "eye_calibration.html"
    return render_template(tpl, labels=get_ui_labels(session.get("language","english")))

@app.route("/eye-calibration/save", methods=["POST"])
@require_session
def eye_calibration_save():
    data    = request.get_json(force=True)
    records = data.get("records", [])
    dbs     = cur_sess()
    om      = get_om()

    om.save_gaze_data(records)

    for r in records:
        db.session.add(GazeRecord(
            session_id=dbs.id,
            dot_index=r.get("dot_index"),
            target_x_px=r.get("target_x_px"), target_y_px=r.get("target_y_px"),
            click_x_px=r.get("click_x_px"),   click_y_px=r.get("click_y_px"),
            offset_px=r.get("offset_px"),      timestamp=r.get("timestamp"),
        ))

    om.log_event("session","EYE_CALIBRATION_DONE",f"{len(records)} dots")
    om.save_session_log()
    save_om(om)
    db.session.commit()
    logger.info("Eye calibration saved: %d gaze records for session_id=%s", len(records), dbs.id)
    return jsonify({"status":"ok", "next_url": url_for("interview", phase_id="baseline", q_idx=0)})

# =============================================================================
# SCREEN 4 – INTERVIEW
# =============================================================================

@app.route("/interview/<phase_id>/<int:q_idx>")
@require_session
def interview(phase_id, q_idx):
    lang      = session.get("language","english")
    labels    = get_ui_labels(lang)
    phase     = next((p for p in PHASES if p["id"]==phase_id), None)
    fragment  = is_fragment_request()

    if not phase:
        target = url_for("interview", phase_id="baseline", q_idx=0)
        return jsonify({"redirect": target}) if fragment else redirect(target)

    questions = phase_questions(phase_id, lang)

    if q_idx >= len(questions):
        om  = get_om()
        dbs = cur_sess()
        om.log_event(phase_id, "PHASE_END")
        phase_order = [p["id"] for p in PHASES]
        cidx = phase_order.index(phase_id)
        if cidx + 1 < len(phase_order):
            next_phase = phase_order[cidx + 1]
            om.save_session_log(); save_om(om)
            target = url_for("interview", phase_id=next_phase, q_idx=0)
        else:
            om.log_event("session","INTERVIEW_COMPLETE")
            om.save_session_log(); save_om(om)
            target = url_for("pss_test")
        return jsonify({"redirect": target}) if fragment else redirect(target)

    q_text      = questions[q_idx]
    global_q_no = PHASE_Q_OFFSET[phase_id] + q_idx + 1
    global_q_lbl = f"Q{q_idx+1}"
    colors      = PHASE_COLORS[phase_id]
    phase_label = PHASE_LABELS[phase_id].get(lang, PHASE_LABELS[phase_id]["english"])

    if q_idx == 0:
        om = get_om()
        om.log_event(phase_id,"PHASE_START"); om.save_session_log(); save_om(om)

    om          = get_om()
    video_fname = os.path.basename(om.video_path(phase_id, global_q_lbl, ext="mp4"))
    audio_fname = os.path.basename(om.audio_path(phase_id, global_q_lbl))

    tpl = "fragments/interview_fragment.html" if fragment else "interview.html"
    return render_template(tpl,
        phase_id=phase_id, phase_label=phase_label,
        q_idx=q_idx, q_text=q_text,
        global_q_no=global_q_no, total_qs=len(questions),
        q_secs=phase["q_secs"], prep_secs=phase["prep_secs"],
        colors=colors, labels=labels, lang=lang,
        video_fname=video_fname, audio_fname=audio_fname,
        upload_video_url=url_for("upload_video", phase_id=phase_id, q_idx=q_idx),
        upload_audio_url=url_for("upload_audio", phase_id=phase_id, q_idx=q_idx),
        log_url=url_for("interview_log", phase_id=phase_id, q_idx=q_idx),
        next_step_url=url_for("interview", phase_id=phase_id, q_idx=q_idx+1),
        prep_key = "prepare_cog" if phase_id == "cognitive_stress" else "prepare_social",
        is_cognitive = (phase_id == "cognitive_stress"),
    )

# ── File upload routes ────────────────────────────────────────────────────────
# [MODIFIED] upload_video – adds Cloudinary upload after successful local save

@app.route("/upload/video/<phase_id>/<int:q_idx>", methods=["POST"])
@require_session
def upload_video(phase_id, q_idx):
    om         = get_om()
    local_lbl  = f"Q{q_idx+1}"
    save_path  = om.video_path(phase_id, local_lbl, ext="mp4")
    data       = request.data
    logger.info("Video upload received: phase=%s q=%d size=%d bytes → target %s",
               phase_id, q_idx+1, len(data) if data else 0, save_path)

    # ── Step 1: existing local conversion (unchanged) ──────────────────────
    ok = False
    if data:
        ok = convert_to_mp4(data, save_path)

    if ok:
        logger.info("Video local save SUCCESS: %s", save_path)
    else:
        logger.error("Video local save FAILED: phase=%s q=%d target=%s",
                     phase_id, q_idx+1, save_path)

    # ── Step 2: [ADDED] Cloudinary upload ─────────────────────────────────
    cloudinary_url = None
    if ok:
        cloudinary_url = upload_to_cloudinary(
            save_path,
            resource_type="video",                    # mp4 is a video resource
            folder=f"samjna/{om.participant_name}",   # organise by participant
        )
        if cloudinary_url:
            # Delete local file only after confirmed cloud upload
            try:
                os.remove(save_path)
                logger.info("Local video deleted after Cloudinary upload: %s", save_path)
            except OSError as e:
                logger.warning("Could not delete local video %s: %s", save_path, e)
        else:
            # Upload failed — keep local file, log warning, do not crash
            logger.warning("Cloudinary video upload failed; local file retained: %s", save_path)

    # ── Step 3: log event ─────────────────────────────────────────────────
    om2 = get_om()
    if cloudinary_url:
        om2.log_event(phase_id, f"Q{q_idx+1}_VIDEO_SAVED", cloudinary_url)
    else:
        om2.log_event(phase_id, f"Q{q_idx+1}_VIDEO_{'SAVED' if ok else 'FAILED'}", save_path)
    om2.save_session_log(); save_om(om2)

    return jsonify({
        "status":        "ok" if ok else "error",
        "file":          os.path.basename(save_path),
        "cloudinary_url": cloudinary_url,   # None if not uploaded / not configured
    })


# [MODIFIED] upload_audio – adds Cloudinary upload after successful local save

@app.route("/upload/audio/<phase_id>/<int:q_idx>", methods=["POST"])
@require_session
def upload_audio(phase_id, q_idx):
    om           = get_om()
    local_lbl    = f"Q{q_idx+1}"
    save_path    = om.audio_path(phase_id, local_lbl)
    data         = request.data
    content_type = request.content_type or ""
    src_ext      = "wav" if "wav" in content_type else "webm"
    logger.info("Audio upload received: phase=%s q=%d size=%d bytes content_type=%s → target %s",
               phase_id, q_idx+1, len(data) if data else 0, content_type, save_path)

    # ── Step 1: existing local conversion (unchanged) ──────────────────────
    ok = False
    if data:
        ok = convert_to_wav(data, src_ext, save_path)

    if ok:
        logger.info("Audio local save SUCCESS: %s", save_path)
    else:
        logger.error("Audio local save FAILED: phase=%s q=%d target=%s",
                     phase_id, q_idx+1, save_path)

    # ── Step 2: [ADDED] Cloudinary upload ─────────────────────────────────
    cloudinary_url = None
    if ok:
        cloudinary_url = upload_to_cloudinary(
            save_path,
            resource_type="raw",                      # WAV must be "raw" on Cloudinary
            folder=f"samjna/{om.participant_name}",
        )
        if cloudinary_url:
            try:
                os.remove(save_path)
                logger.info("Local audio deleted after Cloudinary upload: %s", save_path)
            except OSError as e:
                logger.warning("Could not delete local audio %s: %s", save_path, e)
        else:
            logger.warning("Cloudinary audio upload failed; local file retained: %s", save_path)

    # ── Step 3: log event ─────────────────────────────────────────────────
    om2 = get_om()
    if cloudinary_url:
        om2.log_event(phase_id, f"Q{q_idx+1}_AUDIO_SAVED", cloudinary_url)
    else:
        om2.log_event(phase_id, f"Q{q_idx+1}_AUDIO_{'SAVED' if ok else 'FAILED'}", save_path)
    om2.save_session_log(); save_om(om2)

    return jsonify({
        "status":        "ok" if ok else "error",
        "file":          os.path.basename(save_path),
        "cloudinary_url": cloudinary_url,
    })


@app.route("/interview/<phase_id>/<int:q_idx>/log", methods=["POST"])
@require_session
def interview_log(phase_id, q_idx):
    data   = request.get_json(force=True)
    event  = data.get("event","Q_EVENT")
    detail = data.get("detail","")
    om     = get_om()
    dbs    = cur_sess()

    om.log_event(phase_id, event, detail)
    om.save_session_log()
    save_om(om)

    db.session.add(InterviewEvent(
        session_id=dbs.id, phase_id=phase_id, q_index=q_idx,
        global_q_no=PHASE_Q_OFFSET.get(phase_id,0)+q_idx+1,
        event_type=event, detail=detail,
    ))
    db.session.commit()
    return jsonify({"status":"ok"})

# =============================================================================
# SCREEN 5 – PSS TEST
# =============================================================================

@app.route("/pss", methods=["GET","POST"])
@require_session
def pss_test():
    lang   = session.get("language","english")
    labels = get_ui_labels(lang)
    fragment = is_fragment_request()

    if request.method == "POST":
        questions = get_questions("pss", lang)
        if request.is_json:
            payload = request.get_json(force=True)
            answers_in = payload.get("answers", {})
            def _get(i): return answers_in.get(str(i), answers_in.get(i))
        else:
            def _get(i): return request.form.get(f"q{i}")

        raw, errors = [], []
        for i in range(len(questions)):
            v = _get(i)
            if v is None: errors.append(i+1)
            else:         raw.append(int(v))
        if errors:
            msg = f"Please answer question(s): {', '.join(map(str,errors))}"
            if request.is_json:
                return jsonify({"status":"error", "message": msg}), 400
            flash(msg, "error")
            return redirect(url_for("pss_test"))

        scored = [4-v if i in PSS_REVERSED else v for i,v in enumerate(raw)]
        total  = sum(scored)
        if total <= 13:   interp = "Low perceived stress (score 0–13)"
        elif total <= 26: interp = "Moderate perceived stress (score 14–26)"
        else:             interp = "High perceived stress (score 27–40)"

        om  = get_om()
        dbs = cur_sess()

        om.save_pss_results(raw, total, interp)
        om.log_event("session","PSS_COMPLETE",f"Score={total} | {interp}")
        om.save_session_log()
        save_om(om)

        db.session.add(PSSResult(session_id=dbs.id,
                                 answers_json=json.dumps(raw),
                                 score=total, interpretation=interp))
        db.session.commit()
        logger.info("PSS complete: session_id=%s score=%d (%s)", dbs.id, total, interp)

        session["pss_score"]          = total
        session["pss_interpretation"] = interp
        session["output_dir"]         = om.output_dir

        if request.is_json:
            return jsonify({"status":"ok", "redirect": url_for("thank_you"),
                           "score": total, "interpretation": interp})
        return redirect(url_for("thank_you"))

    tpl = "fragments/pss_test_fragment.html" if fragment else "pss_test.html"
    return render_template(tpl,
                           questions=get_questions("pss",lang),
                           options=get_pss_options(lang),
                           labels=labels, lang=lang)

# =============================================================================
# SCREEN 6 – THANK YOU
# =============================================================================

@app.route("/thank-you")
@require_session
def thank_you():
    lang   = session.get("language","english")
    labels = get_ui_labels(lang)
    score  = session.get("pss_score","—")
    interp = session.get("pss_interpretation","")
    odir   = session.get("output_dir","")
    dbs    = cur_sess()
    name   = dbs.participant_name if dbs else ""
    fragment = is_fragment_request()
    session.clear()
    tpl = "fragments/thank_you_fragment.html" if fragment else "thank_you.html"
    return render_template(tpl,
                           pss_score=score, interpretation=interp,
                           participant=name, output_dir=odir, labels=labels)

# =============================================================================
# ADMIN
# =============================================================================

@app.route("/admin")
def admin():
    sessions = DBSession.query.order_by(DBSession.created_at.desc()).all()
    return render_template("admin.html", sessions=sessions)

@app.route("/admin/session/<int:session_id>")
def admin_session(session_id):
    dbs    = db.session.get(DBSession, session_id)
    gaze   = GazeRecord.query.filter_by(session_id=session_id).all()
    events = InterviewEvent.query.filter_by(session_id=session_id).all()
    pss    = PSSResult.query.filter_by(session_id=session_id).first()
    return render_template("admin_session.html",
                           sess=dbs, gaze=gaze, events=events, pss=pss)

# =============================================================================
@app.route('/download-all-data')
def download_all_data():
    output_folder = os.path.join(BASE_DIR, "Output")

    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    temp_zip.close()

    with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, output_folder)
                zipf.write(filepath, arcname)

    return send_file(
        temp_zip.name,
        as_attachment=True,
        download_name="samjna_output.zip"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)