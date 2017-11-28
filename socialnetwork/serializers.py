from django.contrib.auth.models import User
from rest_framework import serializers

from socialnetwork.models import Post
from socialnetwork.services import email_exists


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'posts',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate_email(self, email):
        if not email_exists(email):
            raise serializers.ValidationError('Email doesn\'t exist')
        return email


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    number_of_likes = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'
