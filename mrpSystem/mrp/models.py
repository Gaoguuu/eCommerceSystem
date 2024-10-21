from django.db import models


# Create your models here.
class Material(models.Model):
    MatID = models.CharField(verbose_name="物料号", max_length=5, unique=True)
    MatName = models.CharField(verbose_name="名称", max_length=20)
    MatUni = models.CharField(verbose_name="单位", max_length=4)
    MatPro = models.CharField(verbose_name="调配方式", max_length=10)
    MatLos = models.FloatField(verbose_name="损耗率")
    MatPre = models.FloatField(verbose_name="提前期")


class Store(models.Model):
    MatID = models.CharField(verbose_name="物料号", max_length=5, unique=True)
    MatName = models.CharField(verbose_name="名称", max_length=20)
    MatRem = models.IntegerField(verbose_name="工厂库存")
    MatPre = models.IntegerField(verbose_name="资料库存")


class BOM(models.Model):
    MatID = models.CharField(verbose_name="物料号", max_length=5)
    MatName = models.CharField(verbose_name="名称", max_length=20)
    MatNeed = models.IntegerField(verbose_name="装配数量")
    MatUni = models.CharField(verbose_name="单位", max_length=4)
    MatCen = models.CharField(verbose_name="层次", max_length=1)


class Allo(models.Model):
    AlloNum = models.CharField(verbose_name="调配基准编号", max_length=10)
    AlloID = models.CharField(verbose_name="调配配区代码", max_length=10)
    ParID = models.CharField(verbose_name="父物料号", max_length=20)
    ParName = models.CharField(verbose_name="父物料名称", max_length=20)
    ChiID = models.CharField(verbose_name="子物料号", max_length=20)
    ChiName = models.CharField(verbose_name="子物料名称", max_length=20)
    ConnNum = models.IntegerField(verbose_name="子物料数量")
    MatPre = models.IntegerField(verbose_name="物料提前期")
    ShoPre = models.IntegerField(verbose_name="供应商提前期")