 // Highlight current page in navigation
        document.addEventListener('DOMContentLoaded', function() {
            // Mobile menu toggle
            const mobileMenuButton = document.getElementById('mobileMenuButton');
            const mobileMenu = document.getElementById('mobileMenu');
            
            mobileMenuButton.addEventListener('click', function() {
                mobileMenu.classList.toggle('hidden');
            });
            
            // Loader
            const loader = document.getElementById('loader');
            window.addEventListener('load', function() {
                setTimeout(function() {
                    loader.classList.add('loader-fade-out');
                }, 500);
            });
            
            // Smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth'
                        });
                        
                        // Close mobile menu if open
                        if (!mobileMenu.classList.contains('hidden')) {
                            mobileMenu.classList.add('hidden');
                        }
                    }
                });
            });
        });