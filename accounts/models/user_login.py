from django.db import models


class UserLogin(models.Model):
    """
    Simple model to store fictitious user login credentials.
    No real authentication - just stores emails and passwords.
    """
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_logins'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email