# Data issues log

Dataset: dataset\_list (46,606 rows, 25 columns). Only aggregate counts are recorded here, no raw records.

## Dataset scope

* All 46,606 tickets were closed between 2013-10-01 and 2014-03-31 (Close\_Time range). Open\_Time spans 2012 to 2014 and uses the format dd-mm-yyyy hh:mm.
* 97.5% were also opened in that window; 1,150 were opened earlier (the backlog still open on 1 October). Monthly volume is near zero before October 2013 (median month: 10 tickets), then 6,000 to 8,600 a month. The extract therefore appears to be cut by close date; the reason is an open question for the data owner (question 1 below).
* Survivorship: tickets opened before 1 Oct 2013 have 1 High in 1,114 labelled (0.09%), against 699 in 44,112 (1.58%) from October onward. They are excluded from modelling.
* The end of the window is right-censored: tickets opened in late March and still open on 31 March are absent. The share of tickets over 72 hours falls from a 24 to 27% plateau to 19.2%, 9.9% and 0.0% from the week of 17 March. (Weekly median elapsed time is too unstable to use for this check.)
* Modelling window: opened 2013-10-01 to 2014-03-16, 42,304 rows (41,074 labelled, 1,230 unlabelled).
* Track 2 has 182 days in the extract and 167 after trimming the censored end (about 24 weeks). Models are fitted on the daily series; quarterly and annual volumes are planning estimates that cannot be validated (see Track 2 below).
* The High rate by month falls from 2.13% (Oct) to 1.10 and 1.29% (Feb and Mar).

## Hidden missing values (placeholders stored as text)

|Column|Blank or placeholder|Reading|Treatment|
|-|-|-|-|
|Related\_Change, No\_of\_Related\_Changes|46,046|Blank means no change linked (560 linked)|Has\_Related\_Change flag; counts to 0|
|No\_of\_Related\_Incidents|45,384|Blank means none (1,222 linked)|Fill with 0|
|Reopen\_Time|44,322|Never reopened (2,284 reopened)|Has\_Reopen\_Time flag; left null|
|Closure\_Code|460 blank (a further 1,590 are the real value "Unknown")|Not recorded|"Not Recorded"|
|Resolved\_Time|1,780|Missing timestamp|Left null; not a feature|
|Impact, Priority|1,380 each (NS and NA)|Same rows, label unknown|Left null; excluded from Track 1 labels|
|No\_of\_Related\_Interactions|114|Unclear|Left null|
|CI\_Cat, CI\_Subcat|111 each|Unknown asset type|"Unknown"|
|Handle\_Time\_hrs, No\_of\_Reassignments|1 each|Stray blanks|Left null|

## Other issues

|Issue|Evidence|Decision|
|-|-|-|
|All 25 columns are strings|df.info()|Numerics and datetimes converted|
|Priority equals a lookup of Impact and Urgency|Crosstab has one value per pair|Impact and Urgency excluded from the headline features; Set A uses them as a contrast only|
|Severe class imbalance|3 P1 and 697 P2: 700 High of 45,226 labelled (1.55%)|P1 and P2 merged into High; metrics: recall, precision, average precision|
|number\_cnt is uniform random|Mean 0.500, std 0.289, all 46,606 values unique; not in the brief|Dropped|
|Alert\_Status is constant|"closed" in all 46,606 rows|Dropped|
|Status is 99.98% Closed and known only after handling|value\_counts|Kept in the clean file; excluded from features|
|Urgency has the label "5 - Very Low"|1 row|Recoded to 5|
|Duplicates|46,606 unique Incident\_ID|None|
|9 tickets have Status "Work in progress" and a Close\_Time|All opened and closed within October 2013|No action|
|Elapsed\_hrs (Close\_Time minus Open\_Time)|Median 18.4 hours, mean 123.1, maximum 15,722.6; no ticket closes before it opens|Heavy right skew; post-event, so not a feature|
|Category has a single "request for change"|value\_counts|Track 4 target is Has\_Related\_Change (560 tickets; 516 in the modelling window)|
|No free-text or department column|Column list (`09`, section 1b)|Track 3 covers priority tagging and reassignment risk; department tagging deferred (field requested 4 Nov, not received)|

