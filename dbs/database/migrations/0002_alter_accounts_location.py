# Generated by Django 3.2 on 2021-04-19 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.location'),
        ),
    ]
