import facebook
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import UserToken, UserProfile
from .serializers import LoginSerializer, UserProfileSerializer


class AccountViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer

    @list_route(methods=['POST'])
    def login(self, request):
        """
        Logs in the user.
        ---
        request_serializer: LoginSerializer
        """
        serialized_data = LoginSerializer(data=request.data)
        if serialized_data.is_valid():
            access_token = serialized_data.validated_data['access_token']

            graph = facebook.GraphAPI(access_token=access_token, version='2.5')

            try:
                fb_user = graph.get_object('me?fields=id,first_name,last_name,picture,email')
            except facebook.GraphAPIError:
                return Response({'success': False, 'error': 'Invalid token'}, status=HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(username=fb_user['id'])
            if created:
                user.set_unusable_password()
                UserProfile.objects.create(user=user)

            user.first_name = fb_user['first_name']
            user.last_name = fb_user['last_name']
            user.profile.picture = fb_user['picture']['data']['url']

            if 'email' in fb_user:
                user.email = fb_user['email']

            user.save()
            user.profile.save()

            user_token = UserToken.objects.create(user=user)
            return Response(
                    {
                        'success': True,
                        'token': user_token.token.hex,
                        'uid': User.objects.get(email=user.email).pk,
                    }
            )

        return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user  # type User
        user_profile_serialized = UserProfileSerializer(user.profile)
        return Response(user_profile_serialized.data)
