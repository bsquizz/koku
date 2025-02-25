# Generated by Django 3.1.13 on 2021-12-01 13:00
import django.db.models.deletion
from django.db import migrations
from django.db import models

from koku.database import set_pg_extended_mode
from koku.database import unset_pg_extended_mode


class Migration(migrations.Migration):

    dependencies = [("api", "0050_exchangerates"), ("reporting", "0210_ocpaws_partables")]

    operations = [
        migrations.RunPython(code=set_pg_extended_mode, reverse_code=unset_pg_extended_mode),
        migrations.CreateModel(
            name="OCPAzureStorageSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("subscription_guid", models.TextField()),
                ("service_name", models.TextField(null=True)),
                ("usage_quantity", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("unit_of_measure", models.TextField(null=True)),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_storage_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_storage_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPAzureNetworkSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("subscription_guid", models.TextField()),
                ("service_name", models.TextField(null=True)),
                ("usage_quantity", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("unit_of_measure", models.TextField(null=True)),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_network_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_network_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPAzureDatabaseSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("subscription_guid", models.TextField()),
                ("service_name", models.TextField(null=True)),
                ("usage_quantity", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("unit_of_measure", models.TextField(null=True)),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_database_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_database_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPAzureCostSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_cost_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_cost_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPAzureCostSummaryByServiceP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("subscription_guid", models.TextField()),
                ("service_name", models.TextField(null=True)),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_cost_summary_by_service_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_cost_summary_by_service_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPAzureCostSummaryByLocationP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("subscription_guid", models.TextField()),
                ("resource_location", models.TextField(null=True)),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_cost_summary_by_location_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_cost_summary_by_location_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPAzureCostSummaryByAccountP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("subscription_guid", models.TextField()),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_cost_summary_by_account_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_cost_summary_by_account_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPAzureComputeSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("subscription_guid", models.TextField()),
                ("instance_type", models.TextField(null=True)),
                ("resource_id", models.CharField(max_length=253, null=True)),
                ("usage_quantity", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("unit_of_measure", models.TextField(null=True)),
                ("pretax_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=33, null=True)),
                ("currency", models.TextField(null=True)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpazure_compute_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpazure_compute_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.AddIndex(
            model_name="ocpazurestoragesummaryp",
            index=models.Index(fields=["usage_start"], name="ocpazstorsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpazurestoragesummaryp",
            index=models.Index(fields=["service_name"], name="ocpazstorsumm_svc_name"),
        ),
        migrations.AddIndex(
            model_name="ocpazurestoragesummaryp",
            index=models.Index(fields=["cluster_id"], name="ocpazstorsumm_clust_id"),
        ),
        migrations.AddIndex(
            model_name="ocpazurenetworksummaryp",
            index=models.Index(fields=["usage_start"], name="ocpaznetsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpazurenetworksummaryp",
            index=models.Index(fields=["service_name"], name="ocpaznetsumm_svc_name"),
        ),
        migrations.AddIndex(
            model_name="ocpazurenetworksummaryp",
            index=models.Index(fields=["cluster_id"], name="ocpaznetsumm_clust_id"),
        ),
        migrations.AddIndex(
            model_name="ocpazuredatabasesummaryp",
            index=models.Index(fields=["usage_start"], name="ocpazdbsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpazuredatabasesummaryp",
            index=models.Index(fields=["service_name"], name="ocpazdbsumm_svc_name"),
        ),
        migrations.AddIndex(
            model_name="ocpazuredatabasesummaryp",
            index=models.Index(fields=["cluster_id"], name="ocpazdbsumm_clust_id"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummaryp", index=models.Index(fields=["cluster_id"], name="ocpazcostsumm_clust_id")
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybyservicep",
            index=models.Index(fields=["usage_start"], name="ocpazcostsumm_svc_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybyservicep",
            index=models.Index(fields=["service_name"], name="ocpazcostsumm_svc_svc_name"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybyservicep",
            index=models.Index(fields=["cluster_id"], name="ocpazcostsumm_svc_clust_id"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybylocationp",
            index=models.Index(fields=["usage_start"], name="ocpazcostsumm_loc_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybylocationp",
            index=models.Index(fields=["resource_location"], name="ocpazcostsumm_loc_res_loc"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybylocationp",
            index=models.Index(fields=["cluster_id"], name="ocpazcostsumm_loc_clust_id"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybyaccountp",
            index=models.Index(fields=["usage_start"], name="ocpazcostsumm_acc_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybyaccountp",
            index=models.Index(fields=["subscription_guid"], name="ocpazcostsumm_acc_sub_guid"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecostsummarybyaccountp",
            index=models.Index(fields=["cluster_id"], name="ocpazcostsumm_acc_clust_id"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecomputesummaryp",
            index=models.Index(fields=["usage_start"], name="ocpazcompsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecomputesummaryp",
            index=models.Index(fields=["instance_type"], name="ocpazcompsumm_insttyp"),
        ),
        migrations.AddIndex(
            model_name="ocpazurecomputesummaryp",
            index=models.Index(fields=["cluster_id"], name="ocpazcompsumm_clust_id"),
        ),
        migrations.RunPython(code=unset_pg_extended_mode, reverse_code=set_pg_extended_mode),
    ]
