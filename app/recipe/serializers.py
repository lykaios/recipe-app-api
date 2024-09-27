"""
Serializers for recipe APIs
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    # override default method in class so that we can create tags
    def create(self, validated_data):
        """Create a recipe."""
        # we have to pop tags out so that we dont pass it into Recipe.create()
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        # as we are outside of View, we have to pass in request context to retrieve user
        auth_user = self.context['request'].user
        # **tag passes in all key-value pairs rather than a single one e.g. name=tame['name']
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)

        return recipe

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""

    # simply add an additional field to base Class
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']