## Handle\_Time\_hrs: evidence and decision

* Handle\_Time\_hrs (a post-event duration in hours) has two formats: decimal commas that parse (15,353 rows with a Close\_Time) and about 31,250 digit-grouped integers (pattern 9,99,99,99,999) that cannot be read as decimals.
* Relation to Open\_Time and Close\_Time (clean rows, by elapsed time): handle equals elapsed for 96.0% of tickets under 1 hour (10,117) but only 27.5% for 1-8 hours (1,915), 0.5% for 8-24 hours (950), 0.4% for 1-3 days (846), 0.1% for 3-7 days (708) and 0.1% over 7 days (817). Median handle time for tickets over a day is 0.5 to 5.1 hours. For 1-8 hour tickets the 75th percentile is 13.2 hours, so at least a quarter (about 480) have a handle time above their whole Open-to-Close span: handle time is not a function of Open\_Time and Close\_Time alone.
* Working-hours clock: among same-day weekday tickets touching time outside 7:30-18:00 (226 of 12,010), handle equals the clipped window value for 76.5% and plain elapsed time for 14.6%, so a working-day clock applies within a day (the end time is not well identified). For multi-day tickets it does not match (window match 27% to 40%, 8.9% over 7 days).
* Damaged strings: 70.2% of 31,240 agree with the window value up to a power of ten (chance 2.6%), falling from 92% (1-8 hours, 9,333 rows) through 83.5%, 72.1% and 60.5% to 36.2% (over 7 days, 6,535 rows), mirroring the clean rows. The decimal place is lost, so values cannot be recovered without a rule for the number of decimals.
* Three bins have a maximum of 99.7 to 100.0 hours among clean rows (8-24h, 1-3d, 3-7d): possibly a cap or a selection effect; the cause cannot be determined from the extract.
* Decision: unchanged. Parsed values kept, the rest null; excluded from every feature set (post-event); Elapsed\_hrs derived from timestamps for descriptive use. No decoding column is built.

Clean file: 46,606 rows x 26 columns (25 original, minus 2 dropped, plus Has\_Reopen\_Time, Has\_Related\_Change and Elapsed\_hrs). Datetime nulls (Reopen\_Time 44,322, Resolved\_Time 1,780) are left as null; no imputation.

## Track 1 feature decisions

* Firm exclusions (post-event): Status, Resolved\_Time, Close\_Time, Reopen\_Time, Has\_Reopen\_Time, Handle\_Time\_hrs, Elapsed\_hrs, Closure\_Code.
* Timing unconfirmed (excluded from the headline; tested as a sensitivity run): No\_of\_Reassignments, No\_of\_Related\_\*, Has\_Related\_Change, KB\_number.
* Identifiers (not features): Incident\_ID, Related\_Interaction, Related\_Change.
* month is excluded: the test months (Feb, Mar) never occur in training. hour and weekday are used.
* CI\_Name: 2,471 values in training; 4.9% of test rows carry a value never seen in training; 76% of High tickets sit on CIs with under 30 training rows. Excluded from the baseline; adding it gave no gain (see sensitivity runs).
* WBS: 255 values in training; 0.6% of test rows unseen. Encoding: one-hot with values under 30 training rows pooled into an "infrequent" bucket, fitted on training data only.
* The test period High rate is 1.12% (115 of 10,229), so always predicting Not High scores 0.9888 accuracy. Metrics: recall, precision, average precision.

## Track 1: modelling log

### Pipeline notes

* Validation: time-ordered folds (3) inside the training period for tuning; January used to choose the alert threshold; test period (1 Feb to 16 Mar) scored for the headline result.
* Imbalance: balanced sample weights, not SMOTE (features are one-hot categories, so synthetic rows are not meaningful).
* Outlier capping, Yeo-Johnson and scaling are not applied: Track 1 features are categorical plus hour and weekday; the skewed numeric columns are post-event and excluded.
* Explanation: logistic regression coefficients instead of SHAP.
* models/track1\_priority\_lr.joblib contains confidential asset codes, so it is git-ignored and not published.

