// =============================================================================
// assessment_shell.js
//
// Owns ONE MediaStream for the entire assessment, acquired exactly once
// (during the Face Calibration step) and reused for Eye Calibration and
// every Interview question. This mirrors the Tkinter app's CameraManager
// singleton: cv2.VideoCapture(0) is opened once at startup and stays open
// until the whole session ends — no screen ever re-opens the camera.
//
// Navigation between steps happens via fetch() + DOM swap (no full page
// reload), which is what makes a single MediaStream survive across steps.
// =============================================================================

window.Samjna = (function () {
  let mediaStream   = null;   // the ONE persistent camera+mic stream
  let streamFailed  = false;  // true if user denied / device unavailable
  let currentStepUrl = null;

  const stepContainer   = () => document.getElementById("step-container");
  const camBar          = () => document.getElementById("global-camera-bar");
  const camPreview       = () => document.getElementById("global-cam-preview");
  const camStatus        = () => document.getElementById("global-cam-status");

  function log(...args) { console.log("[Samjna]", ...args); }
  function warn(...args) { console.warn("[Samjna]", ...args); }

  // ── Camera/mic acquisition (called ONCE, from Face Calibration) ───────────
  async function acquireMediaOnce() {
    if (mediaStream) {
      log("Reusing existing MediaStream (already acquired) — not calling getUserMedia again.");
      return mediaStream;
    }
    if (streamFailed) {
      log("Previous getUserMedia attempt failed; retrying on explicit request.");
    }
    try {
      log("Requesting camera + microphone access (getUserMedia) — this should happen ONCE per session.");
      mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      streamFailed = false;
      log("Camera/microphone acquired successfully. Tracks:",
          mediaStream.getTracks().map(t => `${t.kind}:${t.label}`));

      camBar().style.display = "block";
      camPreview().srcObject = mediaStream;
      camStatus().textContent = "● Live";
      camStatus().style.color = "#50DDAA";

      // If the user revokes permission or unplugs the device mid-session,
      // detect it so we can show a clear status instead of silently
      // recording nothing.
      mediaStream.getTracks().forEach(track => {
        track.addEventListener("ended", () => {
          warn(`Media track ended unexpectedly: ${track.kind}`);
          camStatus().textContent = "⚠ Camera/mic disconnected";
          camStatus().style.color = "#FFDD44";
          notifyStreamLost();
        });
      });

      return mediaStream;
    } catch (err) {
      streamFailed = true;
      warn("getUserMedia failed:", err.name, err.message);
      camBar().style.display = "block";
      camStatus().textContent = "⚠ Camera/mic not available — responses will not be recorded.";
      camStatus().style.color = "#FF6666";
      return null;
    }
  }

  function getStream() {
    return mediaStream;
  }

  function isStreamHealthy() {
    if (!mediaStream) return false;
    return mediaStream.getTracks().some(t => t.readyState === "live");
  }

  // ── Reconnect gracefully if the stream is lost mid-session ────────────────
  let reconnectAttempted = false;
  async function notifyStreamLost() {
    if (reconnectAttempted) return;
    reconnectAttempted = true;
    log("Attempting to reconnect camera/microphone after stream loss…");
    mediaStream = null;
    const newStream = await acquireMediaOnce();
    reconnectAttempted = false;
    if (newStream) {
      log("Reconnected successfully.");
      document.dispatchEvent(new CustomEvent("samjna:stream-reconnected", { detail: { stream: newStream } }));
    } else {
      warn("Reconnect attempt failed.");
    }
  }

  // ── Fragment loading / navigation (no full page reload) ───────────────────
  async function loadStep(url, { method = "GET", body = null } = {}) {
    log("Loading step fragment:", url);
    currentStepUrl = url;
    const opts = {
      method,
      headers: { "X-Requested-With": "XMLHttpRequest" },
    };
    if (body) {
      opts.headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(body);
    }
    const resp = await fetch(url, opts);
    if (!resp.ok) {
      warn("Step fragment request failed:", url, resp.status);
      stepContainer().innerHTML =
        `<div class="card"><div class="card-title">Something went wrong</div>
         <p style="color:var(--text-dim)">Could not load the next step (HTTP ${resp.status}). Please refresh.</p></div>`;
      return;
    }
    const contentType = resp.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const data = await resp.json();
      if (data.redirect) {
        await loadStep(data.redirect);
      }
      return;
    }
    const html = await resp.text();
    stepContainer().innerHTML = html;
    // Execute any <script> tags in the injected fragment (innerHTML does not run them)
    Array.from(stepContainer().querySelectorAll("script")).forEach(oldScript => {
      const newScript = document.createElement("script");
      Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
      newScript.textContent = oldScript.textContent;
      oldScript.parentNode.replaceChild(newScript, oldScript);
    });
  }

  async function goTo(url) {
    await loadStep(url);
  }

  async function postJSON(url, payload) {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest" },
      body: JSON.stringify(payload || {}),
    });
    return resp.json();
  }

  function init() {
    const first = window.SAMJNA_FIRST_STEP_URL;
    if (first) loadStep(first);
  }

  return {
    init, goTo, loadStep, postJSON,
    acquireMediaOnce, getStream, isStreamHealthy, log, warn,
  };
})();

window.addEventListener("DOMContentLoaded", () => window.Samjna.init());
