from django.db import models
from django.contrib.auth.models import User

class UserGroup(models.Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User, related_name='user_group')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    simplyfy_debt = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.name}'

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_name', null=True, blank=True)
    friends = models.ManyToManyField(User, related_name='user_friend')
    
    def __str__(self) -> str:
        return f"{self.user.email}"