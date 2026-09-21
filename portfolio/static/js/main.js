// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize project filters (if on projects page)
    if (typeof initProjectFilters === 'function') {
        initProjectFilters();
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


