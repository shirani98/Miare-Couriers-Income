# Generated by Django 3.2 on 2023-02-04 09:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.SmallIntegerField(choices=[(1, 'TRIP'), (2, 'INCREASE'), (3, 'DECREASE')], verbose_name='Transaction Type')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Amount')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('description', models.JSONField(blank=True, null=True, verbose_name='Description')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='transaction.courier')),
            ],
        ),
    ]
