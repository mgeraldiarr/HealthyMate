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
        mobileBtn?.addEventListener('click', () => { mobileMenu.classList.toggle('hidden'); });
        window.addEventListener('resize', () => { if (window.innerWidth >= 768) mobileMenu.classList.add('hidden'); });
        document.body.addEventListener('click', (e) => {
            if (window.innerWidth < 768 && !mobileMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
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

        // // FAQ accordion
        // document.querySelectorAll('.faq-toggle').forEach(button => {
        //     button.addEventListener('click', () => {
        //         const faqContent = button.nextElementSibling;
        //         const icon = button.querySelector('i');
                
        //         // Toggle content
        //         faqContent.classList.toggle('hidden');
                
        //         // Rotate icon
        //         icon.classList.toggle('rotate-180');
                
        //         // Smooth height transition
        //         if (!faqContent.classList.contains('hidden')) {
        //             faqContent.style.maxHeight = faqContent.scrollHeight + 'px';
        //         } else {
        //             faqContent.style.maxHeight = null;
        //         }
        //     });
        // });


        // // Save results button
        // const saveResultsBtn = document.getElementById('saveResultsBtn');
        // if (saveResultsBtn) {
        //     saveResultsBtn.addEventListener('click', () => {
        //         showToast('Your results have been saved!');
        //     });
        // }
        
        // // Toast notification function
        // function showToast(message) {
        //     const toast = document.getElementById('toast');
        //     const toastMessage = document.getElementById('toastMessage');
            
        //     toastMessage.textContent = message;
        //     toast.classList.remove('translate-y-10', 'opacity-0');
        //     toast.classList.add('translate-y-0', 'opacity-100');
            
        //     setTimeout(() => {
        //         toast.classList.remove('translate-y-0', 'opacity-100');
        //         toast.classList.add('translate-y-10', 'opacity-0');
        //     }, 3000);
        // }
        