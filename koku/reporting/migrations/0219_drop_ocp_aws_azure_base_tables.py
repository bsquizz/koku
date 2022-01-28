# Generated by Django 3.2.11 on 2022-01-28 19:42
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("reporting", "0218_rm_unused_gcp_partables")]

    operations = [
        migrations.RemoveField(model_name="ocpawscostlineitemprojectdailysummary", name="account_alias"),
        migrations.RemoveField(model_name="ocpawscostlineitemprojectdailysummary", name="cost_entry_bill"),
        migrations.RemoveField(model_name="ocpawscostlineitemprojectdailysummary", name="report_period"),
        migrations.RemoveField(model_name="ocpazurecostlineitemdailysummary", name="cost_entry_bill"),
        migrations.RemoveField(model_name="ocpazurecostlineitemdailysummary", name="report_period"),
        migrations.RemoveField(model_name="ocpazurecostlineitemprojectdailysummary", name="cost_entry_bill"),
        migrations.RemoveField(model_name="ocpazurecostlineitemprojectdailysummary", name="report_period"),
        migrations.DeleteModel(name="OCPAWSCostLineItemDailySummary"),
        migrations.DeleteModel(name="OCPAWSCostLineItemProjectDailySummary"),
        migrations.DeleteModel(name="OCPAzureCostLineItemDailySummary"),
        migrations.DeleteModel(name="OCPAzureCostLineItemProjectDailySummary"),
    ]
