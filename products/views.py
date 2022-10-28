from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from .permissions import IsOwnerSeller, IsSellerOrReadOnly
from .models import Product

from .serializers import ProductSerializer, ProductDetailSerializer


class SerializerByMethodMixin:

    serializer_map = None

    def get_serializer_class(self):
        assert (
            self.serializer_map is not None
        ), f"'{self.__class__.__name__}' should include a `serializer_map` attribute"

        return self.serializer_map.get(self.request.method)


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductDetailSerializer

        return ProductSerializer


class ProductDetailView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerSeller]

    queryset = Product.objects.all()

    serializer_map = {
        "PATCH": ProductDetailSerializer,
    }

    lookup_url_kwarg = "pk"
