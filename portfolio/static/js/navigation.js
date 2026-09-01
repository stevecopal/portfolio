// Navigation: hamburger menu, navbar scroll behavior, back-to-top
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initMobileMenu();
        initNavbarScroll();
        initBackToTop();
        initActiveNavLinks();
    });

    // ── Mobile Menu ──────────────────────────────────────────
    function initMobileMenu() {
        var hamburger = document.getElementById('hamburgerBtn');
        var closeBtn = document.getElementById('mobileCloseBtn');
        var mobileMenu = document.getElementById('mobileMenu');
        var overlay = document.getElementById('mobileOverlay');
        
        if (!hamburger || !mobileMenu || !overlay) return;
        
        function openMenu() {
            hamburger.classList.add('active');
            mobileMenu.classList.add('open');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function closeMenu() {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('open');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
        
        // Hamburger toggle
        hamburger.addEventListener('click', function() {
            if (mobileMenu.classList.contains('open')) {
                closeMenu();
            } else {
                openMenu();
            }
        });
        
        // Close button inside mobile menu
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                closeMenu();
            });
        }
        
        // Overlay click
        overlay.addEventListener('click', function() {
            closeMenu();
        });
        
        // Close on link click
        mobileMenu.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                closeMenu();
            });
        });
        
        // Close on Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
                closeMenu();
            }
        });
    }

    // ── Navbar Scroll ─────────────────────────────────────────
    function initNavbarScroll() {
        var navbar = document.getElementById('navbar');
        if (!navbar) return;
        
        var lastScrollY = window.scrollY;
        var scrollThreshold = 80;
        
        window.addEventListener('scroll', function() {
            var currentScrollY = window.scrollY;
            
            // Prevent negative scroll (iOS bounce)
            if (currentScrollY < 0) return;
            
            // Add shadow when scrolled
            if (currentScrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            // Hide on scroll down, show on scroll up
            if (currentScrollY > lastScrollY && currentScrollY > scrollThreshold) {
                navbar.classList.add('-translate-y-full');
            } else {
                navbar.classList.remove('-translate-y-full');
            }
            
            lastScrollY = currentScrollY;
        });
    }

    // ── Back to Top ──────────────────────────────────────────
    function initBackToTop() {
        var btn = document.getElementById('backToTop');
        if (!btn) return;
        
        window.addEventListener('scroll', function() {
            if (window.scrollY > 400) {
                btn.style.opacity = '1';
                btn.style.pointerEvents = 'auto';
            } else {
                btn.style.opacity = '0';
                btn.style.pointerEvents = 'none';
            }
        });
        
        btn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── Active Nav Links ─────────────────────────────────────
    function initActiveNavLinks() {
        var currentPath = window.location.pathname;
        var navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(function(link) {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

})();
