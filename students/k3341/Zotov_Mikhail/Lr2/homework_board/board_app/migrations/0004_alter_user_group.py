# Generated by Django 5.1.2 on 2024-11-30 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0003_groupteacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=10, null=True),
        ),
    ]