// script.js - JavaScript functionality

// Mobile menu toggle
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// Vehicle data
const vehicles = [
    {
        name: 'Mercedes-Benz Clase S',
        icon: '🏎️',
        description: 'Elegancia y confort supremo con tecnología de vanguardia para ejecutivos exigentes.',
        features: 'Asientos de cuero, climatización automática, sistema de sonido premium',
        value: 'mercedes-s'
    },
    {
        name: 'BMW X7 xDrive',
        icon: '🚙',
        description: 'SUV premium espacioso y potente, perfecto para viajes familiares de lujo.',
        features: 'Tracción integral, 7 asientos, techo panorámico, asistente de conducción',
        value: 'bmw-x7'
    },
    {
        name: 'Audi A8 Quattro',
        icon: '🏁',
        description: 'Innovación alemana y diseño sofisticado para una experiencia de conducción inigualable.',
        features: 'Matrix LED, suspensión neumática, cockpit virtual, masaje en asientos',
        value: 'audi-a8'
    },
    {
        name: 'Tesla Model S',
        icon: '⚡',
        description: 'Vehículo eléctrico de lujo con tecnología autopilot y rendimiento excepcional.',
        features: 'Autopilot, pantalla táctil 17", carga rápida, 0-100 km/h en 3.2s',
        value: 'tesla-s'
    },
    {
        name: 'Porsche Panamera',
        icon: '🏃‍♂️',
        description: 'Deportivo de lujo de 4 puertas que combina performance y elegancia.',
        features: 'Motor V8 biturbo, chasis deportivo, frenos cerámicos, interior deportivo',
        value: 'porsche-panamera'
    },
    {
        name: 'Range Rover Vogue',
        icon: '🏔️',
        description: 'SUV de lujo británico con capacidades todo terreno y máximo confort.',
        features: 'Control de terreno, suspensión neumática, interior en cuero Windsor',
        value: 'range-rover'
    },
    {
        name: 'Bentley Continental GT',
        icon: '👑',
        description: 'Gran turismo británico que representa la máxima expresión del lujo automotriz.',
        features: 'Motor W12, interior artesanal, sistema de sonido Naim, acabados en madera',
        value: 'bentley-gt'
    },
    {
        name: 'Maserati Quattroporte',
        icon: '🇮🇹',
        description: 'Sedán deportivo italiano que combina elegancia, performance y exclusividad.',
        features: 'Motor Ferrari V6, escape deportivo, interior italiano, suspensión Skyhook',
        value: 'maserati-quattroporte'
    }
];

// Load all vehicles in vehicles page (if needed dynamically)
function loadAllVehicles() {
    const grid = document.getElementById('all-vehicles-grid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    vehicles.forEach((vehicle, index) => {
        const vehicleCard = document.createElement('div');
        vehicleCard.className = 'vehicle-card fade-in';
        vehicleCard.style.animationDelay = `${index * 0.1}s`;
        
        vehicleCard.innerHTML = `
            <div class="vehicle-image">${vehicle.icon}</div>
            <div class="vehicle-content">
                <h3>${vehicle.name}</h3>
                <p>${vehicle.description}</p>
                <p style="font-size: 0.8rem; color: var(--primary-gold); margin-bottom: 1rem;">
                    ${vehicle.features}
                </p>
                <a href="/reserva/?vehicle=${vehicle.value}" class="vehicle-button">Reservar</a>
            </div>
        `;
        
        grid.appendChild(vehicleCard);
    });
}

