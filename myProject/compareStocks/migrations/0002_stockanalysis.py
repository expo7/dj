# Generated by Django 5.1.1 on 2024-10-09 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compareStocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker1', models.CharField(max_length=10)),
                ('ticker2', models.CharField(max_length=10)),
                ('analysis', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