### Model comparison (asset and time fields, time-ordered CV, average precision)

|Model|CV average precision|Test average precision|
|-|-|-|
|XGBoost (64-setting grid)|0.455|0.321|
|Logistic regression (C=0.01)|0.451|0.315|
|Gradient boosting|0.442|0.306|
|Random forest|0.428|0.336|
|Decision tree|0.405|0.322|

Random model: 0.0175 (training High rate). XGBoost is top by 0.004, well within fold-to-fold variation (about 0.04). Tie-break rule: logistic regression is kept when the top model is within 0.01 CV AP, because its coefficients explain each alert; the rule was added after the wider XGBoost grid was run, which is stated in `06`, section 6. XGBoost is the first alternative to re-test with more data. With C extended to 0.003 to 0.1, C=0.01 still won.

### Set A (Impact and Urgency included): not a result

Recall 0.965 (111 of 115) for all five models, CV AP 0.994 to 1.000, test AP 0.955 to 0.991, because Priority is a lookup of Impact and Urgency. The same 4 High tickets are missed by every model; the cause was not investigated (possibly rare Impact and Urgency combinations pooled by the encoder).

### Test result (headline: logistic regression, asset and time fields)

|Measure|Value|
|-|-|
|Threshold|0.678, chosen on January for 70% recall (validation precision 0.27)|
|Confusion matrix|9956 / 158 / 48 / 67|
|Recall|0.583 (67 of 115), 95% bootstrap interval 0.496 to 0.672|
|Precision|0.298, interval 0.239 to 0.358|
|ROC-AUC|0.934|
|Average precision|0.315 (28 times the 0.0112 base rate); CV was 0.451 (26 times 0.0175)|
|Accuracy|0.980, below the always-negative 0.9888|
|Alerts|about 5 a day of about 232 labelled tickets a day|

* Validation recall of 0.70 did not reproduce on test; test noise alone does not explain it (the interval excludes 0.70). Intervals treat tickets as independent.
* Operating points (threshold set on validation, applied to test):

|Validation recall target|Alerts per day|High caught|Test recall|Test precision|
|-|-|-|-|-|
|0.5|2.6|53|0.461|0.461|
|0.6|2.8|58|0.504|0.468|
|0.7|5.1|67|0.583|0.298|
|0.8|22.5|91|0.791|0.092|
|0.9|44.4|103|0.896|0.053|

* Limitation: priority is predicted at ticket creation from asset and time fields only.

### What the model uses (logistic coefficients, associations only)

Towards High: Category incident (+0.96), hours 6 and 7 (+0.73, +0.72), Sunday (+0.71), Saturday (+0.50), CI\_Cat networkcomponents (+0.65), Unknown (+0.44), computer (+0.32). Towards Not High: request for information (-0.97), hour 15 (-0.55), Wednesday (-0.50), hour 12 (-0.49), Tuesday (-0.38).

* CI\_Cat computer: 13.26% High in normal hours (2,436 tickets), 27.50% at night or weekends (80); other assets 0.57% and 6.60%. Most of the computer effect is not a night effect. Its small coefficient is likely shared with CI\_Subcat and WBS, which overlap with it; this was not tested separately.
* CI\_Cat Unknown (blank in source): 97 training tickets, 8 High (8.2%); the coefficient rests on 8 events.
* Interaction not modelled: night or weekend raises the High rate 11.5 times for other assets, 2.1 times for computers.

### Sensitivity runs (logistic regression)

|Features|CV AP|Test AP|Test ROC-AUC|
|-|-|-|-|
|Asset and time (headline)|0.451|0.315|0.934|
|+ CI\_Name|0.452|0.319|0.936|
|+ six unconfirmed-timing fields|0.493|0.397|0.962|

