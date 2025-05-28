from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('nonbinary', 'Non-binary'),
    ]
    
    DRINKING_CHOICES = [
        ('never', 'Never'),
        ('rarely', 'Rarely'),
        ('socially', 'Socially'),
        ('regularly', 'Regularly'),
    ]
    
    SMOKING_CHOICES = [
        ('never', 'Never'),
        ('rarely', 'Rarely'),
        ('socially', 'Socially'),
        ('regularly', 'Regularly'),
    ]
    
    PERSONALITY_CHOICES = [
        ('introvert', 'Introvert'),
        ('extrovert', 'Extrovert'),
        ('ambivert', 'Ambivert'),
    ]
    
    ZODIAC_CHOICES = [
        ('aries', 'Aries'),
        ('taurus', 'Taurus'),
        ('gemini', 'Gemini'),
        ('cancer', 'Cancer'),
        ('leo', 'Leo'),
        ('virgo', 'Virgo'),
        ('libra', 'Libra'),
        ('scorpio', 'Scorpio'),
        ('sagittarius', 'Sagittarius'),
        ('capricorn', 'Capricorn'),
        ('aquarius', 'Aquarius'),
        ('pisces', 'Pisces'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    bio = models.TextField(blank=True)
    
    # Photos - storing as comma-separated filenames
    photo1 = models.ImageField(upload_to='profile_photos/', blank=True)
    photo2 = models.ImageField(upload_to='profile_photos/', blank=True)
    photo3 = models.ImageField(upload_to='profile_photos/', blank=True)
    
    # Hobbies - storing as comma-separated string
    hobbies = models.TextField(blank=True, help_text="Comma-separated hobbies")
    
    personality = models.CharField(max_length=20, choices=PERSONALITY_CHOICES, blank=True)
    zodiac = models.CharField(max_length=20, choices=ZODIAC_CHOICES, blank=True)
    drinking = models.CharField(max_length=20, choices=DRINKING_CHOICES, blank=True)
    smoking = models.CharField(max_length=20, choices=SMOKING_CHOICES, blank=True)
    
    # Preferences - storing as comma-separated string
    preferences = models.TextField(blank=True, help_text="Comma-separated gender preferences")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def get_hobbies_list(self):
        if self.hobbies:
            return [hobby.strip() for hobby in self.hobbies.split(',') if hobby.strip()]
        return []
    
    def set_hobbies_list(self, hobbies_list):
        self.hobbies = ','.join(hobbies_list)
    
    def get_preferences_list(self):
        if self.preferences:
            return [pref.strip() for pref in self.preferences.split(',') if pref.strip()]
        return []
    
    def set_preferences_list(self, preferences_list):
        self.preferences = ','.join(preferences_list)
    
    def get_photos(self):
        photos = []
        for photo in [self.photo1, self.photo2, self.photo3]:
            if photo:
                photos.append(photo.url)
        return photos


class Like(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    is_like = models.BooleanField()  # True for like, False for pass
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        action = "liked" if self.is_like else "passed"
        return f"{self.from_user.username} {action} {self.to_user.username}"


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match: {self.user1.username} & {self.user2.username}"
    
    def get_other_user(self, user):
        return self.user2 if self.user1 == user else self.user1


class Message(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"