from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DBSession(db.Model):
    __tablename__ = "sessions"
    id               = db.Column(db.Integer, primary_key=True)
    participant_name = db.Column(db.String(200), nullable=False)
    language         = db.Column(db.String(20),  default="english")
    output_dir       = db.Column(db.String(500),  default="")
    session_ts       = db.Column(db.String(20),   default="")
    created_at       = db.Column(db.DateTime,     default=datetime.utcnow)

    gaze_records     = db.relationship("GazeRecord",     back_populates="session", cascade="all,delete-orphan")
    interview_events = db.relationship("InterviewEvent", back_populates="session", cascade="all,delete-orphan")
    pss_result       = db.relationship("PSSResult",      back_populates="session", uselist=False, cascade="all,delete-orphan")

class GazeRecord(db.Model):
    __tablename__ = "gaze_records"
    id          = db.Column(db.Integer, primary_key=True)
    session_id  = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    dot_index   = db.Column(db.Integer)
    target_x_px = db.Column(db.Float)
    target_y_px = db.Column(db.Float)
    click_x_px  = db.Column(db.Float)
    click_y_px  = db.Column(db.Float)
    offset_px   = db.Column(db.Float)
    timestamp   = db.Column(db.String(30))
    session     = db.relationship("DBSession", back_populates="gaze_records")

class InterviewEvent(db.Model):
    __tablename__ = "interview_events"
    id          = db.Column(db.Integer, primary_key=True)
    session_id  = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    phase_id    = db.Column(db.String(30))
    q_index     = db.Column(db.Integer)
    global_q_no = db.Column(db.Integer)
    event_type  = db.Column(db.String(50))
    detail      = db.Column(db.Text, default="")
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    session     = db.relationship("DBSession", back_populates="interview_events")

class PSSResult(db.Model):
    __tablename__ = "pss_results"
    id             = db.Column(db.Integer, primary_key=True)
    session_id     = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    answers_json   = db.Column(db.Text)
    score          = db.Column(db.Integer)
    interpretation = db.Column(db.String(100))
    recorded_at    = db.Column(db.DateTime, default=datetime.utcnow)
    session        = db.relationship("DBSession", back_populates="pss_result")