* CI\_Name adds nothing: excluded.
* Single fields: KB\_number +0.034 CV AP (largest); No\_of\_Related\_Incidents +0.030 test AP; the other four add at most +0.014 test AP.
* Rolling monthly folds, six fields (C=0.03): AP 0.549, 0.503, 0.436, 0.368 (mean 0.464) against 0.510, 0.410, 0.370, 0.274 (mean 0.391); the gain appears in every fold. Consistency does not separate real signal from leakage, so the headline stays on asset and time fields until the timing of these fields is confirmed (question 5 below).
* The test period was also scored for these variants; none was selected on it.

### Optimisation (rolling-origin CV, 4 monthly folds, 345 High tickets)

Test period already viewed several times, so decisions used rolling folds (Dec, Jan, Feb, 1 to 16 Mar; High counts 130, 100, 79, 36). Time features were fixed a priori (office hours 8 to 18, weekend).

|Model|Mean AP|Recall at 2.2% alerts|
|-|-|-|
|LR, asset and time (current)|0.391|0.613|
|LR + time features|0.392|0.614|
|XGBoost + time features|0.402|0.620|
|XGBoost deeper|0.402|0.627|
|Rank average of LR and XGBoost|0.402|0.626|

* Gains of at most +0.011 are within noise: logistic regression stays.
* LR lift over the base rate is 23 to 34 times across folds, so the AP fall tracks the falling High rate.
* Tree models lose the smallest-training fold and win later ones, so they may need more data; this was not tested.
* Not tried: SMOTE (synthetic rows are not meaningful for one-hot categories), neural networks (too few positives: 541), and re-adding CI\_Name (no gain in the sensitivity run).

### Coefficients by column (saved model)

Read from models/track1\_priority\_lr.joblib on 2026-11-01: 166 one-hot features, intercept -0.886, largest |coef| 1.755 (odds about 5.8 times). Sum and mean of |coef| per input column:

|Column|Features|Sum of abs coef|Mean per feature|
|-|-|-|-|
|WBS|99|22.66|0.23|
|CI\_Subcat|27|6.61|0.24|
|hour|18|5.15|0.29|
|CI\_Cat|12|2.87|0.24|
|weekday|7|2.67|0.38|
|Category|3|1.95|0.65|

* The sum grows with the number of values, so WBS leads on the sum only; per feature, Category and weekday move the odds most.
* Neither number is contribution to performance (that depends on how often each value occurs). Drop-column or permutation AP on January would answer that (not run).
* The saved bundle holds class\_weight=None, so the balanced weights were passed at fit time as sample weights. 98 of the 166 feature names contain WBS codes: the file is not published.

## Open questions for the data owner, and the assumption used

No answers were received, so each question was handled with the assumption shown.

1. Was the extract cut by close date, and is data outside 1 Oct 2013 to 31 Mar 2014 available? Assumed yes, cut by close date (04\_eda); the models use tickets opened 1 Oct 2013 to 16 Mar 2014.
2. What is number\_cnt? Treated as noise (uniform random values, all unique) and dropped.
3. What format is Handle\_Time\_hrs meant to have? Two thirds of values cannot be read; the column is post-event and not used as a feature.
4. Is High (priority 1 or 2) the right target, with Impact and Urgency excluded because Priority is a lookup of them? Assumed yes.
5. Which fields exist when a ticket is created (KB\_number, the related-record counts, Related\_Change, No\_of\_Reassignments)? Assumed not known at creation; excluded from the headline models and tested only as a sensitivity run.
6. What recall and alert volume could the service desk accept? Assumed about 5 alerts a day (70% recall target on validation); other operating points are reported (06, Table 9).
7. Is Category set at creation? Assumed yes; used as a feature.
8. Are night and weekend tickets automated alerts? Unknown; hour and weekday are used as features as recorded.
9. Track 3: what should be tagged? Resolved by the project: priority tagging and reassignment risk; department tagging needs an assignment-group field.
10. Track 4: which field defines the RFC target? Resolved by the project: Has\_Related\_Change.
11. What may be published? Assumed: code and aggregate results only; no data, models or asset codes.
12. Is priority fixed at ticket creation? Assumed yes; history-based features were tested but not adopted.

## Track 1: evaluation addendum

