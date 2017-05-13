from django.contrib.auth.models import User, Group
from rest.models import Word
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ('name', 'accepted','corrects','wrongs')