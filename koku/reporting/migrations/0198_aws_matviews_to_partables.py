# Generated by Django 3.1.13 on 2021-10-18 19:35
import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations
from django.db import models

from koku.database import set_pg_extended_mode
from koku.database import unset_pg_extended_mode


class Migration(migrations.Migration):

    dependencies = [("api", "0050_exchangerates"), ("reporting", "0197_usersettings")]

    operations = [
        migrations.RunPython(code=set_pg_extended_mode, reverse_code=unset_pg_extended_mode),
        migrations.CreateModel(
            name="AWSStorageSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_storage_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_storage_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSStorageSummaryByServiceP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_storage_summary_by_service_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_storage_summary_by_service_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSStorageSummaryByRegionP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("region", models.CharField(max_length=50, null=True)),
                ("availability_zone", models.CharField(max_length=50, null=True)),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_storage_summary_by_region_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_storage_summary_by_region_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSStorageSummaryByAccountP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_storage_summary_by_account_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_storage_summary_by_account_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSNetworkSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_network_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_network_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSDatabaseSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_database_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_database_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSCostSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_cost_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_cost_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSCostSummaryByServiceP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_cost_summary_by_service_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_cost_summary_by_service_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSCostSummaryByRegionP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("region", models.CharField(max_length=50, null=True)),
                ("availability_zone", models.CharField(max_length=50, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_cost_summary_by_region_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_cost_summary_by_region_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSCostSummaryByAccountP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_cost_summary_by_account_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_cost_summary_by_account_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSComputeSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("instance_type", models.CharField(max_length=50, null=True)),
                (
                    "resource_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=256), null=True, size=None
                    ),
                ),
                ("resource_count", models.IntegerField(null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_compute_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_compute_summary_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSComputeSummaryByServiceP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("instance_type", models.CharField(max_length=50, null=True)),
                (
                    "resource_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=256), null=True, size=None
                    ),
                ),
                ("resource_count", models.IntegerField(null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_compute_summary_by_service_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_compute_summary_by_service_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSComputeSummaryByRegionP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("region", models.CharField(max_length=50, null=True)),
                ("availability_zone", models.CharField(max_length=50, null=True)),
                ("instance_type", models.CharField(max_length=50, null=True)),
                (
                    "resource_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=256), null=True, size=None
                    ),
                ),
                ("resource_count", models.IntegerField(null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_compute_summary_by_region_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_compute_summary_by_region_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="AWSComputeSummaryByAccountP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("usage_account_id", models.CharField(max_length=50)),
                ("instance_type", models.CharField(max_length=50, null=True)),
                (
                    "resource_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=256), null=True, size=None
                    ),
                ),
                ("resource_count", models.IntegerField(null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("savingsplan_effective_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "organizational_unit",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="reporting.awsorganizationalunit"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="api.provider"),
                ),
            ],
            options={"db_table": "reporting_aws_compute_summary_by_account_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_aws_compute_summary_by_account_p ALTER COLUMN id SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.RunPython(code=unset_pg_extended_mode, reverse_code=set_pg_extended_mode),
    ]
