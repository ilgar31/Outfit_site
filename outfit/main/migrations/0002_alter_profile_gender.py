# Generated by Django 4.1.5 on 2023-07-10 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1),
        ),
    ]
