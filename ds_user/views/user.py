from rest_framework import status, permissions, parsers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from ds_user.serializer.user_serializer import UserSerializer, UserModelSerializer
from django.utils.translation import gettext as _
from rest_framework.views import APIView


class BannedAPIView(APIView):
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = UserSerializer

    def post(self, r):
        self.serializer_class.banned(r.data.get('token'))
        return Response({"message": _("Accounts has been banned")}, status=status.HTTP_200_OK)


class AvatarAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]
    serializer_class = UserSerializer

    def post(self, r):
        user = r.user
        serializer = self.serializer_class.avatar(r.data, user)
        if not serializer:
            return Response({"message": _("Something went wrong, please try again later")}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': _("Profile has been updated")}, status=status.HTTP_200_OK)


class UpdateAPIVIew(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]
    serializer_class = UserSerializer

    def post(self, r):
        user = r.user
        serializer = self.serializer_class(user, data=r.data)
        serializer.context['args'] = 'update'
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Profile has been updated")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, r):
        serializer = self.serializer_class.r_u(r.data.get('token'))
        if not serializer:
            return Response({'message': _("Accounts not found")}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": _("Accounts has been reset")})


class PasswordAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, r):
        user = r.user
        serializer = self.serializer_class(user, data=r.data)
        serializer.context['args'] = 'password'
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('Password has been updated')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserModelViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    serializer_query = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny, ]
        else:
            permission_classes = [permissions.IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def list(self, r):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, r):
        serializer = self.serializer_query(data=r.data)
        serializer.context['args'] = "create"
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _("Accounts has been created")}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retreive(self, r, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        if not queryset:
            return Response({'message': _("Accounts not found")}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
