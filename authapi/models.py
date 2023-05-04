from django.db import models
from django.contrib.auth.models import User

class MobileNumber(models.Model):
    user=models.OneToOneField(User,related_name='number',on_delete=models.CASCADE,null=True,blank=True,default=None)
    country_code=models.IntegerField(null=False,blank=False)
    number=models.BigIntegerField(unique=True, null=False,blank=False)
    is_verified=models.BooleanField(null=False,default=False)
    counter = models.IntegerField(default=0,null=False)

    def __str__(self) -> str:
        return f'{self.country_code} {self.number}'
