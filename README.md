# GUCupid 💕

**A Beautiful Dating App for Gauhati University Students**

![GUCupid Banner](https://img.shields.io/badge/GUCupid-Find%20Your%20Perfect%20Match-FF6B9D?style=for-the-badge&logo=heart&logoColor=white)

[![Django](https://img.shields.io/badge/Django-5.2.1-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![Channels](https://img.shields.io/badge/Django_Channels-WebSocket_Support-092E20?style=flat)](https://channels.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

> *"Where hearts connect and love stories begin"*

## 🌟 Overview

GUCupid is a modern, feature-rich dating application specifically designed for Gauhati University students. Built with Django and real-time WebSocket technology, it provides a safe and engaging platform for university students to connect, match, and build meaningful relationships within their academic community.

## Screenshots
![Screenshot 2025-05-29 133157](https://github.com/user-attachments/assets/120db603-d711-45d9-8ede-a4738e36a880)
![image](https://github.com/user-attachments/assets/792c851e-ef58-461f-b82c-a6d35052d3c6)
![Screenshot 2025-05-29 132947](https://github.com/user-attachments/assets/d99fb4b0-ef2d-44d4-ab44-eb552cc1aad4)
![Screenshot 2025-05-29 133053](https://github.com/user-attachments/assets/5affa90e-a013-4071-90ea-ab0214b7a221)




## ✨ Features

### 🔐 **Authentication & Profile Management**
- **Secure Registration/Login** - University-specific authentication via [`auth_view`](core/views.py)
- **Comprehensive Profiles** - Photos, bio, interests, and academic details via [`profile_setup`](core/views.py)
- **Smart Matching Algorithm** - Based on preferences, interests, and mutual compatibility

### 💕 **Matching System**
- **Swipe Interface** - Intuitive like/pass system implemented in [`home`](core/views.py)
- **Instant Match Notifications** - Real-time alerts via [`like_profile`](core/views.py) and WebSocket consumers
- **Preference Filtering** - Filter by gender, interests, and lifestyle choices
- **Rejected Profile Reset** - Second chances with [`reset_rejected_profiles`](core/views.py)

### 💬 **Real-time Chat**
- **WebSocket-powered Messaging** - Instant communication via [`ChatConsumer`](dating_app/consumers.py)
- **Match-based Conversations** - Chat only with mutual matches through [`chat`](core/views.py)
- **Message Notifications** - Stay updated via [`NotificationConsumer`](dating_app/notifications_consumer.py)
- **Secure Communication** - Private and encrypted conversations

### 🎯 **Advanced Features**
- **Multi-photo Profiles** - Up to 3 photos per profile in [`Profile`](core/models.py)
- **Interest Matching** - 20+ hobby categories for better compatibility
- **Lifestyle Preferences** - Drinking, smoking, personality type matching
- **College & Department Info** - Academic-based connections
- **Zodiac Compatibility** - For those who believe in the stars

### 📱 **User Experience**
- **Mobile-first Design** - Responsive design in [base.html](templates/base.html)
- **Beautiful UI/UX** - Modern gradient design with romantic themes
- **Smooth Animations** - Engaging swipe animations and transitions
- **Tab-based Navigation** - Easy switching between Discover, Matches, and Profile

## 🚀 Tech Stack

### Backend
- **Django 5.2.1** - Robust web framework
- **Django Channels** - WebSocket support for real-time features in [`asgi.py`](dating_app/asgi.py)
- **SQLite** - Lightweight database for development
- **Pillow** - Image handling and processing

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Tailwind CSS** - Utility-first styling framework
- **Vanilla JavaScript** - Custom interactions and WebSocket handling in [`notifications.js`](static/js/notifications.js)
- **Progressive Web App** - Mobile app-like experience

### Real-time Features
- **WebSocket Connections** - Live chat and notifications via [`routing.py`](dating_app/routing.py)
- **Django Channels** - Message queuing and broadcasting
- **Asynchronous Views** - Non-blocking user experience

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager
- Git
- Redis (for WebSocket support)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gucupid.git
   cd GUCupid/LoveSpark
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install django==5.2.1
   pip install channels
   pip install daphne
   pip install pillow
   pip install django-cors-headers
   pip install channels-redis
   ```

4. **Configure environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env file with your settings
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files** (for production)
   ```bash
   python manage.py collectstatic
   ```

### 🚀 Running the Application

#### Development Server (Simple)
```bash
python manage.py runserver
```

#### Production Server with WebSocket Support (Recommended)
```bash
# Using Daphne ASGI server for WebSocket support
daphne -b 0.0.0.0 -p 8000 dating_app.asgi:application
```
