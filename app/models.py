from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)


class ClientRequest(Log):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    description = models.TextField(null=True, blank=True, help_text="what is your image")
    variable_1 = models.SmallIntegerField()
    method = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    pass


class ModelResult(Log):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_request = models.OneToOneField(ClientRequest, on_delete=models.CASCADE)
    result = models.ImageField()

    def __str__(self):
        return self.client_request.image
    pass
