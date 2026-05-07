        // Loader fade
        window.addEventListener('load', () => {
            const loader = document.getElementById('loader');
            setTimeout(() => {
                document.getElementById('loader').classList.add('opacity-0', 'pointer-events-none');
            }, 500);
            setTimeout(() => {
                document.getElementById('loader').style.display = 'none';
            }, 1000);
        });

        // Mobile menu toggle
        const mobileBtn = document.getElementById('mobileMenuButton');
        const mobileMenu = document.getElementById('mobileMenu');
        mobileBtn?.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
        window.addEventListener('resize', () => {
            if (window,innerWidth >= 768) mobileMenu.classList.add('hidden');
        });
        document.body.addEventListener('click', (e) => {
            if (window.innerWidth < 768 && !mobileMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Animation on scroll
        const animateOnScroll = () => {
            const elements = document.querySelectorAll('.animate-fade-in-up');
            elements.forEach(element => {
                const elementPosition = element.getBoundingClientRect().top;
                const screenPosition = window.innerHeight / 1.2;
                
                if(elementPosition < screenPosition) {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }
            });
        };

        window.addEventListener('scroll', animateOnScroll);
        window.addEventListener('load', animateOnScroll);

        


