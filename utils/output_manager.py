# =============================================================================
# output_manager.py  – Flask version (identical file/folder naming to Tkinter)
#
# Folder:  Output/<SafeName>_<YYYYMMDD_HHMMSS>/
# Sub-folders: baseline/ social_stress/ cognitive_stress/ recovery/ pss/
#
# Video : <phase>/<name>_<global_q>_<ts>.webm   (browser MediaRecorder)
# Audio : <phase>/<name>_<global_q>_<ts>.wav    (browser MediaRecorder)
# Gaze  : eye_gaze_calibration.csv
# PSS   : pss/pss_scores.csv
# Log   : session_log.json
# =============================================================================

import os
import csv
import json
import logging
from datetime import datetime

logger = logging.getLogger("samjna")

PHASE_Q_OFFSET = {
    "baseline":         0,   # q1, q2, q3
    "social_stress":    3,   # q4, q5, q6
    "cognitive_stress": 6,   # q7, q8, q9
    "recovery":         9,   # q10, q11
}

# Where output folders are written on the server / local machine.
# On Railway, set OUTPUT_BASE_DIR to a mounted Volume path (e.g. /data/Output)
# so files survive redeploys/restarts — without it, the filesystem is ephemeral.
BASE_OUTPUT = os.environ.get(
    "OUTPUT_BASE_DIR",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Output")
)


class OutputManager:
    def __init__(self, participant_name: str, timestamp: str = None):
        safe_name = "".join(c if c.isalnum() else "_" for c in participant_name).strip("_")
        ts        = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        folder    = f"{safe_name}_{ts}"

        self.output_dir       = os.path.join(BASE_OUTPUT, folder)
        self.safe_name        = safe_name
        self.participant_name = participant_name
        self.timestamp        = ts
        self._log             = []

        already_existed = os.path.isdir(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        for sub in ("baseline", "social_stress", "cognitive_stress", "recovery", "pss"):
            os.makedirs(os.path.join(self.output_dir, sub), exist_ok=True)
        if not already_existed:
            logger.info("Output folder structure created: %s", self.output_dir)

    # ── Path helpers (identical logic to Tkinter version) ─────────────────────

    def _global_q_label(self, phase: str, local_label: str) -> str:
        offset = PHASE_Q_OFFSET.get(phase, 0)
        try:
            local_num = int(local_label.lstrip("Qq"))
        except ValueError:
            local_num = 1
        return f"q{offset + local_num}"

    def video_path(self, phase: str, label: str = "", ext: str = "mp4") -> str:
        """<phase>/<name>_<global_q>_<ts>.mp4"""
        gq       = self._global_q_label(phase, label) if label else "q0"
        filename = f"{self.safe_name}_{gq}_{self.timestamp}.{ext}"
        return os.path.join(self.output_dir, phase, filename)

    def audio_path(self, phase: str, label: str = "") -> str:
        """<phase>/<name>_<global_q>_<ts>.wav"""
        gq       = self._global_q_label(phase, label) if label else "q0"
        filename = f"{self.safe_name}_{gq}_{self.timestamp}.wav"
        return os.path.join(self.output_dir, phase, filename)

    def gaze_csv_path(self) -> str:
        return os.path.join(self.output_dir, "eye_gaze_calibration.csv")

    def pss_csv_path(self) -> str:
        return os.path.join(self.output_dir, "pss", "pss_scores.csv")

    def session_log_path(self) -> str:
        return os.path.join(self.output_dir, "session_log.json")

    # ── Writers ───────────────────────────────────────────────────────────────

    GAZE_FIELDNAMES = ["dot_index", "target_x_px", "target_y_px",
                      "click_x_px", "click_y_px", "offset_px", "timestamp"]

    def save_gaze_data(self, gaze_records: list):
        if not gaze_records:
            logger.warning("save_gaze_data called with 0 records — eye_gaze_calibration.csv not written")
            return
        with open(self.gaze_csv_path(), "w", newline="", encoding="utf-8") as f:
            # Explicit column order matches the original Tkinter app exactly
            # (dict insertion order is not guaranteed to survive a JSON
            # round-trip from the browser, so we pin it here rather than
            # relying on gaze_records[0].keys()).
            writer = csv.DictWriter(f, fieldnames=self.GAZE_FIELDNAMES, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(gaze_records)
        logger.info("Saved %d gaze records → %s", len(gaze_records), self.gaze_csv_path())

    def save_pss_results(self, answers: list, score: int, interpretation: str):
        with open(self.pss_csv_path(), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Question_No", "Answer_Value"])
            for i, val in enumerate(answers, 1):
                w.writerow([i, val])
            w.writerow([])
            w.writerow(["Total_PSS_Score", score])
            w.writerow(["Interpretation", interpretation])
            w.writerow([])
            w.writerow(["participant_name", "pss_score"])
            w.writerow([self.participant_name, score])
        logger.info("Saved PSS results (score=%s) → %s", score, self.pss_csv_path())

    def log_event(self, phase: str, event: str, detail: str = ""):
        self._log.append({
            "time":   datetime.now().isoformat(timespec="seconds"),
            "phase":  phase,
            "event":  event,
            "detail": detail,
        })
        logger.debug("EVENT [%s] %s — %s", phase, event, detail)

    def save_session_log(self):
        with open(self.session_log_path(), "w", encoding="utf-8") as f:
            json.dump({
                "participant":   self.participant_name,
                "session_start": self.timestamp,
                "events":        self._log,
            }, f, indent=2)
