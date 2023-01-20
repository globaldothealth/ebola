# Ebola data Uganda outbreak 2022

This repository contains dated records of curated Ebola cases from the 2022 outbreak in Uganda. Data are curated from openly accessible sources. We continue to experience ongoing challenges in data curation, discussed below. Line-list data may change due to ongoing data reconciliation and validation. 

Our latest data set and archives can be found [here](https://3mmuwilir3.execute-api.eu-central-1.amazonaws.com/web).

UPDATE:

2023-01-20. On January 11th, 2023, the Ugandan Ministry of Health declared the end of the SVD Ebola outbreak. The final number of confirmed cases is 142. G.h counts for confirmed cases by district matches that reported in the MOH SitReps through [#90](https://www.afro.who.int/sites/default/files/2023-01/Ug_EVD_SitRep%2390.pdf) (Mubende 64; Kyegegwa 4; Kassanda 49; Kagadi 1; Masaka 1; Wakiso 4; Jinja 1; Kampala 17; Bunyangabu 1); however, SitRep [#91](https://www.afro.who.int/sites/default/files/2023-01/Ug_EVD_SitRep%2391.pdf) reassigned a KAL case to WAK without explanation. Therefore, final counts of confirmed cases by district do not match. 

Also, Outcome for ID#s 149, 150, 157, 158, 161, and 162 remain unassigned for reasons outlined in our [blog post](https://globaldothealth.substack.com/p/curator-review-for-2022-reflecting). 

Finally, Uganda's [MOH website](https://www.health.go.ug/ebola/) differs from final SitRep data in [#93](https://www.afro.who.int/sites/default/files/2023-01/Ug_EVD_SitRep%2393.pdf). The MOH website reports 142 cases/ 56 deaths/ 86 recoveries. SitRep data reports 142 cases/ 55 deaths/ 87 recoveries.

We recognize these discrepancies and remain limited by the detail and accuracy of information publicly released by the MOH. Questions can be addressed to info@global.health.

2022-12-14. The sum of deaths and recoveries for the G.h dataset is not in alignment with current MOH numbers. Our curation team identified count and location discrepancies in data from SitRep [66](https://www.afro.who.int/countries/uganda/publication/ebola-virus-disease-uganda-sitrep-66) and beyond that prevent us from updating the Outcome for the remaining cases. Also, SitRep [68](https://www.afro.who.int/countries/uganda/publication/ebola-virus-disease-uganda-sitrep-68) reported a reclassification of Outcome for a Mubende case; however, without further detail, we are unable to identify a specific ID# for the change. We are limited by the detail and accuracy of information publicly released by the MOH. We will continue to check for new MOH reports that may provide updated/corrected case information that could reconcile differences between our two datasets. 

2022-11-23: The curation team has completed a data reconciliation exercise to update case data between SitReps (e.g. deaths, recoveries, HCW, and location information). The "Date_last_modified" column lists the date of reconciliation on 2022-11-22.  Data are updated through SitRep [57](https://www.afro.who.int/countries/uganda/publication/ebola-virus-disease-uganda-sitrep-57) with a total of 141 confirmed cases, including 55 deaths, and 79 recoveries.

2022-11-04: Confirmed cases have been added to the line-list through SitRep [41](https://www.afro.who.int/sites/default/files/2022-11/Ug_EVD_SitRep%2341.pdf) @131 cases. Our curation team is working to reconcile case data between SitReps (e.g. deaths, recoveries, HCW), which will take time to complete due to changing report format and fluctuating counts that greatly complicate the review process.

## Data curation
This section is an overview of the data curation process, a discussion about limitations and assumptions.

Curation, especially early in the outbreak, is a manual, labor-intensive process. We experience many recurring challenges in building an emerging disease dataset in real-time.

The Ebola line-list is built from a collection of sources, listed here, which will be updated as new sources become available: https://github.com/globaldothealth/ebola/wiki. The original source(s) of information is provided for each line-list ID in our database. The WHO provides Situation Reports (SitReps) from the Uganda Ministry of Health; while not available from the start of the outbreak, these resources have become a primary source for information. However, we remain limited by inconsistent, aggregated, or missing case information; change in reporting format; data reconciliation; conflicting details; confusing statements; reporting delays. We frequently observe conflicting data and details between sources, and even within a single report. We have not outlined the specific challenges or discrepancies for each [SitRep](https://www.afro.who.int/countries/publications?country=879), but can discuss further as needed.

Reports from government/official sources can be enriched with supplemental information retrieved from local reporting (including media) or other sources. Metadata are added at any time, as information becomes available and our time and resources permit. After making changes, the case will be recorded as modified with the date. Multiple curators look at each datapoint and any discrepancies are resolved in conversations between them. Assumptions are made that may compromise the accuracy of the data. 

Users should refer to our [data dictionary](data_dictionary.yml) for a description of each variable. Assumptions for select variables are briefly discussed below.

**Case_status**: Only confirmed and probable cases are logged at this time. 

**Date_of_onset**: Information is only available for probable cases; we are unable to disaggregate Date_of_onset details for confirmed cases.  

**Date_confirmation**: The report date is used when a Date_confirmation is not specified by source.

**Outcome**. Type: Death: The report date is used when a Date_death is not specified by source. If the number of deaths exceeds the number of new cases reported for that day, then deaths are logged under a previous ID with unassigned outcome and corresponding location information, when available.

**Outcome**. Type: Recovery: When a recovery is reported, the recovery is assigned to a previous ID with unassigned outcome and corresponding location information, when available.

**Healthcare_worker**: Healthcare worker information (e.g. location, date_confirmation, outcome) is not consistently provided by source. Supplemental sources are used, when available, to gain context that may help us to assign an ID. However, due to the limited availability of information, we have not been able to log every confirmed HCW case or outcome. 

Data are hand-curated. The process and methods to create, organize, and maintain data have been applied with consistency; however, we’re human and mistakes happen. As stated above, line-list data may change due to ongoing data reconciliation and validation. We welcome your contributions and feedback. Get involved!

## Contributing

If you would like to request changes, [open an issue](https://github.com/globaldothealth/ebola/issues/new) on this repository and we will happily consider your request. 
If requesting a fix please include steps to reproduce undesirable behaviors.

If you would like to contribute, assign an issue to yourself and/or reach out to a contributor and we will happily help you help us.

If you want to send data to us, you can use our template at [ebola-template.csv](ebola-template.csv) which makes
it easier for us to add to our list. Just open an issue and attach a CSV / XLSX file in this repository,
or email data to info@global.health. Remove any Personally Identifiable Information.

## License and attribution

This repository is published under MIT License and data exports are published under the CC BY 4.0 license.

Please cite as: "Global.health Ebola (accessed on YYYY-MM-DD)" & please add the appropriate agency, paper, and/or individual in publications and/or derivatives using these data, contact them regarding the legal use of these data, and remember to pass-forward any existing license/warranty/copyright information.
