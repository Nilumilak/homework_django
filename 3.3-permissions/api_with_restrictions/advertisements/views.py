from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError

from .filters import AdvertisementFilter
from .models import Advertisement, Favorites
from .serializers import AdvertisementSerializer, FavoritesSerializer
from .permissions import IsOwnerOrReadOnly

from django.core.exceptions import ObjectDoesNotExist


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    @action(methods=['get', 'post'], detail=False)
    def favorites(self, request):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({'error': 'You are not authorized'})

        if request.method == 'GET':
            favorites = Favorites.objects.filter(user=user)
            serializer = FavoritesSerializer(favorites, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            try:
                favorite = Advertisement.objects.get(pk=request.data.get('favorite_id'))
            except ObjectDoesNotExist:
                return Response({'error': 'Advertisement does not exist'})
            if favorite.creator == self.request.user:
                return Response({'error': 'you cannot add your advertisement to favorites'})
            else:
                try:
                    added_favorite = Favorites.objects.create(user=self.request.user,
                                                              favorite_id=favorite)
                    serializer = FavoritesSerializer([added_favorite], many=True)
                    return Response(serializer.data)
                except IntegrityError:
                    return Response({'error': 'Advertisement is already added'})
