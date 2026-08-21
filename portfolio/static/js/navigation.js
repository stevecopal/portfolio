let lastScrollY = window.scrollY;
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;

    // Empêche le déclenchement au rebond sur mobile (scroll négatif)
    if (currentScrollY < 0) return;

    // Masque si on descend, affiche si on monte ou tout en haut
    if (currentScrollY > lastScrollY && currentScrollY > 80) {
        // Scroll vers le bas -> Masquer
        navbar.classList.add('-translate-y-full');
    } else {
        // Scroll vers le haut -> Afficher
        navbar.classList.remove('-translate-y-full');
    }

    lastScrollY = currentScrollY;
});