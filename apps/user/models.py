from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Para soportar hashes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Asegurarse de que la contraseña esté encriptada antes de guardarla
        if not self.pk:  # Si es un nuevo objeto
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def get_view_count(self):
        from django.db.models import Count
        return ViewCount.objects.filter(user=self).aggregate(total_views=Count('id'))['total_views']

class ViewCount(models.Model):
    user = models.ForeignKey(User, related_name='user_view_count', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
        
    def __str__(self):
        return f"{self.ip_address}"
