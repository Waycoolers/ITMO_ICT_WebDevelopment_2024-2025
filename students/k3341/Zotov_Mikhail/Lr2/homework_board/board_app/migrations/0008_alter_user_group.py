# Generated by Django 5.1.2 on 2024-12-03 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0007_alter_user_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='board_app.group'),
            preserve_default=False,
        ),
    ]
