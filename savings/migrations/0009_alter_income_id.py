# Generated by Django 5.1.7 on 2025-04-08 22:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0008_alter_income_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e39b7b6d-a932-4d13-ad04-9a7363463118'), editable=False, primary_key=True, serialize=False),
        ),
    ]
