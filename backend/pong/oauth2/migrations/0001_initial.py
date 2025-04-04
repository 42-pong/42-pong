# Generated by Django 5.1.4 on 2025-01-03 14:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OAuth2",
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
                ("provider", models.CharField(max_length=255)),
                ("provider_id", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="oauth2",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "oauth2",
            },
        ),
        migrations.CreateModel(
            name="FortyTwoToken",
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
                (
                    "access_token",
                    models.CharField(max_length=255, unique=True),
                ),
                ("token_type", models.CharField(max_length=255)),
                ("access_token_expiry", models.DateTimeField()),
                (
                    "refresh_token",
                    models.CharField(max_length=255, unique=True),
                ),
                ("refresh_token_expiry", models.DateTimeField()),
                ("scope", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "oauth2",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="forty_two_token",
                        to="oauth2.oauth2",
                    ),
                ),
            ],
            options={
                "db_table": "forty_two_tokens",
            },
        ),
    ]
