# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from .serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(APIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token_jwt = serializer.validated_data.get("auth_token")

        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                id_token_jwt, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            )

            # Check if email is verified
            if idinfo["email_verified"]:
                email = idinfo["email"]
                name = idinfo.get("name", "")

                # Check if this user exists
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    # Create a new user
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=None,  # Password not needed for OAuth
                        first_name=name.split()[0] if name and " " in name else name,
                    )
                    user.save()

                # Generate or get token
                token, _ = Token.objects.get_or_create(user=user)

                return Response(
                    {
                        "token": token.key,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "name": user.get_full_name(),
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Email not verified with Google"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
