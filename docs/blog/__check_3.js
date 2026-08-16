// Initialize GLightbox after DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
      const lightbox = GLightbox({
        selector: '.glightbox',
        touchNavigation: true,
        loop: true,
        closeButton: true,
        openEffect: 'zoom',
        closeEffect: 'fade',
        slideEffect: 'slide',
        moreLength: 0,
        zoomable: true,
        draggable: true,
        preload: true
      });

      // Reading Progress Bar
      window.addEventListener('scroll', function() {
        const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        const progressBar = document.querySelector('.blog-progress-bar');
        if (progressBar) {
          progressBar.style.width = scrolled + '%';
        }
      });
    });
