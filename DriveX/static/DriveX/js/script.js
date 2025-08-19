// script.js - JavaScript functionality

// Mobile menu toggle
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// Intersection Observer for fade-in animations on scroll
function observeElements() {
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: unobserve after animation to save resources
                // observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: '0px 0px -50px 0px' // Start animation a bit before it's fully in view
    });
    
    fadeElements.forEach(element => {
        observer.observe(element);
    });
}

// Set minimum date to today for date inputs
// Note: Django's DateInput widget with type='date' already handles this visually,
// but this can be a good fallback or enhancement.
function setMinDate() {
    // We look for any date input inside a form with the ID 'reservation-form'
    const reservationForm = document.getElementById('reservation-form');
    if (reservationForm) {
        const dateInput = reservationForm.querySelector('input[type="date"]');
        if (dateInput) {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
            const dd = String(today.getDate()).padStart(2, '0');
            dateInput.min = `${yyyy}-${mm}-${dd}`;
        }
    }
}

// Smooth scrolling for internal navigation links (e.g., to #contact)
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Main function to run when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Set minimum date for any date fields
    setMinDate();
    
    // Initialize intersection observer for animations
    observeElements();
    
    // Mobile menu button functionality
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('show');
        });
    }
    
    // Handle window resize for mobile menu cleanup
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && navLinks && navLinks.classList.contains('show')) {
            navLinks.classList.remove('show');
        }
    });
    
    // Close mobile menu when clicking outside of the navigation area
    document.addEventListener('click', (e) => {
        const nav = document.querySelector('nav');
        if (nav && navLinks && !nav.contains(e.target) && navLinks.classList.contains('show')) {
            navLinks.classList.remove('show');
        }
    });
    
    // Add smooth scrolling to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            if (target !== '#') {
                smoothScroll(target);
            }
        });
    });
});

// Función para mostrar notificaciones Toast
function showToastNotifications() {
    // Comprueba si la variable de mensajes de Django existe
    if (typeof django_messages !== 'undefined' && django_messages.length > 0) {
        const container = document.getElementById('toast-container');
        if (!container) return;

        django_messages.forEach((message, index) => {
            // Creamos el elemento toast
            const toast = document.createElement('div');
            toast.className = `toast ${message.tags}`; // Clases: 'toast' y 'success', 'error', etc.
            toast.textContent = message.body;

            // Lo añadimos al contenedor
            container.appendChild(toast);

            // Hacemos que desaparezca después de 5 segundos
            setTimeout(() => {
                toast.classList.add('hide');
                // Lo eliminamos del DOM después de que la animación de salida termine
                toast.addEventListener('animationend', () => {
                    toast.remove();
                });
            }, 5000);
        });
    }
}


// Main function to run when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ... (tu código existente dentro del listener) ...

    // ¡Añade esta línea para activar las notificaciones!
    showToastNotifications();

});