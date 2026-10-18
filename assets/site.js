// Keep every page and download link functional without JavaScript.
(() => {
  const languageMenu = document.querySelector('.languages');
  if (!languageMenu) return;
  document.addEventListener('click', event => {
    if (!languageMenu.contains(event.target)) languageMenu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && languageMenu.open) {
      languageMenu.open = false;
      languageMenu.querySelector('summary').focus();
    }
  });
})();
