from user.serializers import UserSerializer


def create_user(data):
    user_serializer = UserSerializer(data=data)
    user_serializer.is_valid(raise_exception=False)
    print(user_serializer.errors)
    user_serializer.save()
    return user_serializer.data
