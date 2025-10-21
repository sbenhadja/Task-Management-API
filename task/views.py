from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from task.models import Task
from task.serializers import TaskSerializer


# -----------------------------
# Pagination Personnalisée
# -----------------------------
class TaskPagination(PageNumberPagination):
    page_size = 5  # Nombre d'éléments par défaut
    page_size_query_param = "page_size"  # Permet de changer le nombre d'éléments via ?page_size=10
    max_page_size = 50  # Limite maximale

    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "message": "Tasks retrieved successfully",
            "pagination": {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "has_next": self.page.has_next(),
                "has_previous": self.page.has_previous(),
            },
            "data": data
        })


# -----------------------------
# Lister les tâches de l'utilisateur + création
# -----------------------------
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination

    def get_queryset(self):
        """
        Récupère les tâches de l'utilisateur connecté
        et applique les filtres passés en query params.
        Exemple : ?status=done&due_date=2025-09-04
        """
        user = self.request.user
        
        # Exclure les paramètres réservés de la pagination
        reserved_params = ["page", "page_size"]
        
        filters = {
            f"{key}__exact": value
            for key, value in self.request.query_params.items()
            if value and key not in reserved_params
        }
        return Task.objects.filter(user=user, **filters).order_by("due_date")

    def perform_create(self, serializer):
        """
        Ajoute automatiquement l'utilisateur connecté lors de la création.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "message": "Task created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# -----------------------------
# Récupérer, Mettre à jour, Supprimer une tâche
# -----------------------------
class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restreint l'accès aux tâches de l'utilisateur connecté.
        """
        return Task.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Task retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        """
        Supporte le PATCH (partiel) et le PUT (complet).
        """
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Task updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "status": "success",
            "message": "Task deleted successfully"
        }, status=status.HTTP_200_OK)
