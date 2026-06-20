// main.js – shared JS for Samjna Flask app

// Auto-hide flash messages after 5 s
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => { el.style.transition = 'opacity .5s'; el.style.opacity = '0'; }, 5000);
});
