// Global app JavaScript

// Hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');

    if (flashMessages.length > 0) {
        setTimeout(function() {
            flashMessages.forEach(function(message) {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }

    // Update user status when page becomes visible/hidden
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            updateUserStatus('online');
        } else if (document.visibilityState === 'hidden') {
            updateUserStatus('idle');
        }
    });

    // Update user status on page load
    updateUserStatus('online');

    // Update user status function
    function updateUserStatus(status) {
        // Only update if user is logged in
        const userInfo = document.querySelector('.user-info');
        if (!userInfo) return;

        fetch('/api/users/status', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status })
        }).catch(error => {
            console.error('Error updating status:', error);
        });
    }

    // Update user status before page unload
    window.addEventListener('beforeunload', function() {
        // Use synchronous request for beforeunload
        const xhr = new XMLHttpRequest();
        xhr.open('PUT', '/api/users/status', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ status: 'offline' }));
    });
});