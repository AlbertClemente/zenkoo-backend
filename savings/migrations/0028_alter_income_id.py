# Generated by Django 5.1.7 on 2025-04-10 18:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0027_alter_income_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b32f0039-6788-4183-99ef-ec2875109617'), editable=False, primary_key=True, serialize=False),
        ),
    ]
