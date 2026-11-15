// Scroll reveal
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// Certificate lightbox
const box = document.getElementById('lightbox');
const boxImg = box.querySelector('img');
document.querySelectorAll('.cert-img[data-full]').forEach((b) => {
  b.addEventListener('click', () => { boxImg.src = b.dataset.full; box.hidden = false; });
});
box.addEventListener('click', () => { box.hidden = true; });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') box.hidden = true; });

// Contact form -> Flask /contact
const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  form.querySelectorAll('.err').forEach((s) => (s.textContent = ''));
  status.textContent = 'Sending…'; status.className = '';
  try {
    const res = await fetch('/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    const data = await res.json();
    if (data.ok) {
      status.textContent = data.message; status.className = 'ok'; form.reset();
    } else {
      Object.entries(data.errors || {}).forEach(([k, v]) => {
        const el = form.querySelector(`.err[data-for="${k}"]`); if (el) el.textContent = v;
      });
      status.textContent = 'Please fix the highlighted fields.'; status.className = 'bad';
    }
  } catch {
    status.textContent = 'Something went wrong. Please try again.'; status.className = 'bad';
  }
});
