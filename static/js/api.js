// API utilities and common functions

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastBody = document.getElementById('toast-body');
    const toastHeader = toast.querySelector('.toast-header');
    
    // Remove existing classes
    toast.classList.remove('text-bg-success', 'text-bg-danger', 'text-bg-info', 'text-bg-warning');
    
    // Add appropriate class based on type
    switch (type) {
        case 'success':
            toast.classList.add('text-bg-success');
            break;
        case 'error':
            toast.classList.add('text-bg-danger');
            break;
        case 'warning':
            toast.classList.add('text-bg-warning');
            break;
        default:
            toast.classList.add('text-bg-info');
    }
    
    toastBody.textContent = message;
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle API errors
function handleApiError(response, fallbackMessage = 'An error occurred') {
    if (response.status === 404) {
        return 'Resource not found';
    } else if (response.status === 400) {
        return 'Invalid request data';
    } else if (response.status === 409) {
        return 'Resource already exists';
    } else if (response.status === 500) {
        return 'Server error';
    }
    return fallbackMessage;
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Set active navigation item
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setActiveNavItem();
    
    // Add loading indicators to buttons on click
    document.addEventListener('click', function(e) {
        if (e.target.matches('button[type="submit"], .btn-primary')) {
            const button = e.target;
            const originalText = button.innerHTML;
            
            // Don't add loading to buttons that already have it or are disabled
            if (button.disabled || button.innerHTML.includes('spinner-border')) {
                return;
            }
            
            // Add loading spinner
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
            
            // Reset after 3 seconds as fallback
            setTimeout(() => {
                button.disabled = false;
                button.innerHTML = originalText;
            }, 3000);
        }
    });
    
    // Global error handler for unhandled promise rejections
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        showToast('An unexpected error occurred', 'error');
    });
}); 