# Generated by Django 4.2 on 2023-06-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("financial_report", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailyreport",
            name="amount",
            field=models.BigIntegerField(default=0, verbose_name="Amount"),
        ),
        migrations.AlterField(
            model_name="weeklyreport",
            name="amount",
            field=models.BigIntegerField(default=0, verbose_name="Amount"),
        ),
    ]