// Form validation
function validateForm() {
    let isValid = true;
    const requiredFields = ['name', 'email', 'phone', 'vehicle', 'date', 'time', 'duration', 'pickup', 'pickup-address'];
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        const errorDiv = document.getElementById(fieldId + '-error');
        
        if (!field) return; // Skip if field doesn't exist on current page
        
        if (!field.value.trim()) {
            if (errorDiv) {
                errorDiv.style.display = 'block';
                field.style.borderColor = '#ff6b6b';
            }
            isValid = false;
        } else {
            if (errorDiv) {
                errorDiv.style.display = 'none';
                field.style.borderColor = 'rgba(201, 167, 77, 0.2)';
            }
        }
    });
    
    // Email validation
    const email = document.getElementById('email');
    if (email && email.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const emailError = document.getElementById('email-error');
        if (!emailRegex.test(email.value)) {
            if (emailError) {
                emailError.style.display = 'block';
                emailError.textContent = 'Por favor ingresa un correo válido';
                email.style.borderColor = '#ff6b6b';
            }
            isValid = false;
        }
    }
    
    // Date validation (not in the past)
    const dateField = document.getElementById('date');
    if (dateField && dateField.value) {
        const selectedDate = new Date(dateField.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        const dateError = document.getElementById('date-error');
        if (selectedDate < today) {
            if (dateError) {
                dateError.style.display = 'block';
                dateError.textContent = 'La fecha no puede ser anterior a hoy';
                dateField.style.borderColor = '#ff6b6b';
            }
            isValid = false;
        }
    }
    
    return isValid;
}

// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    
    if (validateForm()) {
        // If validation passes, submit the form normally
        const form = event.target;
        
        // Show success message
        const successMessage = document.getElementById('success-message');
        if (successMessage) {
            successMessage.style.display = 'block';
            successMessage.scrollIntoView({ behavior: 'smooth' });
            
            // Hide success message after 5 seconds
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 5000);
        }
        
        // For Django, you might want to actually submit the form
        // Uncomment the next line to allow normal form submission
        // form.submit();
        
        // Reset form after successful submission
        form.reset();
    }
}

// Intersection Observer for animations
function observeElements() {
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    fadeElements.forEach(element => {
        element.classList.remove('visible');
        observer.observe(element);
    });
}

// Set minimum date to today
function setMinDate() {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear();
        dateInput.min = yyyy + '-' + mm + '-' + dd;
    }
}

// Real-time form validation
function setupRealTimeValidation() {
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            const errorDiv = document.getElementById(input.id + '-error');
            if (errorDiv) {
                if (!input.value.trim() && input.required) {
                    errorDiv.style.display = 'block';
                    input.style.borderColor = '#ff6b6b';
                } else {
                    errorDiv.style.display = 'none';
                    input.style.borderColor = 'rgba(201, 167, 77, 0.2)';
                }
            }
        });
        
        input.addEventListener('focus', () => {
            input.style.borderColor = 'var(--primary-gold)';
        });
    });
}

// Smooth scrolling for navigation links
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Dynamic availability check (simulation)
function checkAvailability() {
    const vehicle = document.getElementById('vehicle');
    const date = document.getElementById('date');
    const time = document.getElementById('time');
    
    if (vehicle && date && time && vehicle.value && date.value && time.value) {
        // Simulate availability check
        setTimeout(() => {
            // Random availability (90% chance of being available)
            const isAvailable = Math.random() > 0.1;
            
            // You could show availability status here
            console.log(`Availability for ${vehicle.value} on ${date.value} at ${time.value}: ${isAvailable ? 'Available' : 'Not Available'}`);
        }, 500);
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Set up form event listener
    const reservationForm = document.getElementById('reservation-form');
    if (reservationForm) {
        reservationForm.addEventListener('submit', handleFormSubmit);
    }
    
    // Set minimum date
    setMinDate();
    
    // Setup real-time validation
    setupRealTimeValidation();
    
    // Initialize intersection observer
    observeElements();
    
    // Add availability check listeners
    const vehicleSelect = document.getElementById('vehicle');
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    
    if (vehicleSelect && dateInput && timeInput) {
        [vehicleSelect, dateInput, timeInput].forEach(input => {
            input.addEventListener('change', checkAvailability);
        });
    }
    
    // Handle window resize for mobile menu
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            const navLinks = document.querySelector('.nav-links');
            if (navLinks) {
                navLinks.classList.remove('active');
            }
        }
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        const nav = document.querySelector('nav');
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const navLinks = document.querySelector('.nav-links');
        
        if (nav && navLinks && !nav.contains(e.target) && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
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

// Re-trigger animations when page loads or changes
window.addEventListener('load', () => {
    observeElements();
});

window.addEventListener('scroll', () => {
    // Optional: Re-observe elements on scroll for dynamic content
    // observeElements();
});