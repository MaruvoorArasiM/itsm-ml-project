id_cols       = ["Incident_ID", "KB_number", "Related_Interaction", "Related_Change"]
cat_cols      = ["CI_Name", "CI_Cat", "CI_Subcat", "WBS", "Category", "Closure_Code", "Status", "Alert_Status"]
ordinal_cols  = ["Impact", "Urgency", "Priority"]
count_cols    = ["No_of_Reassignments", "No_of_Related_Interactions", "No_of_Related_Incidents", "No_of_Related_Changes"]
time_cols     = ["Open_Time", "Reopen_Time", "Resolved_Time", "Close_Time"]
duration_cols = ["Handle_Time_hrs"]
drop_cols     = ["number_cnt"]

import sys, importlib
importlib.invalidate_caches()
sys.path.append("../src")
from columns import *

grouped = id_cols + cat_cols + ordinal_cols + count_cols + time_cols + duration_cols + drop_cols
print(len(grouped), set(df.columns) - set(grouped))
