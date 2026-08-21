// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initThemeToggle();
    initBackToTop();
    initAnimations();
    initProjectFilters();
    initCounters();
    initTypingEffect();
    initNavbarScroll();
});

// Mobile Menu Toggle
function initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// Back to Top Button
function initBackToTop() {
    const backToTopButton = document.getElementById('backToTop');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.remove('opacity-0');
            } else {
                backToTopButton.classList.add('opacity-0');
            }
        });
        
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

// Navbar Scroll Effect & Auto-Hide
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    
    // Sécurité si la navbar n'existe pas sur la page
    if (!navbar) return;

    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY;

        // 1. Réduction du padding et ajout d'ombre au scroll
        if (currentScrollY > 50) {
            navbar.classList.add('py-2', 'shadow-sm');
            navbar.classList.remove('py-4');
        } else {
            navbar.classList.remove('py-2', 'shadow-sm');
            navbar.classList.add('py-4');
        }

        // 2. Masquer au scroll vers le bas / Afficher au scroll vers le haut
        if (currentScrollY < 0) return; // Empêche l'effet de rebond iOS

        if (currentScrollY > lastScrollY && currentScrollY > 80) {
            // Scroll vers le bas -> Masquer
            navbar.classList.add('-translate-y-full');
        } else {
            // Scroll vers le haut -> Afficher
            navbar.classList.remove('-translate-y-full');
        }

        lastScrollY = currentScrollY;
    });
}

// Navbar Scroll Effect & Auto-Hide
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    
    // Sécurité si la navbar n'existe pas sur la page
    if (!navbar) return;

    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY;

        // 1. Réduction du padding et ajout d'ombre au scroll
        if (currentScrollY > 50) {
            navbar.classList.add('py-2', 'shadow-sm');
            navbar.classList.remove('py-4');
        } else {
            navbar.classList.remove('py-2', 'shadow-sm');
            navbar.classList.add('py-4');
        }

        // 2. Masquer au scroll vers le bas / Afficher au scroll vers le haut
        if (currentScrollY < 0) return; // Empêche l'effet de rebond iOS

        if (currentScrollY > lastScrollY && currentScrollY > 80) {
            // Scroll vers le bas -> Masquer
            navbar.classList.add('-translate-y-full');
        } else {
            // Scroll vers le haut -> Afficher
            navbar.classList.remove('-translate-y-full');
        }

        lastScrollY = currentScrollY;
    });
}