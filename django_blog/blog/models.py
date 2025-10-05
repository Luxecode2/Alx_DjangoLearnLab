from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone # Import timezone for default=timezone.now

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # Changed related_name to 'posts'
    created_at = models.DateTimeField(default=timezone.now) # Creation timestamp, can be manually edited if needed
    updated_at = models.DateTimeField(auto_now=True) # Automatically updates on each save

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # This is crucial for CreateView and UpdateView to know where to redirect after success
        # The 'blog:post_detail' URL pattern expects a 'pk' (primary key) argument
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_at'] # Order posts by newest first by default