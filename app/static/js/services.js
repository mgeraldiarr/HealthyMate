// Animation for service icons
        document.querySelectorAll('.service-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.querySelector('.service-icon').classList.add('rotate-y-180');
            });
            card.addEventListener('mouseleave', function() {
                this.querySelector('.service-icon').classList.remove('rotate-y-180');
            });
        });

        // Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
            mobileMenu.classList.add('hidden');
        }
    });

    // Loader functionality
    const loader = document.getElementById('loader');
    if (loader) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                loader.style.opacity = '0';
                setTimeout(function() {
                    loader.style.display = 'none';
                }, 500);
            }, 500);
        });
    }

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
});

// // WhatsApp Reservasi
// document.querySelectorAll('[data-wa-reservasi]').forEach(button => {
//     button.addEventListener('click', function(e) {
//         e.preventDefault();
//         const phone = '6281287258113'; // Ganti dengan nomor Anda
//         const message = encodeURIComponent('Halo HealthyMate, saya ingin konsultasi nutrisi');
//         window.open(`https://wa.me/${phone}?text=${message}`, '_blank');
//     });
// });