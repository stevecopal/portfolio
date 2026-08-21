// Animation on Scroll (Intersection Observer)
function initAnimations() {
    const animateOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in', 'opacity-100');
                entry.target.classList.remove('opacity-0');
                
                // Add slide-up effect for elements with specific class
                if (entry.target.classList.contains('slide-up')) {
                    entry.target.classList.add('translate-y-0');
                    entry.target.classList.remove('translate-y-10');
                }
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observe all elements with animation classes
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        el.classList.add('opacity-0');
        if (el.classList.contains('slide-up')) {
            el.classList.add('translate-y-10');
        }
        animateOnScroll.observe(el);
    });
}

// Typing Effect for Hero Section
function initTypingEffect() {
    const typingElement = document.querySelector('.typing-effect');
    if (!typingElement) return;
    
    const text = typingElement.textContent;
    const words = text.split(' ');
    typingElement.textContent = '';
    
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    
    function type() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            typingElement.textContent = typingElement.textContent.slice(0, -1);
            charIndex--;
        } else {
            typingElement.textContent += currentWord[charIndex];
            charIndex++;
        }
        
        let typeSpeed = isDeleting ? 50 : 100;
        
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
    
    // Start typing effect
    setTimeout(type, 1000);
}

// Counter Animation
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = parseInt(target.textContent);
                let currentValue = 0;
                const increment = finalValue / 100;
                const duration = 2000; // 2 seconds
                const stepTime = duration / 100;
                
                const counter = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        target.textContent = finalValue + '+';
                        clearInterval(counter);
                    } else {
                        target.textContent = Math.floor(currentValue) + '+';
                    }
                }, stepTime);
                
                counterObserver.unobserve(target);
            }
        });
    }, {
        threshold: 0.5
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}




