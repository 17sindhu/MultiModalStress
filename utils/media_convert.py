# =============================================================================
# media_convert.py
# Converts browser-recorded WebM blobs to MP4 (video) / WAV (audio) using
# FFmpeg. All conversions are logged (success + failure + stderr) per the
# validation/logging requirements.
# =============================================================================

import os
import subprocess
import tempfile
import shutil
import logging

logger = logging.getLogger("samjna")

FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def convert_to_mp4(webm_bytes: bytes, mp4_path: str) -> bool:
    """Convert raw WebM video bytes to a proper .mp4 (H.264/AAC) file at mp4_path."""
    if not webm_bytes:
        logger.error("convert_to_mp4: received empty byte payload — nothing to write (%s)", mp4_path)
        return False
    if not ffmpeg_available():
        logger.error("convert_to_mp4: ffmpeg binary not found on PATH — cannot produce %s", mp4_path)
        return False

    os.makedirs(os.path.dirname(mp4_path), exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(webm_bytes)
        tmp_path = tmp.name

    try:
        logger.info("FFmpeg video conversion starting: %s (%d bytes) → %s "
                   "(video-only output — audio track explicitly stripped with -an)",
                   tmp_path, len(webm_bytes), mp4_path)
        result = subprocess.run(
            [FFMPEG_BIN, "-y", "-i", tmp_path,
             "-c:v", "libx264", "-preset", "fast", "-crf", "23",
             "-an",                        # strip any audio track — MP4 must be video-only
             "-movflags", "+faststart",
             mp4_path],
            capture_output=True, timeout=180,
        )
        if result.returncode != 0:
            logger.error("FFmpeg video conversion FAILED (exit %d) for %s\nstderr: %s",
                         result.returncode, mp4_path,
                         result.stderr.decode(errors="replace")[-2000:])
            return False
        if not os.path.exists(mp4_path) or os.path.getsize(mp4_path) == 0:
            logger.error("FFmpeg reported success but output file missing/empty: %s", mp4_path)
            return False
        logger.info("FFmpeg video conversion SUCCESS: %s (%d bytes)",
                    mp4_path, os.path.getsize(mp4_path))
        return True
    except subprocess.TimeoutExpired:
        logger.error("FFmpeg video conversion TIMED OUT for %s", mp4_path)
        return False
    except Exception as e:
        logger.error("FFmpeg video conversion EXCEPTION for %s: %s", mp4_path, e)
        return False
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def convert_to_wav(audio_bytes: bytes, src_ext: str, wav_path: str) -> bool:
    """Convert raw browser audio bytes (webm/opus or wav container) to clean PCM .wav."""
    if not audio_bytes:
        logger.error("convert_to_wav: received empty byte payload — nothing to write (%s)", wav_path)
        return False
    if not ffmpeg_available():
        logger.error("convert_to_wav: ffmpeg binary not found on PATH — cannot produce %s", wav_path)
        return False

    os.makedirs(os.path.dirname(wav_path), exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=f".{src_ext}", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        logger.info("FFmpeg audio conversion starting: %s (%d bytes) → %s",
                    tmp_path, len(audio_bytes), wav_path)
        result = subprocess.run(
            [FFMPEG_BIN, "-y", "-i", tmp_path,
             "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le",
             wav_path],
            capture_output=True, timeout=60,
        )
        if result.returncode != 0:
            logger.error("FFmpeg audio conversion FAILED (exit %d) for %s\nstderr: %s",
                         result.returncode, wav_path,
                         result.stderr.decode(errors="replace")[-2000:])
            return False
        if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
            logger.error("FFmpeg reported success but output file missing/empty: %s", wav_path)
            return False
        logger.info("FFmpeg audio conversion SUCCESS: %s (%d bytes)",
                    wav_path, os.path.getsize(wav_path))
        return True
    except subprocess.TimeoutExpired:
        logger.error("FFmpeg audio conversion TIMED OUT for %s", wav_path)
        return False
    except Exception as e:
        logger.error("FFmpeg audio conversion EXCEPTION for %s: %s", wav_path, e)
        return False
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
