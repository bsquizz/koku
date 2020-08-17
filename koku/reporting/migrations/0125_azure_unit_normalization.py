# Generated by Django 2.2.12 on 2020-07-23 15:38
import pkgutil

from django.db import connection
from django.db import migrations


def add_views(apps, schema_editor):
    """Create database VIEWS from files."""
    view_sql = pkgutil.get_data("reporting.provider.azure", f"sql/views/reporting_azure_storage_summary.sql")
    view_sql = view_sql.decode("utf-8")
    with connection.cursor() as cursor:
        cursor.execute(view_sql)

    view_sql = pkgutil.get_data("reporting.provider.azure", f"sql/views/reporting_azure_compute_summary.sql")
    view_sql = view_sql.decode("utf-8")
    with connection.cursor() as cursor:
        cursor.execute(view_sql)


class Migration(migrations.Migration):

    dependencies = [("reporting", "0124_auto_20200806_1943")]

    operations = [
        migrations.RunSQL(
            """
                WITH cte_split_units AS (
                    SELECT li.id,
                        m.currency,
                        CASE WHEN split_part(m.unit_of_measure, ' ', 2) != '' AND NOT (m.unit_of_measure = '100 Hours' AND m.meter_category='Virtual Machines')
                            THEN  split_part(m.unit_of_measure, ' ', 1)::integer
                            ELSE 1::integer
                            END as multiplier,
                        CASE
                            WHEN split_part(m.unit_of_measure, ' ', 2) = 'Hours'
                                THEN  'Hrs'
                            WHEN split_part(m.unit_of_measure, ' ', 2) = 'GB/Month'
                                THEN  'GB-Mo'
                            WHEN split_part(m.unit_of_measure, ' ', 2) != ''
                                THEN  split_part(m.unit_of_measure, ' ', 2)
                            ELSE m.unit_of_measure
                        END as unit_of_measure
                        -- split_part(m.unit_of_measure, ' ', 2) as unit
                    FROM reporting_azurecostentrylineitem_daily AS li
                    JOIN reporting_azuremeter AS m
                        ON li.meter_id = m.id
                )
                UPDATE reporting_azurecostentrylineitem_daily_summary AS li
                SET usage_quantity = li.usage_quantity * su.multiplier,
                    unit_of_measure = su.unit_of_measure
                FROM cte_split_units AS su
                WHERE li.id = su.id
                ;
            """
        ),
        migrations.RunSQL(
            """
            DROP INDEX IF EXISTS azure_storage_summary;
            DROP MATERIALIZED VIEW IF EXISTS reporting_azure_storage_summary;
            """
        ),
        migrations.RunPython(add_views),
    ]
