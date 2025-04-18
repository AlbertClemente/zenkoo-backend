# Generated by Django 5.1.7 on 2025-04-17 16:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0035_alter_savinggoal_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('reserved_savings', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('reflection', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'month')},
            },
        ),
    ]
