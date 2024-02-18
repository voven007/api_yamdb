from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review, Title



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('__all__')
    
    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST' and Review.objects.filter(
                author=request.user, title=title).exists()):
            raise ValidationError(
                'Нельзя сделать более одного отзыва!'
            )
        return data

class CommentSerializer(serializers.ModelSerializer):
     author = serializers.StringRelatedField(
        read_only=True,
    )

     class Meta:
        model = Comment
        fields = ('__all__')