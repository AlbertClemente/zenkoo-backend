# Generated by Django 5.1.7 on 2025-04-14 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0034_savinggoal_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savinggoal',
            name='status',
            field=models.CharField(choices=[('active', 'Activa'), ('paused', 'Pausada'), ('completed', 'Completada')], max_length=12),
        ),
    ]
