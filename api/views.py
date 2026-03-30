from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from rest_framework import mixins, permissions, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from structure.models import Specialist, Application
from .serializers import (UserSerializer, ApplicationSerializer,
                          SpecialistSerializer)

User = get_user_model()


class RedirectToSpecialistsView(View):
    def get(self, request):
        return redirect('specialist-list')


class SpecialistViewSet(
    viewsets.ReadOnlyModelViewSet
):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer

    @action(
        ['GET'],
        detail=True,
        url_path='session-link',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def session_link(self, request, pk):
        return redirect(
            f'{get_object_or_404(Specialist, pk=pk).link}'
        )


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        ['GET'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def session_link(self, request, pk):
        return redirect(
            f'{get_object_or_404(Specialist, pk=pk).link}'
        )


class ApplicationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    parser_classes = [MultiPartParser, FormParser]