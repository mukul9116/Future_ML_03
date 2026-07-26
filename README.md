# Resume Screening System — Future Interns Task 3

## Problem Statement

Automated screening and ranking of resumes based on a certain job description, extraction
of candidate skills, identification of skills that are missing with respect to the job
description.

## Data

Raw data not included in the repository (refer to .gitignore). Datasets used:
- Resumes: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- Job descriptions: https://www.kaggle.com/datasets/PromptCloudHQ/us-jobs-on-monstercom

To replicate, download both files and put them in Google Drive directory FUTURE_ML_03/data/
or in directory data/ if working outside Colab.

## Dataset

### Resumes
- **Source:** Kaggle - snehaanbhawal/resume-dataset
- **Number of resumes:** Total of 2,484 resumes, in 24 categories.
- **Categories chosen for this project:** Information-Technology, Engineering, Finance,
  Sales, HR, Healthcare (selected for diverse vocabulary of skills – verified through word
  frequency analysis). CONSULTANT category was considered but rejected because of lack
  of distinctive vocabulary, DESIGNER was considered but rejected due to overlap with engineering.

### Job Description Sources
- **Source:** Kaggle - PromptCloudHQ/us-jobs-on-monstercom (22,000 US jobs, scraped from Monster.com)
- **Gap identified:** there are no corresponding job descriptions in the resume data set; hence a job description source had to be found that would allow us to do resume-to-job description matching.
- **Approach to selection:** one sample job description per category was chosen (not one per resume) because we have to rank multiple resumes against one job role, and having multiple job descriptions per category for each resume will make such ranking impossible
- **Sectors in Monster.com to categories in resume data set mapping** were used to identify candidates:

| Resume Category    | Monster.com Sector | Selected Job Title                |
|--------------------|------------------|-----------------------------------|
| Information-Technology | IT/Software Development   | IT Support Technician Job in Madison  |
| Engineering         | Engineering          | Sr. Process Engineer             |
| Finance            | Accounting/Finance/Insurance | Senior Accountant/Analyst Job in Denver |
| Sales              | Sales/Retail/Business Development | Sales Professional Job in Las Vegas  |
| Human Resources    | Human Resources    | Human Resources Manager Job in Dallas |
| Healthcare         | Medical/Health      | Registered Nurse - Clinic Job in Houston |

-**Intentional exclusions during resume selection:** “Software Engineer” was excluded from the
  Engineering category (it would clash with the IT terminology); finance-related or too
  specialized posts were excluded from Sales (e.g., "Financial Advisor/Financial Sales", 
  "Bilingual Newborn Photographer/Sales") in favor of a general "Sales Professional" post.

## Scope

Explore the resume dataset, cleanse and analyze resume texts, extract skills, find job
descriptions related to selected categories, develop resume-to-job description matching and
ranking system, rank candidates in relation to their respective job description and detect
skill gaps.

## Approach (Outline)

Loading Data -> Categories Selection and Validation -> Job Descriptions Selection -> 
Text Cleansing -> Skills Extraction -> Resume-JD Similarity Matching -> Candidate Ranking
-> Skill Gap Detection

## Design Note: Matching Scope

This design is meant to rank multiple resumes to ONE job description for each role (matches task requirement - "rank resumes based on a given job role"), NOT one unique JD for each resume. Underlying match function (similarity between a resume and a JD text) is category agnostic and can be applied to any resume-JD pair; but only 6 categories were included in scope of this project.

## Progress (Day 1 of 10)

- Created project repository (FUTURE_ML_03)
- Downloaded resume dataset from Kaggle
- Set up environment (Colab + Drive)
- Loaded dataset, analyzed category distribution
- Selected 6 resume categories using word-frequency analysis, and replaced 2
  initially-considered categories (CONSULTANT, DESIGNER) as it was proved that those categories lack distinctiveness
- Identified limitation: need to source separate job descriptions (not present in initial resume dataset)
- Sourced and selected 6 job descriptions (one for each category) from job postings
  dataset, avoiding skills overlapping between different categories
- Saved selected job descriptions as pickle for future use in matching and ranking steps

## Day 2 Findings (Text Preprocessing)

- Built a text cleaning pipeline using spaCy: tokenization -> lemmatization -> stopword
  removal, in that specific order (lemmatizing first ensures grammatical variants of
  stopwords, e.g. is/was/were/being, are all normalized to "be" before stopword matching,
  rather than relying on an exhaustive raw-form stopword list)
- Chose lemmatization over stemming for accuracy - stemming risks overstemming errors
  (e.g. "organization" and "organ" reducing to the same stem), which would create false
  skill matches
- Discovered spaCy's default stopword list missed resume-specific boilerplate (city,
  state, company, work, include) - built a custom stopword list using systematic
  cross-category word-frequency analysis rather than manual guessing
- Deliberately did NOT remove "customer", "management", "service" despite appearing
  across all categories - frequency alone doesn't mean a word lacks meaning; these are
  genuine business terms, not grammatical noise
- Applied cleaning to all 700 resumes (6 selected categories) and 6 job descriptions,
  saved as pickles for tomorrow's skill extraction work

  ## Day 3 Findings (Skill Extraction)

- Tested spaCy's default NER on sample text - confirmed it does NOT recognize skills
  out of the box (e.g. "SQL" was tagged as ORG, "Python" and "project management" were
  not recognized at all)
- Built a custom skill list using EVIDENCE from data (bigram/unigram frequency analysis
  per category), not manual guessing - mirrors the same evidence-based approach used for
  category selection (Day 11) and custom stopwords (Day 12)
- Excluded generic cross-category business terms (management, business, team, process)
  from the skill list - these carry meaning but have low discriminative value for
  ranking, since they appear roughly equally across all categories
- Implemented skill extraction using spaCy's EntityRuler (rule-based pattern matching,
  NOT a trained NER model) - confirmed and correctly labeled as keyword/
  phrase matching, not true NER
- Extracted and deduplicated skills for all resumes and job descriptions
- Known limitation identified and verified with real evidence: keyword matching cannot
  disambiguate context (e.g. "policy" in HR vs. Finance context are different concepts
  but get tagged identically) - documented rather than hidden