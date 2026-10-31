\# Data issues log



Dataset: dataset\_list (46,606 rows, 25 columns). Only aggregate counts are recorded here, no raw records.



\## Hidden missing values



| Column | Blank or placeholder | Reading | Treatment |

|---|---|---|---|

| Related\_Change, No\_of\_Related\_Changes | 46,046 | Blank means no change linked (560 linked) | Has\_Related\_Change flag, counts to 0 |

| No\_of\_Related\_Incidents | 45,384 | Probably none (1,222 linked) | Fill with 0 |

| Reopen\_Time | 44,322 | Never reopened (2,284 reopened) | Has\_Reopen\_Time flag |

| Closure\_Code | 2,050 | Not recorded | "Not Recorded" |

| Resolved\_Time | 1,780 | Missing timestamp | Leave blank, not a feature |

| Impact, Priority | 1,380 each (NS and NA) | Same rows, label unknown | Exclude from Track 1 labels |

| No\_of\_Related\_Interactions | 114 | Unclear | Check, probably 0 |

| CI\_Cat, CI\_Subcat | 111 each | Unknown asset type | "Unknown" |

| Handle\_Time\_hrs, No\_of\_Reassignments | 1 each | Stray blanks | Inspect those rows |



\## Other issues



| Issue | Evidence | Decision |

|---|---|---|

| All 25 columns are strings | df.info() | Convert numerics and datetimes |

| Handle\_Time\_hrs uses comma decimals | 46,349 rows | Replace comma, convert to float |

| Priority equals a lookup of Impact and Urgency | Crosstab has one value per pair | Test with and without Impact and Urgency |

| Severe class imbalance | 3 P1, 697 P2, about 1.5% high priority | Merge P1 and P2 into High |

| number\_cnt looks like random noise | All values unique, not in brief | Drop after check |

| Alert\_Status is constant ("closed") | 46,606 identical rows | Drop |

| Status is 99.98% Closed and only known after handling | value\_counts | Drop |

| Urgency has the label "5 - Very Low" | 1 row | Recode to 5 |

| No duplicates | 46,606 unique Incident\_ID | No action |



\## Open questions for mentor



\- What is number\_cnt?

\- Which field defines the RFC target for Track 4?

\- Should Impact and Urgency be allowed as features for Track 1?

\- What may be published publicly (code, charts, results)?



number\_cnt is uniform random (mean 0.50, std 0.289): drop.

Closure\_Code: “Unknown” is a real value (1,590); the other 460 are blank, so map them to “Not Recorded”.

Time columns use dd-mm-yyyy hh:mm, spanning 2012 to 2014.



Handle\_Time\_hrs has mixed formats: decimal comma in about 15,000 rows, and a digit-grouped integer, probably hours × 10^6, in about 31,000 rows. Fix pending verification.





Shape (46606, 26): 25 original columns, plus Has\_Reopen\_Time, Has\_Related\_Change and Elapsed\_hrs, minus the two dropped columns.

Handle\_Time\_hrs has 31,253 nulls, not the 31,252 I predicted. My count was off by one: it’s the 31,252 failed conversions plus the 1 stray blank we saw earlier. Nothing is wrong.

Every remaining null is a deliberate one: Related\_Change 46,046, Reopen\_Time 44,322, Resolved\_Time 1,780, Impact and Priority 1,380 each, No\_of\_Related\_Interactions 114, No\_of\_Reassignments 1. Closure\_Code, CI\_Cat and CI\_Subcat are now complete.

Elapsed\_hrs is sound. No ticket closes before it opens (0 rows). The median is 18.4 hours, but the mean is 123 and the maximum is 15,723 hours (about 655 days). That heavy right skew is the reason the outlier and Yeo-Johnson steps exist, and it matters for EDA charts and for any model that depends on distances. It’s also a post-event field, so it can’t be a feature.

