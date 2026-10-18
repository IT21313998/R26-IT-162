// Interactive functionality for SLIIT CDAP Project Website
document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navLinks');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // Active navigation highlight based on current page
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const links = document.querySelectorAll('.nav-links a');
  
  links.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Milestone Filter / Dropdown selector (Slide 11)
  const milestoneSelector = document.getElementById('milestoneFilter');
  if (milestoneSelector) {
    milestoneSelector.addEventListener('change', (e) => {
      const selected = e.target.value;
      const items = document.querySelectorAll('.timeline-item');
      
      items.forEach(item => {
        if (selected === 'all' || item.getAttribute('data-status') === selected) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }

  // Contact form submission mock
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const feedback = document.getElementById('formFeedback');
      if (feedback) {
        feedback.innerHTML = `
          <div style="padding: 15px; background: #e8f5e9; color: #2e7d32; border-radius: 8px; margin-top: 15px; border-left: 4px solid #4caf50;">
            <strong>Thank you!</strong> Your message has been sent to the R26-IT-162 research team.
          </div>
        `;
        contactForm.reset();
      }
    });
  }
});
