// Loader
        document.addEventListener('DOMContentLoaded', () => {
            const loader = document.getElementById('loader');
            if (loader) {
                setTimeout(() => {
                    loader.classList.add('loader-fade-out');
                    document.body.classList.remove('bg-gray-50');
                    loader.addEventListener('animationend', () => loader.remove(), { once: true });
                }, 1500);
            }
        });

        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobileMenuButton');
        const mobileMenu = document.getElementById('mobileMenu');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
                document.body.style.overflow = mobileMenu.classList.contains('hidden') ? '' : 'hidden';
                
                // Toggle button icon
                const icon = mobileMenuButton.querySelector('svg');
                if (mobileMenu.classList.contains('hidden')) {
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
                } else {
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
                }
            });
        }

        // Close mobile menu when clicking on a link
        const mobileLinks = document.querySelectorAll('#mobileMenu a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (mobileMenu) mobileMenu.classList.add('hidden');
                if (mobileMenuButton) {
                    const icon = mobileMenuButton.querySelector('svg');
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
                }
                document.body.style.overflow = '';
            });
        });

        // Auto-close flash messages after 5 seconds
        document.addEventListener('DOMContentLoaded', () => {
            const flashes = document.querySelectorAll('[class*="bg-"]');
            flashes.forEach(flash => {
                setTimeout(() => {
                    flash.remove();
                }, 5000);
            });
        });