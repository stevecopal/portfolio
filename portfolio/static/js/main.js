// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle
    if (typeof initThemeToggle === 'function') {
        initThemeToggle();
    }
    
    // Initialize project filters (if on projects page)
    if (typeof initProjectFilters === 'function') {
        initProjectFilters();
    }
    
    // Initialize blog filters (if on blog page)
    if (typeof initBlogFilters === 'function') {
        initBlogFilters();
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
