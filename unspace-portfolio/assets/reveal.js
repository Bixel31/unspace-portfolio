// ---- Scroll reveal ----
(function () {
  const els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || !els.length) {
    els.forEach(e => e.classList.add('in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    els.forEach(e => io.observe(e));
  }
})();

// ---- Mobile nav toggle ----
(function () {
  const btn = document.getElementById('navToggle');
  const nav = document.getElementById('nav');
  if (!btn || !nav) return;
  const close = () => { nav.classList.remove('open'); btn.classList.remove('active');
    btn.setAttribute('aria-expanded', 'false'); document.body.classList.remove('nav-lock'); };
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.classList.toggle('active', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('nav-lock', open);
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  window.addEventListener('resize', () => { if (window.innerWidth > 760) close(); });
})();

// ---- Contact form ----
(function () {
  const form = document.getElementById('contactForm');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = form.querySelector('input[type=email]');
    const msg = form.querySelector('textarea');
    const note = form.querySelector('.form-note');
    const ok = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value) && msg.value.trim().length > 1;
    if (!ok) {
      note.textContent = 'Please enter a valid email and a short message.';
      note.className = 'form-note err';
      return;
    }
    form.querySelector('button').textContent = 'Sent';
    note.textContent = 'Thank you — we will be in touch shortly.';
    note.className = 'form-note ok';
    form.querySelector('input').value = '';
    form.querySelector('textarea').value = '';
  });
})();