* Target: High = Priority in (1, 2), labelled tickets only. Across the whole file, 695 of 700 High tickets have Impact 1 or 2 (the other 5 are Impact 3), so High is nearly "Impact 1 or 2". This is why Impact and Urgency are excluded (open question 4).
* Test period (10,229 tickets, 115 High) was also scored for Set A, the sensitivity variants and the rolling folds. The headline model, features and threshold were fixed before any of them, and none changed them.
* Rule baselines: "computer" flags 765 (7.5%), catches 62, recall 0.539, precision 0.081; "computer and incident" flags 742, catches 62, precision 0.084. The model at the same volumes catches 83 (recall 0.722, precision 0.108 and 0.112).
* Alert budgets: top 1.0%: 102 alerts, 50 caught; 2.2%: 225, 67; 5.0%: 511, 80; 10.0%: 1,023, 92.
* Segments at threshold 0.678: computer 765 tickets, 62 High, 153 alerts, 60 caught (0.97); other assets 9,464 tickets, 53 High, 72 alerts, 7 caught (0.13). Night or weekend: 178 tickets, 7 High, 45 alerts, 3 caught. Normal hours: 10,051 tickets, 108 High, 180 alerts, 64 caught. Incidents: 114 High, 67 caught; the 1 High request for information was missed.
* Recall interval resampling whole days: 0.49 to 0.672 (ticket-level: 0.496 to 0.672).
* Recall gap (0.70 on validation, 0.583 on test): the Oct to Dec model on test caught 66 of 115 (0.574, 224 alerts) against 67 for the final model, so refitting is not the cause. Feb 45 of 79 (0.57); 1 to 16 Mar 22 of 36 (0.611). Computer share of High tickets: Oct 0.60, Nov 0.61, Dec 0.71, Jan 0.65, Feb 0.53, Mar 0.56; training 345 of 541 (64%), test 62 of 115 (54%). Reading: recall depends on the asset mix (an estimate, not tested directly); the rest fits threshold-selection optimism and noise.
* Six unconfirmed-timing fields at equal alert volume (225): 79 of 115 caught (recall 0.687, precision 0.351) against 67 (0.583, 0.298); computers 60 of 62 in both, other assets 19 of 53 against 7. Single fields (CV AP / test AP): Reassignments 0.456/0.321, Related\_Interactions 0.450/0.317, Related\_Incidents 0.461/0.345, Related\_Changes 0.455/0.328, Has\_Related\_Change 0.455/0.329, KB\_number 0.485/0.346. KB\_number has no blanks, so it may be assigned late. Not used in the headline (open question 5).
* Coefficient weight (sum of absolute values): WBS 22.66 (99 columns), CI\_Subcat 6.61, hour 5.15, CI\_Cat 2.87, weekday 2.67, Category 1.95. Rough guide only: sums grow with the number of categories.
* History features on rolling folds (mean AP): recent-ticket counts 0.389, prior High rate of CI and WBS 0.414, both 0.416, against 0.391 for Set B. The first three folds tie (0.430 against 0.429); the gain is the 36-ticket March fold. Non-computer recall at 2.2% alerts 0.072 to 0.190. Not adopted. Related open question: whether priority is fixed at ticket creation (question 12).
* Break-fix check: an incident-only model, scored on test incidents at the headline model's alert volume (218), caught 67 of 114, the same as the headline model (AP 0.311 against 0.319, ROC-AUC 0.924 for both). Not adopted; Category already separates break-fix from non-break-fix tickets.

## Track 2: volume forecasting (`07`)

