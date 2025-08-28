function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const button = element.nextElementSibling;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

function openUrl(elementId) {
    const element = document.getElementById(elementId);
    const url = element.textContent;
    
    if (url && url !== 'An error occurred') {
        window.open(url, '_blank');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('shortenForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const originalUrl = document.getElementById('originalUrl').value;
        const daysAlive = document.getElementById('daysAlive').value;
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        const shortenBtn = document.getElementById('shortenBtn');
        
        // Reset previous results
        result.classList.remove('show', 'error');
        loading.style.display = 'block';
        shortenBtn.disabled = true;
        
        try {
            const requestBody = { 
                original_url: originalUrl,
                days_alive: parseInt(daysAlive)
            };
            
            const response = await fetch('/api/shorten/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(requestBody)
            });
            
            const data = await response.json();
            console.log('API Response:', data); // Debug log
            
            if (response.ok) {
                // Success
                document.getElementById('resultTitle').textContent = '✅ URL Shortened Successfully!';
                document.getElementById('shortUrl').textContent = data.shorted_url;
                document.getElementById('originalUrlResult').textContent = data.original_url;
                
                // Display QR code if available
                const qrImage = document.getElementById('qrCodeImage');
                
                console.log('QR element found:', qrImage !== null); // Debug log
                console.log('QR Code data:', data.qr_code); // Debug log
                
                if (data.qr_code) {
                    console.log('Setting QR code image...'); // Debug log
                    qrImage.src = data.qr_code;
                    qrImage.style.display = 'block';
                    console.log('QR image src set to:', qrImage.src.substring(0, 50) + '...'); // Debug log
                } else {
                    console.log('No QR code data received'); // Debug log
                    qrImage.style.display = 'none';
                }
                
                // Show all result items on success
                const resultItems = result.querySelectorAll('.result-item');
                resultItems.forEach(item => {
                    item.style.display = 'block';
                });
                
                result.classList.add('show');
                result.classList.remove('error');
            } else {
                // Error
                document.getElementById('resultTitle').textContent = '❌ Error';
                document.getElementById('shortUrl').textContent = data.error || 'An error occurred';
                
                // Hide QR code on error
                document.getElementById('qrCodeImage').style.display = 'none';
                
                // Hide other result items for error state
                const resultItems = result.querySelectorAll('.result-item');
                resultItems.forEach((item, index) => {
                    if (index === 0) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                result.classList.add('show', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('resultTitle').textContent = '❌ Network Error';
            document.getElementById('shortUrl').textContent = 'Failed to connect to server';
            result.classList.add('show', 'error');
        } finally {
            loading.style.display = 'none';
            shortenBtn.disabled = false;
        }
    });
});

// Get CSRF token for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
