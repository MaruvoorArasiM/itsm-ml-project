# DAX measures: ITSM Service Desk dashboard

The twelve measures used in `ITSM_Service_Desk_Dashboard.pbix`. Each table comes from a CSV in this folder (see `10_powerbi_export`). The tables are loaded separately with no relationships, so each page uses one table.

## Tickets (`ticket_summary`)

| Measure | DAX | Used for |
|---|---|---|
| Total Tickets | `SUM(ticket_summary[Tickets])` | Ticket counts on the Overview page |
| High Tickets | `CALCULATE([Total Tickets], ticket_summary[Priority_Group] = "High (P1-P2)")` | Critical (P1/P2) tickets; the weekday-by-hour heatmap |
| Labelled Tickets | `CALCULATE([Total Tickets], ticket_summary[Priority_Group] <> "Unlabelled")` | Denominator for High Rate (1,230 tickets have no priority) |
| High Rate | `DIVIDE([High Tickets], [Labelled Tickets])` | Critical-ticket rate overall (1.6%) and by asset type |
| Reassignment Rate | `DIVIDE(SUM(ticket_summary[Reassigned_Tickets]), [Total Tickets])` | Share of tickets reassigned at least once (40.7%) |

## Model alerts (`alert_outcomes`, test period 1 Feb to 16 Mar 2014)

| Measure | DAX | Used for |
|---|---|---|
| Caught | `CALCULATE(SUM(alert_outcomes[Tickets]), alert_outcomes[Outcome] = "Caught")` | Critical tickets the model flagged (67) |
| Missed | `CALCULATE(SUM(alert_outcomes[Tickets]), alert_outcomes[Outcome] = "Missed")` | Critical tickets not flagged (48) |
| False Alarms | `CALCULATE(SUM(alert_outcomes[Tickets]), alert_outcomes[Outcome] = "False alarm")` | Flagged tickets that were not critical (158) |
| Recall | `DIVIDE([Caught], [Caught] + [Missed])` | Share of critical tickets caught (58.3%) |
| Alerts per Day | `DIVIDE([Caught] + [False Alarms], DISTINCTCOUNT(alert_outcomes[Date]))` | Alert workload: 225 alerts over 43 days with tickets (5.2) |

## Forecast (`annual_forecast`)

| Measure | DAX | Used for |
|---|---|---|
| Annual Incidents Forecast | `CALCULATE(SUM(annual_forecast[Forecast]), annual_forecast[Series] = "Incidents")` | Incidents expected, April 2014 to March 2015 (75,164) |
| Annual Tickets Forecast | `CALCULATE(SUM(annual_forecast[Forecast]), annual_forecast[Series] = "All tickets")` | All tickets expected over the same 12 months (93,115) |

## Notes

- `CALCULATE` evaluates a measure under an added filter; `DIVIDE` returns blank instead of an error when the denominator is zero.
- The data is aggregated in Python before it reaches Power BI, so `SUM` is enough; no row-by-row functions (`SUMX`) or time-intelligence functions are needed.
- Rates by asset type use a Top N visual filter (the 6 largest asset types), so that types with only a few tickets do not show misleading 50% or 100% rates.
