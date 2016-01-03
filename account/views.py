from rest_framework import viewsets
from rest_framework.decorators import list_route
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .models import UserToken
from rest_framework.status import HTTP_400_BAD_REQUEST


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

            # user = authenticate(access_token='1234567890')
            # TODO: Add Facebook auth
            if access_token!='1234567890':
                return Response({'success': False, 'error': 'Invalid token'}, status=HTTP_400_BAD_REQUEST)
            else:
                usertoken = UserToken.objects.create(username='root')
                return Response(
                    {
                        'success': True,
                        'token': usertoken.token.hex
                    }
                )
        return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)

