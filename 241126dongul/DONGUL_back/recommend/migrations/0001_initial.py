# Generated by Django 4.2.7 on 2024-11-22 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepositProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bank', models.CharField(max_length=100)),
                ('interest_rate', models.FloatField()),
                ('term', models.IntegerField(help_text='기간(개월)')),
            ],
        ),
        migrations.CreateModel(
            name='SavingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bank', models.CharField(max_length=100)),
                ('interest_rate', models.FloatField()),
                ('term', models.IntegerField(help_text='기간(개월)')),
            ],
        ),
    ]