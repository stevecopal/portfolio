// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize project filters (if on projects page)
    if (typeof initProjectFilters === 'function') {
        initProjectFilters();
    }
    
    // Initialize contact form
    if (typeof initContactForm === 'function') {
        initContactForm();
    }
});

// Project Filters
function initProjectFilters() {
    var filterButtons = document.querySelectorAll('[data-filter]');
    if (!filterButtons.length) return;
    
    filterButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            filterButtons.forEach(function(b) { b.classList.remove('active'); });
            btn.classList.add('active');
        });
    });
}

// Contact Form
function initContactForm() {
    var form = document.getElementById('contactForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        var valid = true;
        form.querySelectorAll('[required]').forEach(function(field) {
            if (!field.value.trim()) {
                valid = false;
                field.style.borderColor = '#EF4444';
            } else {
                field.style.borderColor = '';
            }
        });
        if (!valid) {
            e.preventDefault();
            if (typeof showToast === 'function') {
                showToast('Please fill in all required fields.', 'error');
            }
        }
    });
}
