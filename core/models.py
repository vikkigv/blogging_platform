from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Blog(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author_id')
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, db_column='blog_id', related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'blog_comments'

    def __str__(self):
        return self.comment