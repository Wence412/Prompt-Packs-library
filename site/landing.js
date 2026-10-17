if (document.body.classList.contains('landing-page')) {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const nav = document.querySelector('.landing-nav');
  const reveal = document.querySelectorAll('.reveal');
  const themeToggle = document.querySelector('#theme-toggle');
  if (reduceMotion || !('IntersectionObserver' in window)) reveal.forEach(element => element.classList.add('is-visible'));
  else {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), { threshold: 0.12 });
    reveal.forEach(element => observer.observe(element));
  }
  const updateNav = () => nav.classList.toggle('is-scrolled', window.scrollY > 24);
  updateNav(); window.addEventListener('scroll', updateNav, { passive: true });
  if (themeToggle) {
    const setTheme = theme => {
      document.body.dataset.theme = theme;
      const isLight = theme === 'light';
      themeToggle.textContent = isLight ? 'Use dark theme' : 'Use light theme';
      themeToggle.setAttribute('aria-pressed', String(isLight));
      localStorage.setItem('prompt-packs-theme', theme);
    };
    try { setTheme(localStorage.getItem('prompt-packs-theme') || 'dark'); } catch { setTheme('dark'); }
    themeToggle.addEventListener('click', () => setTheme(document.body.dataset.theme === 'light' ? 'dark' : 'light'));
  }
}
