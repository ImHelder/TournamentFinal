# Generated by Django 5.0.4 on 2024-04-05 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0010_match_roundnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='secondParticipant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondParticipant', to='Site.participant'),
        ),
    ]