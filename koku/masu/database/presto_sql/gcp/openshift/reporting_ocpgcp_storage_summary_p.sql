-- Clear out old entries first
DELETE FROM postgres.{{schema | sqlsafe}}.reporting_ocpgcp_storage_summary_p
WHERE usage_start >= date('{{start_date | sqlsafe}}')
    AND usage_start <= date('{{end_date | sqlsafe}}')
    AND invoice_month = '{{year | sqlsafe}}{{month | sqlsafe}}'
    AND report_period_id = {{report_period_id | sqlsafe}}
;

-- Populate the daily aggregate line item data
INSERT INTO postgres.{{schema | sqlsafe}}.reporting_ocpgcp_storage_summary_p (
    uuid,
    report_period_id,
    cluster_id,
    cluster_alias,
    node,
    usage_start,
    usage_end,
    account_id,
    service_id,
    service_alias,
    unblended_cost,
    markup_cost,
    currency,
    source_uuid,
    credit_amount,
    invoice_month
)
    SELECT uuid(),
        report_period_id,
        cluster_id,
        cluster_alias,
        node,
        usage_start,
        usage_end,
        account_id
        service_id,
        service_alias,
        sum(unblended_cost) as unblended_cost,
        sum(markup_cost) as markup_cost,
        max(currency) as currency,
        source_uuid,
        sum(credit_amount) as credit_amount,
        invoice_month
    FROM postgres.{{schema | sqlsafe}}.reporting_ocpgcpcostlineitem_daily_summary
    -- Get data for this month or last month
    WHERE usage_start >= date('{{start_date | sqlsafe}}')
        AND usage_start <= date('{{end_date | sqlsafe}}')
        AND service_alias IN ('Filestore', 'Storage', 'Cloud Storage', 'Data Transfer')
        AND invoice_month = '{{year | sqlsafe}}{{month | sqlsafe}}'
    GROUP BY report_period_id,
        cluster_id,
        cluster_alias,
        node,
        usage_start,
        usage_end,
        account_id,
        service_id,
        service_alias,
        source_uuid,
        invoice_month
;
