from rest_framework import serializers

from core.models import Blog, Comments

class BlogCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    comments = BlogCommentsSerializer(required=False, many=True)

    class Meta:
        model = Blog
        fields = '__all__'


