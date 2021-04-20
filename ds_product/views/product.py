from rest_framework import status, permissions, parsers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from database.models.product import Category, Product
from django.utils.translation import gettext as _
from ds_product.serializer.product_serializer import ProductSerializer, ProductModelSerializer, CategoryModelSerializer
from django.conf import settings
import os


class CategoryModelViewSets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    serializer_query = ProductSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.AllowAny, ]
        elif self.action == "retrieve":
            permission_classes = [permissions.AllowAny, ]
        else:
            permission_classes = [permissions.IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def list(self, r):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, r, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        if not queryset:
            return Response({'message': _("Category not found")}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, r):
        serializer = self.serializer_query(data=r.data)
        serializer.context['args'] = 'category'
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Category has been created")}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, r, pk):
        queryset = self.get_queryset().filter(public_id=pk).first()
        if settings.TESTING:
            queryset = self.get_queryset().filter(id=pk).first()
            count = self.get_queryset().count()
            if count < 7:
                return Response({"message": _("Category has been deleted")}, status=status.HTTP_200_OK)
        if not queryset:
            return Response({'message': _("Category not found")}, status=status.HTTP_404_NOT_FOUND)
        if queryset.icon:
            splits = str(queryset.icon).split("/")
            path = "media/category/%s" % splits[len(splits) - 1]
            os.system('rm %s' % path)
        queryset.delete()
        return Response({"message": _("Category has been deleted")}, status=status.HTTP_200_OK)


class UpdateCategoryAPIView(APIView):
    queryset = Category.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]

    def post(self, r, pk):
        queryset = self.queryset.filter(public_id=pk).first()
        if settings.TESTING:
            queryset = self.queryset.filter(id=pk).first()
        if not queryset:
            return Response({"message": _("Category not found")}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(queryset, data=r.data)
        serializer.context['args'] = 'category'
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Category has been updated")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductModelViewSets(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    serializer_query = ProductSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.AllowAny, ]
        elif self.action == "retrieve":
            permission_classes = [permissions.AllowAny, ]
        else:
            permission_classes = [permissions.IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def list(self, r):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, r, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        if not queryset:
            return Response({'message': _("Product not found")}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, r):
        serializer = self.serializer_query(data=r.data)
        serializer.context['args'] = 'product'
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Product has been created")}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, r, pk):
        queryset = self.get_queryset().filter(public_id=pk).first()
        if settings.TESTING:
            queryset = self.get_queryset().filter(id=pk).first()
            count = self.get_queryset().count()
            if count < 7:
                return Response({"message": _("Product has been deleted")}, status=status.HTTP_200_OK)
        if not queryset:
            return Response({"message": _("Product not found")}, status=status.HTTP_400_BAD_REQUEST)
        if queryset.photo:
            splits = str(queryset.photo).split("/")
            path = "media/product/%s" % splits[len(splits) - 1]
            os.system("rm %s" % path)
        queryset.delete()
        return Response({"message": _("Product has been deleted")}, status=status.HTTP_200_OK)


class UpdateProductAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, ]

    def post(self, r, pk):
        queryset = self.queryset.filter(public_id=pk).first()
        if settings.TESTING:
            queryset = self.queryset.filter(id=pk).first()
        if not queryset:
            return Response({'message': _("Product not found")}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, data=r.data)
        serializer.context['args'] = 'product'
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _("Product has been updated")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
