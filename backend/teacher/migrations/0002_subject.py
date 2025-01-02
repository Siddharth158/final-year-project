# Generated by Django 5.0.7 on 2024-12-29 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teacher", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
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
                ("subject_code", models.CharField(max_length=20, unique=True)),
                ("subject_name", models.CharField(max_length=100)),
                ("semester", models.PositiveIntegerField()),
                ("is_active", models.BooleanField(default=False)),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subjects",
                        to="teacher.teacher",
                    ),
                ),
            ],
        ),
    ]