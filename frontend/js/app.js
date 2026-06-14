// MaskVision AI - Main Application Script

document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Update active nav link
    const updateActiveNav = () => {
        const sections = document.querySelectorAll('section[id], div[id]');
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current || 
                (current === '' && link.getAttribute('href') === 'index.html')) {
                link.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav();
});

// Detect mask function for API calls
async function detectMask(imageData) {
    try {
    const response = await fetch(window.APP_CONFIG?.api_base + '/api/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        });

        if (!response.ok) {
            throw new Error('Detection failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Upload file to backend
async function uploadFile(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);

    const response = await fetch(window.APP_CONFIG?.api_base + '/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Check backend health
async function checkBackendHealth() {
    try {
    const response = await fetch(window.APP_CONFIG?.api_base + '/api/health');
        return response.ok;
    } catch (error) {
        console.error('Backend not reachable:', error);
        return false;
    }
}
