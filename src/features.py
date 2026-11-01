asset_cols = ["CI_Cat", "CI_Subcat", "WBS", "Category"]
ci_name    = ["CI_Name"]
time_feats = ["hour", "weekday"]
matrix_cols = ["Impact", "Urgency"]

post_event = ["Status", "Resolved_Time", "Close_Time", "Reopen_Time", "Has_Reopen_Time",
              "Handle_Time_hrs", "Elapsed_hrs", "Closure_Code"]
unsure_timing = ["No_of_Reassignments", "No_of_Related_Interactions", "No_of_Related_Incidents",
                 "No_of_Related_Changes", "Has_Related_Change", "KB_number"]
identifiers = ["Incident_ID", "Related_Interaction", "Related_Change"]

set_a = asset_cols + time_feats + matrix_cols   # includes Impact and Urgency
set_b = asset_cols + time_feats                 # the honest test
