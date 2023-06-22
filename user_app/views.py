import string
from random import choice
from .utils import *
from random import randint
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class UserRegistrationView(APIView):

    def post(self, request, format=None):
        serializers = UserRegistrationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'message': 'Registration Successfull'}, status=status.HTTP_201_CREATED)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserLogin(APIView):

    def post(self, request, format=None):
        serializers = UserLoginSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        email = serializers.data.get('email')
        password = serializers.data.get('password')
        u = User.objects.get(email=email)
        if u:
            user = authenticate(username=u.username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'message': "Login success", "token": token, }, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"non_field_errors": ["Email or Password is not Valid"]}}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {"errors": {"non_field_errors": ["User is not Registered"]}}, status=status.HTTP_404_NOT_FOUND
            )


class CreateGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        game = Game.objects.create(user=request.user, board="")
        return Response({"game_id": game.id}, status=status.HTTP_201_CREATED)


class GetBoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, game_id):
        user = request.user
        try:
            game = Game.objects.get(id=game_id, user=user)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"board": game.board}, status=status.HTTP_200_OK)

    def delete(self, request, game_id):
        user = request.user
        try:
            game = Game.objects.get(id=game_id, user=user)
            game_id = game.delete()
            return Response({"message": f"Game:{game_id} deleted successfully"}, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)


class UpdateBoardView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, game_id):
        user = request.user

        try:
            game = Game.objects.get(id=game_id, user=user)
            if game.completed:
                return Response("Game is already completed", status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        character = request.data.get('character')

        if not character:
            return Response({"error": "Character is required."}, status=status.HTTP_400_BAD_REQUEST)

        alphabets = string.ascii_lowercase

        game.board += character + choice(alphabets)

        response = {"board": game.board}

        if len(game.board) == 6:
            game.is_palindrome = is_palindrome(game.board)
            response['is_palindrome'] = game.is_palindrome
            game.completed = True

        game.save()

        return Response(response, status=status.HTTP_200_OK)


class ListGamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        games = Game.objects.filter(user=user).values(
            "id", "board", "is_palindrome", "completed")
        return Response({"games": games}, status=status.HTTP_200_OK)
