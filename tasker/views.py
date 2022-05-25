from django.shortcuts import render
from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.core.mail import send_mail
from . import models
from . import serializers
from bilim import tasks

class TaskView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """
    User creation view
    """
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(
        detail=False,
        methods=["delete"],
        name="Execute task",
        url_path=r'(?P<id>\d+)/delete',
        url_name="deletes-task"
    )
    def delete(self, request, id):
        try:
            task = models.Task.objects.filter(id=id).delete()
            # tasks.send_beat_email.delay(request.user.email)
            return Response({"detail": "Task has deleted"}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=406)

    @action(
        detail=False,
        methods=["get"],
        name="Execute task",
        url_path=r'(?P<id>\d+)/execute',
        url_name="executes-task"
    )
    def execute_task(self, request, id):
        try:
            task = models.Task.objects.filter(id=id).first()
            if task and task.status == False:      
                task = models.Task.objects.filter(id=id).update(status=True)
                return Response({"detail": "Task has done"}, status=200)
            elif task and task.status == True:
                task = models.Task.objects.filter(id=id).update(status=False)
                return Response({"detail": "Task has not done"}, status=200)
            # tasks.send_beat_email.delay(request.user.email)

        except Exception as e:
            return Response({"detail": str(e)}, status=406)