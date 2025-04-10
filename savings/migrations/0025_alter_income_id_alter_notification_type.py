# Generated by Django 5.1.7 on 2025-04-09 22:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0024_notification_type_alter_income_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ef2f37f2-d0f7-4e84-aee1-81d10755f622'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('general', 'General'), ('cripto', 'Criptomoneda')], default='general', max_length=50),
        ),
    ]
