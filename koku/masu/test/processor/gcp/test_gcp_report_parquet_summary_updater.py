#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""Test the GCPReportParquetSummaryUpdater."""
from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from tenant_schemas.utils import schema_context

from api.utils import DateHelper
from masu.database.cost_model_db_accessor import CostModelDBAccessor
from masu.database.gcp_report_db_accessor import GCPReportDBAccessor
from masu.database.report_manifest_db_accessor import ReportManifestDBAccessor
from masu.processor.gcp.gcp_report_parquet_summary_updater import GCPReportParquetSummaryUpdater
from masu.test import MasuTestCase
from masu.util.common import date_range_pair


class GCPReportParquetSummaryUpdaterTest(MasuTestCase):
    """Test cases for the GCPReportParquetSummaryUpdater."""

    def setUp(self):
        """Setup up shared variables."""
        super().setUp()
        self.dh = DateHelper()
        manifest_id = 1
        with ReportManifestDBAccessor() as manifest_accessor:
            self.manifest = manifest_accessor.get_manifest_by_id(manifest_id)
        self.updater = GCPReportParquetSummaryUpdater(self.schema_name, self.gcp_provider, self.manifest)

    def test_get_sql_inputs(self):
        """Test that dates are returned."""
        # Previous month
        start_str = (self.dh.last_month_end - timedelta(days=3)).isoformat()
        end_str = self.dh.last_month_end.isoformat()
        start, end = self.updater._get_sql_inputs(start_str, end_str)
        self.assertEqual(start, self.dh.last_month_start.date())
        self.assertEqual(end, self.dh.last_month_end.date())

        # Current month
        with ReportManifestDBAccessor() as manifest_accessor:
            manifest = manifest_accessor.get_manifest_by_id(2)
        updater = GCPReportParquetSummaryUpdater(self.schema_name, self.gcp_provider, manifest)
        start_str = self.dh.this_month_start.isoformat()
        end_str = self.dh.this_month_end.isoformat()
        start, end = updater._get_sql_inputs(start_str, end_str)
        self.assertEqual(start, self.dh.this_month_start.date())
        self.assertEqual(end, self.dh.this_month_end.date())

        # No manifest
        updater = GCPReportParquetSummaryUpdater(self.schema_name, self.gcp_provider, None)
        start_date = self.dh.last_month_end - timedelta(days=3)
        start_str = start_date.isoformat()
        end_str = self.dh.last_month_end.isoformat()
        start, end = updater._get_sql_inputs(start_str, end_str)
        self.assertEqual(start, start_date.date())
        self.assertEqual(end, self.dh.last_month_end.date())

    def test_update_daily_tables(self):
        """Test that this is a placeholder method."""
        start_str = self.dh.this_month_start.isoformat()
        end_str = self.dh.this_month_end.isoformat()
        expected_start, expected_end = self.updater._get_sql_inputs(start_str, end_str)

        expected_log = (
            "INFO:masu.processor.gcp.gcp_report_parquet_summary_updater:"
            f"update_daily_tables for: {expected_start}-{expected_end}"
        )

        with self.assertLogs("masu.processor.gcp.gcp_report_parquet_summary_updater", level="INFO") as logger:
            start, end = self.updater.update_daily_tables(start_str, end_str)
            self.assertIn(expected_log, logger.output)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @patch(
        "masu.processor.gcp.gcp_report_parquet_summary_updater.GCPReportDBAccessor.populate_gcp_topology_information_tables"  # noqa: E501
    )
    @patch(
        "masu.processor.gcp.gcp_report_parquet_summary_updater.GCPReportDBAccessor.delete_line_item_daily_summary_entries_for_date_range"  # noqa: E501
    )
    @patch(
        "masu.processor.gcp.gcp_report_parquet_summary_updater.GCPReportDBAccessor.update_line_item_daily_summary_with_enabled_tags"  # noqa: E501
    )
    @patch("masu.processor.gcp.gcp_report_parquet_summary_updater.GCPReportDBAccessor.populate_tags_summary_table")
    @patch(
        "masu.processor.gcp.gcp_report_parquet_summary_updater.GCPReportDBAccessor.populate_line_item_daily_summary_table_presto"  # noqa: E501
    )
    def test_update_daily_summary_tables(
        self, mock_presto, mock_tag_update, mock_summary_update, mock_delete, mock_topo
    ):
        """Test that we run Presto summary."""
        start_str = self.dh.this_month_start.isoformat()
        end_str = self.dh.this_month_end.isoformat()
        start, end = self.updater._get_sql_inputs(start_str, end_str)

        for s, e in date_range_pair(start, end, step=settings.TRINO_DATE_STEP):
            expected_start, expected_end = s, e

        with GCPReportDBAccessor(self.schema) as accessor:
            with schema_context(self.schema):
                bills = accessor.bills_for_provider_uuid(self.gcp_provider.uuid, start)
                bill_ids = [str(bill.id) for bill in bills]
                current_bill_id = bills.first().id if bills else None

        with CostModelDBAccessor(self.schema, self.gcp_provider.uuid) as cost_model_accessor:
            markup = cost_model_accessor.markup
            markup_value = float(markup.get("value", 0)) / 100

        start_return, end_return = self.updater.update_summary_tables(start, end)
        mock_delete.assert_called_with(self.gcp_provider.uuid, expected_start, expected_end)
        mock_presto.assert_called_with(
            expected_start, expected_end, self.gcp_provider.uuid, current_bill_id, markup_value
        )
        mock_tag_update.assert_called_with(bill_ids, start, end)
        mock_summary_update.assert_called_with(start, end, bill_ids)

        self.assertEqual(start_return, start)
        self.assertEqual(end_return, end)
