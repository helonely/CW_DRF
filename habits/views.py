from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


@method_decorator(
    name="list", decorator=swagger_auto_schema(operation_description="cписок привычек")
)
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ("action",)
    ordering_fields = ("time",)

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny]
        elif self.action == "create":
            return [IsAuthenticated]
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            # Разрешаем доступ только к собственным привычкам для чтения, редактирования,
            # частичного редактирования и удаления
            return [IsAuthenticated, IsOwner]

        return super().get_permissions()

    def get_queryset(self):
        if self.action == "list" and not self.request.user.is_authenticated:
            # Если пользователь не авторизован, показываем только публичные привычки
            return Habit.objects.filter(is_public=True).order_by("id")
        else:
            # Если пользователь авторизован, показываем его привычки и публичные привычки
            return Habit.objects.filter(user=self.request.user).order_by("id")


class PublicHabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = HabitPaginator
