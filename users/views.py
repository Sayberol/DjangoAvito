from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from djangoProject1 import settings
from users.models import User
from users.serializers import LocationSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDeleteSerializer


class LocationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LocationSerializer


# class UserView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetailView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer


class UserView(ListView):
    models = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for user in self.object_list.annotate(ads=Count("ad", filter=Q(ad__is_published=True))):
            response.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "total_ads": user.ads,
                "locations": [loc.name for loc in user.locations.all()],
            })

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "total_ads": user.ads,
            "locations": [loc.name for loc in user.locations.all()],
        })
