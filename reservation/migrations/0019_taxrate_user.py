# Generated by Django 4.2.2 on 2023-10-04 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0018_reservation_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxrate',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taxrates', to=settings.AUTH_USER_MODEL),
        ),
    ]
