# Generated by Django 5.1.2 on 2024-10-31 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mrp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("OrderNum", models.CharField(max_length=10, verbose_name="订单编号")),
                ("GoodsNum", models.CharField(max_length=10, verbose_name="货品编号")),
                ("userId", models.CharField(max_length=30, verbose_name="用户ID")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("GoodsNum", models.CharField(max_length=10, verbose_name="货品编号")),
                ("img", models.CharField(max_length=255)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("intro", models.TextField()),
                ("remarks", models.IntegerField()),
                ("shop_name", models.CharField(max_length=100)),
                ("sale", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("userId", models.CharField(max_length=30)),
                ("username", models.CharField(max_length=30)),
            ],
        ),
    ]
