# Generated by Django 5.1.7 on 2025-03-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='graduation_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
