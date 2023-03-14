from asyncio.windows_events import NULL
from pyexpat import model
from re import T
from statistics import mode
from django.db import models
# Create your models here.

class process(models.Model):
    pID = models.IntegerField(unique=True)
    aT = models.IntegerField()
    bT = models.IntegerField()
    def __str__(self):
        return {self.pID, self.aT, self.bT}

class cal_process(models.Model):
    cT = models.IntegerField()
    tAT = models.IntegerField()
    wT = models.IntegerField()
    rt = models.IntegerField(null=True)
    def __str__(self) -> str:
        return super().__str__()

class all_process(models.Model):
    t_p = models.IntegerField()
    def __str__(self) -> str:
        return super().__str__()
    
class avg_times(models.Model):
    avg_proc_wt = models.FloatField()
    avg_proc_tat = models.FloatField()
    # def __str__(self):
    #     return str(self.ProductName) if self.ProductName else ''

# class time_quantum(models.Model):
#     tq = models.IntegerField(null=True)
#     def __str__(self) -> str:
#         return super().__str__()