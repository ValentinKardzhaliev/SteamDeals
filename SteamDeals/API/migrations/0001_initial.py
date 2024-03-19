# Generated by Django 5.0.3 on 2024-03-19 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=200)),
                ('discount_percent', models.IntegerField(default=0)),
                ('final_formatted_price', models.CharField(blank=True, max_length=10, null=True)),
                ('initial_formatted_price', models.CharField(max_length=20)),
                ('image_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]