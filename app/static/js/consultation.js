// Hide loader when page is loaded
        window.addEventListener('load', function() {
        const loader = document.getElementById('loader');
            setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => {
            loader.style.display = 'none';
        }, 500);
    }, 500);
});

// Mobile menu toggle
const mobileMenuButton = document.getElementById('mobileMenuButton');
const mobileMenu = document.getElementById('mobileMenu');

mobileMenuButton.addEventListener('click', function() {
    mobileMenu.classList.toggle('hidden');
});
            
            // Smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const targetId = this.getAttribute('href');
                    if (targetId === '#') return;
                    
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {
                        targetElement.scrollIntoView({
                            behavior: 'smooth'
                        });
                    }
                });
            });