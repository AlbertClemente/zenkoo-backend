# Generated by Django 5.1.7 on 2025-04-09 22:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0025_alter_income_id_alter_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='id',
            field=models.UUIDField(default=uuid.UUID('be166598-e390-48a7-b425-60cc155a52c9'), editable=False, primary_key=True, serialize=False),
        ),
    ]
