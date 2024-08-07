# Generated by Django 4.1 on 2024-07-16 18:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Note",
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
                ("title", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="images/")),
                ("content", models.TextField()),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