* Series: 167 daily counts, 1 Oct 2013 to 16 Mar 2014 (42,304 tickets). Strong weekly cycle (seasonal strength 0.95), no trend, a Christmas dip, early March about 15% lower. Non-stationary (ADF p = 0.18); stationary after a first difference or a weekly difference. No log transform (the weekly swing does not grow with the level).
* Test period (one forecast made on 31 Jan): SARIMA(1,0,0)(1,1,1,7) WAPE 11.1%, seasonal naive 21.5%, Holt-Winters 26.5%, ARIMA(1,1,3) 54.8%. MAPE over all days is distorted by weekend days with 1 to 16 tickets, so weekday MAPE and weekly-total MAPE are reported instead.
* Residuals: no significant leftover autocorrelation (Ljung-Box p 0.18 and 0.17; one correlogram bar at lag 6 just outside the band), but heavy-tailed because of the holidays (Jarque-Bera p < 0.001), so the forecast ranges are too narrow.
* Rolling 4-week backtest (12 origins): run-rate 15.5% mean error on 4-week totals, SARIMA 17.7%, naive 20.2%; 80% ranges held the actual total only half the time. The run-rate is the planning figure; SARIMA agrees with it within 1% per quarter.
* Final model refitted on all 167 days. All tickets: 22,859 to 23,569 per quarter, 93,115 over Apr 2014 to Mar 2015 (range 88,036 to 98,113). Incidents only (`07`, section 18; 80.7% of tickets): 18,455 to 19,025 per quarter, 75,164 over 12 months (70,670 to 79,491); run-rate 75,397.
* Limits: the models know only the weekly cycle and the recent level (no Christmas or yearly pattern); quarterly accuracy cannot be validated with 5.5 months.

## Track 3: auto-tagging and reassignment (`09`)

* No department, assignment-group or resolver field (only No\_of\_Reassignments matches a routing term). Department tagging deferred.
* Reassignment: 40.7% of window tickets reassigned at least once; median time to close rises from 2.5 hours (none) to 243.6 hours (five or more); Spearman 0.53 (association, not cause). Logistic regression ranking: ROC-AUC 0.728, top 10% are 78.3% reassigned (lookup baseline ROC-AUC 0.606).
* Priority tagger (P2 to P5, Set B): XGBoost accuracy 0.767, macro-F1 0.628, balanced accuracy 0.740 (lookup 0.545 / 0.546). P2 recall 0.64 at precision 0.18. P1 cannot be learned (3 tickets, all in the test period).

## Track 4: changes and failures (`08`)

* Target Has\_Related\_Change: 516 of 42,304 window tickets (1.22%) from 205 changes; the 5 largest changes hold 45% (incident storms).
* Five classifiers on asset and time fields are at or below chance on all tickets (ROC-AUC 0.38 to 0.45). Asset-code watchlist (TF-IDF + LightGBM): 32 linked tickets in its top-50 lists over three periods against 1.6 by chance.
* Checks: no sign of retrospective linking (recently closed tickets linked at 0.97% against 0.59% to 0.74% for older ones); inferred CI relationships (shared changes, same-hour tickets) gave no signal. A confirmed dependency map needs the CMDB.
* Failure type from Closure\_Code (5 types, 23,019 window tickets): gradient boosting chosen; Hardware recall 0.89, precision 0.72; right 78% of the time for the 46% of tickets above 0.5 confidence. Closure\_Code is a stand-in label; misconfiguration cannot be modelled.

## Data quality checks and label fixes (`03`, `04`)

* No timestamp out of order; blanks occur in fixed pairs (Related\_Change with its count, CI\_Cat with CI\_Subcat, Priority with Impact; all 460 blank Closure\_Codes are among the 1,780 blank Resolved\_Times).
* Case duplicate merged: CI\_Subcat "IPtelephony" / "Iptelephony" (3 tickets). Dutch Closure\_Code "Overig" (1) recoded to "Other"; "Kwaliteit van de output" (10) kept.
* Similar CI\_Subcat labels (TF-IDF cosine similarity 0.5 or more): 13 of 1,953 pairs, flagged for CMDB review, not merged (`04`, Table 14). "zOS Server" / "zOS Systeem" is the likely duplicate.
* Outliers (IQR rule) are flagged but not capped: the skewed columns are post-event and not features.

## Data request (4 Nov 2026)

Additional data was requested from the data owner, including a department or assignment-group field, CMDB relationships between CIs, and answers to the open questions above. It was not available when the project was completed, so the analysis uses the current extract only, and the affected parts (department tagging and misconfiguration prediction) are documented as limits.

