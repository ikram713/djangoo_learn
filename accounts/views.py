from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import SignupSerializer

@api_view(["POST"])
def signup_view(request):

    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):

    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })

