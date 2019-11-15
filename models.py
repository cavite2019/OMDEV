from django.db import models
import datetime

# Create your models here.
class SSRinitModel(models.Model):
    IP = models.CharField(max_length=16,null=True)
    PORT = models.IntegerField(null=True)
    USER = models.CharField(max_length=15, null=True)
    PASSWORD = models.CharField(max_length=50, null=True)
    IDC = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.IP


class SSRIDCModel(models.Model):
    IDC = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.IDC


class SSRinitdataModel(models.Model):
    USERNAME = models.CharField(max_length=50,null=True)
    IP = models.CharField(max_length=16,null=True)
    PORT = models.IntegerField(null=True)
    STATUS = models.CharField(max_length=10, null=True)
    SSR_LINK = models.TextField(null=True)
    SSR_CODE = models.TextField(null=True)
    LOGS = models.TextField(null=True)
    IDC = models.CharField(max_length=20, null=True)
    CREATED = models.DateTimeField(default=datetime.datetime.now(), null=True)
    def __str__(self):
        return self.IP