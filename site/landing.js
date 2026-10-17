if (document.body.classList.contains('landing-page')) {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const nav = document.querySelector('.landing-nav');
  const reveal = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) reveal.forEach(element => element.classList.add('is-visible'));
  else {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), { threshold: 0.12 });
    reveal.forEach(element => observer.observe(element));
  }
  const updateNav = () => nav.classList.toggle('is-scrolled', window.scrollY > 24);
  updateNav(); window.addEventListener('scroll', updateNav, { passive: true });
}
