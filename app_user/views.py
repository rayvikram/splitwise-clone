from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import UserGroup, Friend

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "id"]


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    friends_list = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = '__all__'
    
    def get_friends_list(self, obj):
        return UserSerializer(obj.friends.all(), many=True).data


# =========================================================================== #
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.resolver_match.url_name == "user-token":
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=["post"])
    def token(self, request, pk=None):
        if User.objects.get(username=request.data.get("username")).check_password(
            request.data.get("password")
        ):
            token, _ = Token.objects.get_or_create(
                user=User.objects.get(username=request.data.get("username"))
            )
            return Response({"token": token.key})
        return Response(
            {"message": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class GroupView(viewsets.ModelViewSet):
    """
    - WIll return all groups created by user

    Args:
        viewsets ([type]): [description]

    Returns:
        [type]: [description]
    """
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    
    def get_queryset(self):
        return UserGroup.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    

class FriendView(viewsets.ModelViewSet):
    """
    - WIll return all groups created by user

    Args:
        viewsets ([type]): [description]

    Returns:
        [type]: [description]
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    
    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        if not data.get('friends'):
            return Response({"message": "Please send Friend email list"}, status=status.HTTP_400_BAD_REQUEST)
        friend, _ = Friend.objects.get_or_create(user=request.user)
        for friend_email in data.get('friends'):
            friend_user = User.objects.filter(email=friend_email).first()
            if friend_user:
                friend.friends.add(friend_user)
            else:
                print(f"No user with email {friend_email}")
        return Response(FriendSerializer(friend).data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        data = request.data
        if not data.get('friends'):
            return Response({"message": "Please send Updated Friend email list"}, status=status.HTTP_400_BAD_REQUEST)
        friend, _ = Friend.objects.get_or_create(user=request.user)
        friend.friends.clear()
        for friend_email in data.get('friends'):
            friend_user = User.objects.filter(email=friend_email).first()
            if friend_user:
                friend.friends.add(friend_user)
            else:
                print(f"No user with email {friend_email}")
        return Response(FriendSerializer(friend).data)
    