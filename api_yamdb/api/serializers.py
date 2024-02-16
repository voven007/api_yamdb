from rest_framework import serializers

from reviews.models import Comment, Review



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('__all__')

class CommentSerializer(serializers.ModelSerializer):
     author = serializers.StringRelatedField(
        read_only=True
    )

     class Comment:
        model = Comment
        fields = ('__all__')