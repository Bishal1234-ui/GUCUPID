from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Exists, OuterRef
from django.core.paginator import Paginator
from .models import Profile, Like, Match, Message
import json


def auth_view(request):
    """Handle both login and registration"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            return redirect('home')
        else:
            return redirect('profile_setup')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if hasattr(user, 'profile'):
                    return redirect('home')
                else:
                    return redirect('profile_setup')
            else:
                messages.error(request, 'Invalid username or password')
                
        elif action == 'register':
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                login(request, user)
                return redirect('profile_setup')
    
    return render(request, 'core/auth.html')


def logout_view(request):
    logout(request)
    return redirect('auth')


@login_required
def profile_setup(request):
    """Create or edit user profile"""
    profile = None
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio', '')
        hobbies = request.POST.getlist('hobbies')
        personality = request.POST.get('personality', '')
        zodiac = request.POST.get('zodiac', '')
        drinking = request.POST.get('drinking', '')
        smoking = request.POST.get('smoking', '')
        preferences = request.POST.getlist('preferences')
        college = request.POST.get('college', '')
        department = request.POST.get('department', '')
        
        if profile:
            profile.name = name
            profile.age = age
            profile.gender = gender
            profile.bio = bio
            profile.set_hobbies_list(hobbies)
            profile.personality = personality
            profile.zodiac = zodiac
            profile.drinking = drinking
            profile.smoking = smoking
            profile.college = college
            profile.department = department
            profile.set_preferences_list(preferences)
        else:
            profile = Profile.objects.create(
                user=request.user,
                name=name,
                age=age,
                gender=gender,
                bio=bio,
                personality=personality,
                zodiac=zodiac,
                drinking=drinking,
                smoking=smoking,
                college=college,
                department=department
            )
            profile.set_hobbies_list(hobbies)
            profile.set_preferences_list(preferences)
        
        # Handle photo uploads
        for i in range(1, 4):
            photo_field = f'photo{i}'
            if photo_field in request.FILES:
                setattr(profile, photo_field, request.FILES[photo_field])
        
        profile.save()
        messages.success(request, 'Profile saved successfully!')
        return redirect('home')
    
    # Get available hobbies
    hobbies_list = [
        'gym', 'travel', 'cooking', 'music', 'art', 'reading', 'movies', 'gaming',
        'photography', 'yoga', 'hiking', 'dancing', 'writing', 'sports', 'gardening',
        'crafts', 'technology', 'fashion', 'wine', 'coffee'
    ]
    
    context = {
        'profile': profile,
        'hobbies_list': hobbies_list,
        'user_hobbies': profile.get_hobbies_list() if profile else [],
        'user_preferences': profile.get_preferences_list() if profile else [],
    }
    
    return render(request, 'core/profile_setup.html', context)


@login_required
def home(request):
    """Main app page with discover, matches, and profile tabs"""
    if not hasattr(request.user, 'profile'):
        return redirect('profile_setup')
    
    # Get user's profile and preferences
    user_profile = request.user.profile
    user_preferences = user_profile.get_preferences_list()
    
    # Get users that current user has already liked/passed
    liked_user_ids = Like.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    
    # Get potential matches based on preferences
    potential_matches = Profile.objects.exclude(
        user=request.user
    ).exclude(
        user_id__in=liked_user_ids
    )
    
    # Filter by user's preferences
    if user_preferences:
        potential_matches = potential_matches.filter(gender__in=user_preferences)
    
    # Filter by mutual preferences (others who are interested in user's gender)
    potential_matches = potential_matches.filter(
        Q(preferences__icontains=user_profile.gender) | Q(preferences='')
    )
    
    # Get user's matches
    user_matches = Match.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).order_by('-created_at')
    
    context = {
        'user_profile': user_profile,
        'potential_matches': potential_matches[:10],  # Limit to 10 profiles
        'matches': user_matches,
    }
    
    return render(request, 'core/home.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def like_profile(request):
    """Handle like/pass action"""
    try:
        data = json.loads(request.body)
        to_user_id = data.get('user_id')
        is_like = data.get('is_like')
        
        to_user = get_object_or_404(User, id=to_user_id)
        
        # Check if already liked/passed
        existing_like = Like.objects.filter(from_user=request.user, to_user=to_user).first()
        if existing_like:
            return JsonResponse({'error': 'Already interacted with this user'}, status=400)
        
        # Create like/pass
        like = Like.objects.create(
            from_user=request.user,
            to_user=to_user,
            is_like=is_like
        )
        
        match_created = False
        match_id = None
        
        # Check for mutual like
        if is_like:
            mutual_like = Like.objects.filter(
                from_user=to_user,
                to_user=request.user,
                is_like=True
            ).first()
            
            if mutual_like:
                # Create match (ensure consistent ordering)
                user1, user2 = (request.user, to_user) if request.user.id < to_user.id else (to_user, request.user)
                match, created = Match.objects.get_or_create(user1=user1, user2=user2)
                match_created = created
                match_id = match.id
        
        return JsonResponse({
            'success': True,
            'match_created': match_created,
            'match_id': match_id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def chat(request, match_id):
    """Chat page for a specific match"""
    match = get_object_or_404(Match, id=match_id)
    
    # Verify user is part of this match
    if request.user not in [match.user1, match.user2]:
        messages.error(request, 'You do not have access to this chat')
        return redirect('home')
    
    # Get the other user
    other_user = match.get_other_user(request.user)
    
    # Get messages for this match
    chat_messages = Message.objects.filter(match=match).order_by('created_at')
    
    context = {
        'match': match,
        'other_user': other_user,
        'other_profile': other_user.profile,
        'messages': chat_messages,
    }
    
    return render(request, 'core/chat.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request, match_id):
    """Send a message in a chat"""
    try:
        match = get_object_or_404(Match, id=match_id)
        
        # Verify user is part of this match
        if request.user not in [match.user1, match.user2]:
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Message content cannot be empty'}, status=400)
        
        message = Message.objects.create(
            match=match,
            sender=request.user,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'sender': message.sender.username,
                'created_at': message.created_at.isoformat()
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_messages(request, match_id):
    """Get messages for a match (for AJAX updates)"""
    try:
        match = get_object_or_404(Match, id=match_id)
        
        # Verify user is part of this match
        if request.user not in [match.user1, match.user2]:
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        messages_data = []
        for message in Message.objects.filter(match=match).order_by('created_at'):
            messages_data.append({
                'id': message.id,
                'content': message.content,
                'sender': message.sender.username,
                'is_own': message.sender == request.user,
                'created_at': message.created_at.isoformat()
            })
        
        return JsonResponse({'messages': messages_data})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def unmatch_user(request):
    """Unmatch two users and remove their likes"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        
        try:
            data = json.loads(request.body)
            match_id = data.get('match_id')
            
            # Get the match
            match = Match.objects.get(
                Q(id=match_id) & (Q(user1=request.user) | Q(user2=request.user))
            )
            
            # Get the other user
            other_user = match.user2 if match.user1 == request.user else match.user1
            
            # Delete the likes between both users
            Like.objects.filter(
                Q(from_user=request.user, to_user=other_user) |
                Q(from_user=other_user, to_user=request.user)
            ).delete()
            
            # Delete all messages in this match
            Message.objects.filter(match=match).delete()
            
            # Delete the match
            match.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Successfully unmatched'
            })
            
        except Match.DoesNotExist:
            return JsonResponse({'error': 'Match not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def reset_rejected_profiles(request):
    """Reset all rejected profiles (remove pass likes) for the current user"""
    try:
        # Delete all "pass" likes from the current user
        deleted_count = Like.objects.filter(
            from_user=request.user,
            is_like=False
        ).delete()[0]
        
        return JsonResponse({
            'success': True,
            'message': f'Reset {deleted_count} rejected profiles'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)