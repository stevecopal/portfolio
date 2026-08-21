// Contact Form Validation
function initContactForm() {
    const contactForm = document.querySelector('form[action*="contact"]');
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validate required fields
        const requiredFields = contactForm.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('border-red-500');
                field.classList.remove('border-gray-300');
            } else {
                field.classList.remove('border-red-500');
                field.classList.add('border-gray-300');
            }
        });
        
        // Validate email format
        const emailField = contactForm.querySelector('input[type="email"]');
        if (emailField && !validateEmail(emailField.value)) {
            isValid = false;
            emailField.classList.add('border-red-500');
            emailField.classList.remove('border-gray-300');
        }
        
        if (!isValid) {
            e.preventDefault();
            // Scroll to first error
            const firstError = contactForm.querySelector('.border-red-500');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });
    
    // Email validation helper
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
}

// Initialize contact form validation
document.addEventListener('DOMContentLoaded', initContactForm);