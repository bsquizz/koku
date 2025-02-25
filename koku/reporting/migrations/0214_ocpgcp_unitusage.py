# Generated by Django 3.1.14 on 2022-01-12 17:19
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("reporting", "0213_delete_mat_views")]

    operations = [
        migrations.AddField(
            model_name="ocpgcpcomputesummaryp", name="unit", field=models.CharField(max_length=63, null=True)
        ),
        migrations.AddField(
            model_name="ocpgcpcomputesummaryp",
            name="usage_amount",
            field=models.DecimalField(decimal_places=9, max_digits=24, null=True),
        ),
        migrations.AddField(
            model_name="ocpgcpdatabasesummaryp", name="unit", field=models.CharField(max_length=63, null=True)
        ),
        migrations.AddField(
            model_name="ocpgcpdatabasesummaryp",
            name="usage_amount",
            field=models.DecimalField(decimal_places=9, max_digits=24, null=True),
        ),
        migrations.AddField(
            model_name="ocpgcpnetworksummaryp", name="unit", field=models.CharField(max_length=63, null=True)
        ),
        migrations.AddField(
            model_name="ocpgcpnetworksummaryp",
            name="usage_amount",
            field=models.DecimalField(decimal_places=9, max_digits=24, null=True),
        ),
        migrations.AddField(
            model_name="ocpgcpstoragesummaryp", name="unit", field=models.CharField(max_length=63, null=True)
        ),
        migrations.AddField(
            model_name="ocpgcpstoragesummaryp",
            name="usage_amount",
            field=models.DecimalField(decimal_places=9, max_digits=24, null=True),
        ),
    ]
