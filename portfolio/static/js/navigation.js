(function() {
    'use strict';

    // Expose for re-init after dynamic DOM changes (e.g. language switch)
    window.initMobileMenu = initMobileMenu;
    window.initSmoothScroll = initSmoothScroll;
    window.initActiveNavLinks = initActiveNavLinks;

    document.addEventListener('DOMContentLoaded', function() {
        initMobileMenu();
        initNavbarScroll();
        initBackToTop();
        initSmoothScroll();
        initActiveNavLinks();
        initScrollSpy();
    });

    function initMobileMenu() {
        var hamburger = document.getElementById('hamburgerBtn');
        var closeBtn = document.getElementById('mobileCloseBtn');
        var mobileMenu = document.getElementById('mobileMenu');
        var overlay = document.getElementById('mobileOverlay');
        if (!hamburger || !mobileMenu || !overlay) return;
        function openMenu() { hamburger.classList.add('active'); mobileMenu.classList.add('open'); overlay.classList.add('active'); document.body.style.overflow = 'hidden'; }
        function closeMenu() { hamburger.classList.remove('active'); mobileMenu.classList.remove('open'); overlay.classList.remove('active'); document.body.style.overflow = ''; }
        hamburger.addEventListener('click', function() { mobileMenu.classList.contains('open') ? closeMenu() : openMenu(); });
        if (closeBtn) closeBtn.addEventListener('click', closeMenu);
        overlay.addEventListener('click', closeMenu);
        mobileMenu.querySelectorAll('a').forEach(function(link) { link.addEventListener('click', closeMenu); });
        document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && mobileMenu.classList.contains('open')) closeMenu(); });
    }

    function initNavbarScroll() {
        var navbar = document.getElementById('navbar');
        if (!navbar) return;
        var lastScrollY = window.scrollY;
        window.addEventListener('scroll', function() {
            var y = window.scrollY;
            if (y < 0) return;
            navbar.classList.toggle('scrolled', y > 20);
            if (y > lastScrollY && y > 80) navbar.classList.add('-translate-y-full');
            else navbar.classList.remove('-translate-y-full');
            lastScrollY = y;
        });
    }

    function initBackToTop() {
        var btn = document.getElementById('backToTop');
        if (!btn) return;
        window.addEventListener('scroll', function() {
            btn.style.opacity = window.scrollY > 400 ? '1' : '0';
            btn.style.pointerEvents = window.scrollY > 400 ? 'auto' : 'none';
        });
        btn.addEventListener('click', function() { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    }

    function getHeaderHeight() {
        var navbar = document.getElementById('navbar');
        return navbar ? navbar.offsetHeight : 64;
    }

    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(link) {
            link.addEventListener('click', function(e) {
                var id = this.getAttribute('href');
                if (!id || id === '#') return;
                var target = document.querySelector(id);
                if (!target) return;
                e.preventDefault();
                var offset = target.getBoundingClientRect().top + window.scrollY - getHeaderHeight() - 16;
                window.scrollTo({ top: offset, behavior: 'smooth' });
                if (history.pushState) history.pushState(null, null, id);
            });
        });
    }

    function initActiveNavLinks() {
        var currentPath = window.location.pathname;
        document.querySelectorAll('.nav-link').forEach(function(link) {
            var href = link.getAttribute('href');
            if (href && currentPath === href) link.classList.add('active');
        });
    }

    function initScrollSpy() {
        var currentPath = window.location.pathname;
        if (currentPath !== '/' && currentPath.indexOf('/en') !== 0 && currentPath.indexOf('/fr') !== 0) return;
        var sections = document.querySelectorAll('section[id]');
        if (!sections.length) return;
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var id = entry.target.getAttribute('id');
                    document.querySelectorAll('.nav-link').forEach(function(l) { l.classList.remove('active'); });
                    if (id === 'hero' || id === 'about') {
                        var homeLink = document.querySelector('.nav-link[href*="home"]');
                        if (homeLink) homeLink.classList.add('active');
                    }
                }
            });
        }, { threshold: 0.3, rootMargin: '-80px 0px -40% 0px' });
        sections.forEach(function(s) { observer.observe(s); });
    }
})();
