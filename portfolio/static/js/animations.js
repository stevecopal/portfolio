// Animations: scroll reveal, counter animation, typing effect
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initScrollReveal();
        initCounters();
        initTypingEffect();
    });

    // ── Scroll Reveal ────────────────────────────────────────
    function initScrollReveal() {
        var revealElements = document.querySelectorAll('.reveal');
        if (!revealElements.length) return;
        
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
        
        revealElements.forEach(function(el) {
            observer.observe(el);
        });
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
        
        counters.forEach(function(counter) {
            observer.observe(counter);
        });
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

    // ── Typing Effect ────────────────────────────────────────
    function initTypingEffect() {
        var typingElement = document.querySelector('.typing-effect');
        if (!typingElement) return;
        
        var text = typingElement.textContent;
        var words = text.split(' ');
        typingElement.textContent = '';
        
        var wordIndex = 0;
        var charIndex = 0;
        var isDeleting = false;
        
        function type() {
            var currentWord = words[wordIndex] || '';
            
            if (isDeleting) {
                typingElement.textContent = typingElement.textContent.slice(0, -1);
                charIndex--;
            } else {
                typingElement.textContent += currentWord[charIndex] || '';
                charIndex++;
            }
            
            var typeSpeed = isDeleting ? 50 : 100;
            
            if (!isDeleting && charIndex === currentWord.length) {
                typeSpeed = 2000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typeSpeed = 500;
            }
            
            setTimeout(type, typeSpeed);
        }
        
        setTimeout(type, 1000);
    }

})();
