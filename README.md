# itsm-ml-project

Machine learning on IT service-management (ITSM) tickets for ABC Tech, in four tracks that follow the four objectives of the project brief: predict high-priority tickets, forecast incident volume, auto-tag tickets, and predict changes and failures.

**Data:** 46,606 tickets closed between 1 October 2013 and 31 March 2014, from a MySQL table (`dataset_list`). The extract is cut by close date, so the models use the tickets opened from 1 October 2013 to 16 March 2014: 167 days and 42,304 tickets (see `04_eda`, Figure 4). It is about 5.5 months of data, not several years. The dataset is confidential and is not included in this repository.

## Results

|Objective|Notebook|Chosen model|Result (test period: 1 Feb to 16 Mar 2014)|
|-|-|-|-|
|1. Predict priority 1 and 2 tickets|`06_track1_models`|Logistic regression on asset and time fields, alert threshold 0.678|Recall 0.583, precision 0.298 (about 5 alerts a day); ROC-AUC 0.934; average precision 0.315 against a 0.011 base rate. Logistic regression is used for the current extract because it performs the same as XGBoost within noise and its coefficients explain each alert; XGBoost is the first model to re-test when more data is available.|
|2. Forecast incident volume, quarterly and annually|`07_track2_volume`|SARIMA(1,0,0)(1,1,1,7) on daily counts, checked against a working-day run-rate|**Incidents:** about 18,500 to 19,100 per quarter and about 75,000 over the next 12 months. **All tickets:** about 23,000 to 23,700 per quarter and about 93,000 to 94,000 a year. Allow about ±10%; about 9% lower for incidents (15% for all tickets) if the early-March level continues.|
|3. Auto-tag priority and department, reduce reassignment|`09_track3_triage`|XGBoost priority tagger (P2 to P5); logistic-regression reassignment ranking|Tagger: accuracy 0.767, macro-F1 0.628 (lookup baseline 0.545). Reassignment: the top 10% of scores are 78.3% reassigned (2.02 times the base rate). **Department tagging is not possible:** the extract has no department or assignment-group field.|
|4. Predict RFCs and asset failure or misconfiguration|`08_track4_rfc`|Asset-code watchlist (TF-IDF + LightGBM); gradient-boosting failure-type suggestion|Linked changes cannot be predicted in general (at chance on all tickets), but the watchlist's top 50 held 32 linked tickets against 1.6 by chance. Failure type (from Closure_Code): Hardware recall 0.89. **Misconfiguration cannot be modelled:** no configuration or CMDB data.|

Every notebook ends with its findings and limits; every table and figure is numbered and cited in the text.

## Notebooks

Run them in this order (each one reads the files the previous ones write):

|Notebook|What it does|
|-|-|
|`01_connection_test`|Writes `src/db.py` and checks the database connection|
|`02_ingest_and_profile`|Loads the table, checks the schema, keys and data quality, saves a raw snapshot|
|`03_cleaning`|Types, missing values, label fixes, and the clean checkpoint|
|`04_eda`|Distributions, relationships, the 167-day modelling window, asset-label review|
|`05_split_features`|Time-based train/test split and the feature sets (Set A and Set B)|
|`06_track1_models`|Objective 1: high-priority alert|
|`07_track2_volume`|Objective 2: daily, quarterly and annual forecasts (all tickets, and incidents only)|
|`08_track4_rfc`|Objective 4: change-link watchlist and failure-type suggestion|
|`09_track3_triage`|Objective 3: priority tagger and reassignment risk|

Notebook 02 has a switch, `USE_DATABASE = False`, to rerun from the saved snapshot without a database connection.

## Setup

1. Create the environment and install the pinned packages:

```
   conda create -n itsm python=3.11
   conda activate itsm
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in `DB_HOST`, `DB_USER` and `DB_NAME`. The password is not stored anywhere; it is asked for in a hidden prompt when notebooks 01 and 02 connect.
3. Start Jupyter from the repository folder and run the notebooks in order.

## Running the project

**Without a database connection:** every notebook is committed with its outputs, so all results, tables and figures can be reviewed on GitHub without running anything.

**With a database connection:**

1. Fill in `.env` from the project's connection details (provided by the data owner; not stored in this repository).
2. Run notebook 01. It asks for the database password in a hidden prompt; the password is never saved to a file or shown in an output.
3. Run notebook 02 to load the table and save a local snapshot (`data/`, git-ignored). Notebooks 03 to 09 then run from the snapshot without connecting.

## Repository layout

```
notebooks/          the nine notebooks above
src/                helpers written by the notebooks (db.py, columns.py, project_config.py, features.py)
reports/figures/    figures saved by the notebooks (aggregates only)
data_issues_log.md  data problems found and how each was handled
requirements.txt    pinned package versions
.env.example        template for the local .env (key names only)
```

`data/`, `models/`, `docs/`, `.env` and PDF files are git-ignored. Notebook outputs show aggregates only: no ticket rows, credentials or asset codes.

## Limits and future work

* **Short history.** 5.5 months of complete data: the quarterly and annual forecast is a planning estimate, not a validated forecast, and no yearly pattern can be estimated. Two to three years of data would allow both.
* **Model choice with more data.** On this extract XGBoost and logistic regression tie (Track 1 CV average precision 0.455 against 0.451; Track 3 reassignment ROC-AUC 0.728 for both). With more history, XGBoost should be re-tested first, as it can capture interactions such as asset type × time of day that the linear model misses.
* **Missing fields.** A department or assignment-group field (for department tagging) and CMDB relationships (for change and misconfiguration prediction) were requested on 4 November 2026; they were not received. The notebooks document how they would be used.
* **Field timing.** Reassignment counts, related-record counts and KB_number may be filled in after a ticket opens, so they are kept out of the headline models; with them, Track 1 average precision rises from 0.315 to 0.397 (`06`, section 18).
* **Saved models.** Only the Track 1 model is saved (`models/`, git-ignored, because the encoder stores asset codes). The other models are proofs of concept and are retrained when their notebooks run.

