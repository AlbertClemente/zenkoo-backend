# Generated by Django 5.1.7 on 2025-04-08 22:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0009_alter_income_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='id',
            field=models.UUIDField(default=uuid.UUID('88df80a7-4d3d-4747-9e5f-63f5d792314d'), editable=False, primary_key=True, serialize=False),
        ),
    ]
