from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken






class UserRegistrationView(APIView):

    def post(self, request, format=None):
        serializers = UserRegistrationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'message':'Registration Successfull'}, status=status.HTTP_201_CREATED)
    

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
                return Response({'message':"Login success", "token": token,}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"non_field_errors": ["Email or Password is not Valid"]}},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                    {"errors": {"non_field_errors": ["User is not Registered"]}}, status=status.HTTP_404_NOT_FOUND
                )
        


class CreateGameView(APIView):
    def post(self, request):
        # Authenticate user using token
        user = authenticate_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        game = Game.objects.create(user=user, board="")
        return Response({"game_id": game.id}, status=status.HTTP_201_CREATED)


class GetBoardView(APIView):
    def get(self, request, game_id):
        # Authenticate user using token
        user = authenticate_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            game = Game.objects.get(id=game_id, user=user)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"board": game.board}, status=status.HTTP_200_OK)


class UpdateBoardView(APIView):
    def put(self, request, game_id):
        # Authenticate user using token
        user = authenticate_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            game = Game.objects.get(id=game_id, user=user)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        character = request.data.get('character')

        if not character:
            return Response({"error": "Character is required."}, status=status.HTTP_400_BAD_REQUEST)

        game.board += character

        if len(game.board) >= 6:
            game.is_palindrome = check_palindrome(game.board)

        game.save()

        return Response({"board": game.board}, status=status.HTTP_200_OK)


class ListGamesView(APIView):
    def get(self, request):
        # Authenticate user using token
        user = authenticate_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        games = Game.objects.filter(user=user).values("game_id", "board", "is_palindrome")
        return Response({"games": games}, status=status.HTTP_200_OK)