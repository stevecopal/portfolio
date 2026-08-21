// Project Filters
function initProjectFilters() {
    const filterButtons = document.querySelectorAll('.filter-button');
    const projectCards = document.querySelectorAll('.project-card');
    const projectsGrid = document.getElementById('projectsGrid');
    
    if (!filterButtons.length || !projectCards.length || !projectsGrid) return;
    
    // Add click event to all filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active', 'bg-black', 'text-white'));
            filterButtons.forEach(btn => btn.classList.add('border', 'border-gray-300', 'text-black', 'hover:bg-gray-100'));
            
            // Add active class to clicked button
            button.classList.add('active', 'bg-black', 'text-white');
            button.classList.remove('border', 'border-gray-300', 'text-black', 'hover:bg-gray-100');
            
            const filter = button.getAttribute('data-filter');
            
            // Filter project cards
            projectCards.forEach(card => {
                if (filter === 'all') {
                    card.classList.remove('hidden');
                    card.classList.add('animate-fade-in');
                    return;
                }
                
                if (filter === 'featured') {
                    if (card.classList.contains('featured')) {
                        card.classList.remove('hidden');
                        card.classList.add('animate-fade-in');
                    } else {
                        card.classList.add('hidden');
                    }
                    return;
                }
                
                // Technology filter
                if (filter.startsWith('tech-')) {
                    const techId = filter.replace('tech-', '');
                    const cardTechnologies = card.getAttribute('data-technologies');
                    
                    if (cardTechnologies && cardTechnologies.includes(techId)) {
                        card.classList.remove('hidden');
                        card.classList.add('animate-fade-in');
                    } else {
                        card.classList.add('hidden');
                    }
                }
            });
        });
    });
}