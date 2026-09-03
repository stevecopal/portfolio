(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initScrollReveal();
        initCounters();
        initReducedMotion();
    });

    // ── Scroll Reveal ────────────────────────────────────────
    function initScrollReveal() {
        var revealElements = document.querySelectorAll('.reveal');
        if (!revealElements.length) return;
        
        // Check for reduced motion preference
        var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) {
            revealElements.forEach(function(el) { el.classList.add('revealed'); });
            return;
        }
        
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -40px 0px'
        });
        
        revealElements.forEach(function(el) { observer.observe(el); });
    }

    // ── Counter Animation ────────────────────────────────────
    function initCounters() {
        var counters = document.querySelectorAll('.counter');
        if (!counters.length) return;
        
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(function(counter) { observer.observe(counter); });
    }
    
    function animateCounter(element) {
        var text = element.textContent;
        var match = text.match(/(\d+)/);
        if (!match) return;
        
        var finalValue = parseInt(match[1]);
        var suffix = text.replace(match[1], '').trim() || '+';
        var currentValue = 0;
        var increment = finalValue / 80;
        var stepTime = 25;
        
        var timer = setInterval(function() {
            currentValue += increment;
            if (currentValue >= finalValue) {
                element.textContent = finalValue + suffix;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(currentValue) + suffix;
            }
        }, stepTime);
    }

    // ── Reduced Motion ───────────────────────────────────────
    function initReducedMotion() {
        var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
        if (mq.matches) {
            document.documentElement.style.scrollBehavior = 'auto';
        }
    }

})();
