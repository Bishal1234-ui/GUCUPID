
class NotificationSystem {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.currentChatMatchId = null;
        this.connect();
        
        // Create notification sound
        this.notificationSound = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBjuS1/LPeSUEJ3nJ8N+OSQgVXrPo66hTFgpFn+Dzvmoh');
        this.notificationSound.volume = 0.5;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            console.log('Notification socket connected');
            this.isConnected = true;
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleNotification(data);
        };
        
        this.socket.onclose = () => {
            console.log('Notification socket closed');
            this.isConnected = false;
            // Reconnect after 3 seconds
            setTimeout(() => this.connect(), 3000);
        };
        
        this.socket.onerror = (error) => {
            console.log('Notification socket error:', error);
        };
    }

    handleNotification(data) {
        if (data.type === 'match') {
            this.showMatchNotification(data.message, data.data);
        } else if (data.type === 'message') {
            this.handleMessageNotification(data.message, data.data);
        }
    }

    showMatchNotification(message, data) {
        // Play notification sound
        this.playNotificationSound();
        
        // Show popup notification
        this.showPopupNotification('🎉 New Match!', message, 'match');
        
        // If on home page, show the existing match modal
        if (window.location.pathname === '/' && typeof showMatchModal === 'function') {
            showMatchModal(data.other_user, data.match_id);
        }
    }

    handleMessageNotification(message, data) {
        // Don't show notification if user is currently in chat with sender
        if (this.currentChatMatchId && this.currentChatMatchId === data.match_id) {
            return;
        }
        
        // Play notification sound
        this.playNotificationSound();
        
        // Show popup notification
        this.showPopupNotification('💬 New Message', message, 'message', data.match_id);
    }

    showPopupNotification(title, message, type, matchId = null) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 bg-white rounded-lg shadow-lg border-l-4 p-4 max-w-sm transform translate-x-full transition-transform duration-300 ${type === 'match' ? 'border-pink-500' : 'border-blue-500'}`;
        
        notification.innerHTML = `
            <div class="flex items-start">
                <div class="flex-1">
                    <h4 class="text-sm font-semibold text-gray-800">${title}</h4>
                    <p class="text-sm text-gray-600 mt-1">${message}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-gray-400 hover:text-gray-600">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                    </svg>
                </button>
            </div>
        `;
        
        // Add click handler for message notifications
        if (type === 'message' && matchId) {
            notification.style.cursor = 'pointer';
            notification.onclick = () => {
                window.location.href = `/chat/${matchId}/`;
            };
        }
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(full)';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }

    playNotificationSound() {
        try {
            this.notificationSound.currentTime = 0;
            this.notificationSound.play().catch(e => {
                console.log('Could not play notification sound:', e);
            });
        } catch (e) {
            console.log('Could not play notification sound:', e);
        }
    }

    setCurrentChatMatch(matchId) {
        this.currentChatMatchId = matchId;
    }

    clearCurrentChatMatch() {
        this.currentChatMatchId = null;
    }
}

// Initialize notification system
const notificationSystem = new NotificationSystem();

// Make it globally available
window.notificationSystem = notificationSystem;
