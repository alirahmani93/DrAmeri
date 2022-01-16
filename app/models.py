from django.db import models

from .utils import input_path, coutput_path, moutput_path, cmoutput_path


# Create your models here.


class Log(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)


class Input(Log):
    image = models.ImageField(upload_to=input_path, )
    variable_1 = models.SmallIntegerField(verbose_name="Min Value", help_text="بزرگتر از 50")
    variable_2 = models.SmallIntegerField(verbose_name="Max Value", help_text="کوچکتر از 500")

    def __str__(self):
        return str(self.id)


class Output(Log):
    input_ids = models.ForeignKey(to=Input, related_name='input', on_delete=models.CASCADE)
    Cimage = models.ImageField(upload_to=coutput_path, )
    Mimage = models.ImageField(upload_to=moutput_path, )
    CMimage = models.ImageField(upload_to=cmoutput_path, )

    def __str__(self):
        return str(self.id)
