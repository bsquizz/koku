# Generated by Django 2.2.11 on 2020-03-24 14:20
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("api", "0015_auto_20200311_2049")]

    operations = [
        migrations.AlterModelOptions(name="sources", options={"ordering": ["name"]}),
        migrations.RemoveField(model_name="provider", name="id"),
    ]
