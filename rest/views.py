from django.contrib.auth.models import User, Group
from rest.models import Word
from rest_framework import viewsets
from rest_framework.views import APIView
from rest.serializers import UserSerializer, GroupSerializer, WordSerializer
from random import randint
from rest_framework.response import Response
from rest_framework import status,generics

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that returns every word
    """
    queryset = Word.objects.all().order_by('-wrongs')
    serializer_class = WordSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class WordView(APIView):
    permission_classes = ()
    def get(self, request, *args, **kw):
        # talvez meter aqui um parametro de dificuldade

        # get 1 false word and 1 true word
        acceptedWords = Word.objects.filter(accepted=True)
        acceptedWord = acceptedWords[randint(0, acceptedWords.count())]

        deniedWords = Word.objects.filter(accepted=False)
        deniedWord = deniedWords[randint(0, deniedWords.count())]

        correcOne = randint(0,1)

        if correcOne == 0:
            words = [acceptedWord.name,deniedWord.name]
        else:
            words = [deniedWord.name,acceptedWord.name]

        response = {"word1":words[0],"word2":words[1]}

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        selectedWord = request.DATA.get("selectedWord","")
        word1 = request.DATA.get("word1","")
        word2 = request.DATA.get("word2","")

        # first check if selected word in words
        if selectedWord != word1 and selectedWord != word2:
            return Response("Selected word is not contained in sent words!", status=status.HTTP_409_CONFLICT)

        # then check if selected word in "accepted words"
        answer = False
        if Word.objects.filter(accepted=True,name=selectedWord).exists():
            answer = True

        # change the hits in the database
        word1 = Word.objects.get(name=word1)
        word2 = Word.objects.get(name=word2)
        if answer:
            serializer = WordSerializer(word1, data = {"corrects": word1.corrects + 1}, partial=True)
            if serializer.is_valid():
                serializer.save()
            serializer = WordSerializer(word2, data = {"corrects": word2.corrects + 1}, partial=True)
            if serializer.is_valid():
                serializer.save()
        else:
            serializer = WordSerializer(word1, data = {"wrongs": word1.wrongs + 1}, partial=True)
            if serializer.is_valid():
                serializer.save()
            serializer = WordSerializer(word2, data = {"wrongs": word2.wrongs + 1}, partial=True)
            if serializer.is_valid():
                serializer.save()

        # then get 2 more words that are not word1 and word2
        acceptedWords = Word.objects.filter(accepted=True).exclude(name=word1).exclude(name=word2)
        acceptedWord = acceptedWords[randint(0, acceptedWords.count())]

        deniedWords = Word.objects.filter(accepted=False).exclude(name=word1).exclude(name=word2)
        deniedWord = deniedWords[randint(0, deniedWords.count())]

        correctOne = randint(0,1)

        if correctOne == 0:
            words = [acceptedWord.name,deniedWord.name]
        else:
            words = [deniedWord.name,acceptedWord.name]

        response = {"answer":answer,"word1":words[0],"word2":words[1]}

        return Response(response, status=status.HTTP_200_OK)
