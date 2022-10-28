from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status

from accounts.models import Account
from accounts.permissions import IsAdmin, IsOwnerSeller

from accounts.serializers import AccountSerializer, AccountUpdatedSerializer


class AccountsView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class LoginView(ObtainAuthToken):
    def post(self, request: Request) -> Response:

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        max_accounts = self.kwargs["num"]
        return self.queryset.order_by("date_joined")[0:max_accounts]


class AccountDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerSeller]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    queryset = Account.objects.all()
    serializer_class = AccountUpdatedSerializer
