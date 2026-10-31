(() => {
  const root = document.documentElement;
  root.classList.add('sc-ready');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = value => Math.min(1, Math.max(0, value));

  const bar = document.createElement('div');
  bar.className = 'scroll-progress';
  bar.setAttribute('aria-hidden', 'true');
  bar.innerHTML = '<span></span>';
  document.body.append(bar);

  const hero = document.querySelector('.landing-hero');
  let queued = false;
  const update = () => {
    queued = false;
    const max = root.scrollHeight - window.innerHeight;
    bar.style.setProperty('--page-p', (max > 0 ? clamp(window.scrollY / max) : 0).toFixed(4));
    if (hero && !reduce) hero.style.setProperty('--hero-p', clamp(window.scrollY / Math.max(hero.offsetHeight, 1)).toFixed(4));
  };
  const queue = () => { if (!queued) { queued = true; window.requestAnimationFrame(update); } };
  window.addEventListener('scroll', queue, { passive: true });
  window.addEventListener('resize', queue);
  update();

  const items = [...document.querySelectorAll('.view-rise')];
  if (!items.length) return;
  if (reduce || !('IntersectionObserver' in window)) { items.forEach(item => item.classList.add('is-visible')); return; }
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  }), { threshold: 0.1, rootMargin: '0px 0px -4% 0px' });
  items.forEach(item => observer.observe(item));
})();
