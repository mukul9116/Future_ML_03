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
  category selection (Day 1) and custom stopwords (Day 2)
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

  ## Day 4 Findings (TF-IDF + Cosine Similarity Matching)

- Built TF-IDF vectors across combined resume+JD corpus, split back into resume/JD
  matrices preserving original order, computed cosine similarity between all
  resume-JD pairs
- Built a category-matching check (not true ranking evaluation) using existing
  resume category labels as ground truth - initial accuracy: 55%
- Root cause investigation found organization/company names (e.g. "teamsoft", "aflac",
  "experis") were dominating TF-IDF weights due to high IDF (rare across the collection)
  despite carrying no skill-relevant meaning - different from "too common" stopword problem
- Fixed systematically using spaCy's built-in (trained) NER to detect and remove ORG
  entities from job description text
- Accuracy improved from 55% to 62.7% after the fix
- NON revomable limitation(using spaCy): 3/14 instances of one org name survived removal due to
  missing whitespace after punctuation in the source text (a raw-data quality issue,
  not a pipeline bug) - accepted as a documented, proportionate tradeoff rather than
  engineered around further
- Investigated remaining Healthcare->Sales mismatches and found they are NOT matching
  errors - they are genuinely hybrid/ambiguous resumes (healthcare recruiting, medical
  billing/insurance, medical transcription) that legitimately span multiple categories
- Important clarification: this 62.7% is a category-matching check, NOT a
  measurement of ranking quality - true ranking evaluation (comparing multiple resumes
  against ONE job description) is separate, future work

  ## Day 5 Findings (Ranking Model) — Full Debugging Log

It was the most comprehensive debugging process in the course of the whole project so far.
Starting from "build a ranking function," it led to resolving four completely different,
compounding bugs. Documented fully since each of them is an evidence-based engineering
discovery, not a guess.

### Problem 1: skill_overlap trivially hit 1.0 in case of unrelated resumes
rank_resume_for_job() was implemented combining similarity_score() and skill_overlap(). The first
test of the new function against IT job description brought up HR, Healthcare, and Finance
resumes in top ranks; zero resumes matching the IT JD. Upon investigation, it turned out that
the list of extracted_skills for the IT JD contained only 7 words, among which (account, client,
benefit) were too generic and could be found in practically any resume, resulting in skill_overlap
equal to 1.0.

### Problem 2: List of skills became too tight after previous narrowing
Discovered the problem with the very skill list, which has been progressively narrowed to decrease
the noise on Day 3, leaving IT category with nothing to match. Skill list was re-created by the use of
TfidfVectorizer (top 150 words per category, ngram_range=(1,2)) and manual curation into a clean,
evidence-based list (see skill_list in 03_skill_extraction).

### Problem 3: Whether the issue was with the IT Job Description
To ensure that the skill set for the job was truly done, tried whether switching to another IT
job description which would be highly technical ("Database Architect Job in Denver" – focused
on SQL, servers, storage) would fix the problem. However, it DID NOT; the switched job
description could extract only 1 skill using the same pipeline. This proved that the problem
was NOT about the specific Job Description chosen (which was the case with Day 4
Engineering Job Description), but rather it lied somewhere deeper within the extraction
process. Switched back to the original IT Job Description ("IT Support Technician Job in
Madison").l IT JD ("IT Support Technician Job in
Madison") since swapping did not help.

### Problem 4 (ROOT CAUSE): extract_skills() was the wrong function for JD requirements
Even after reworking the skills list based on TF-IDF evidence, the incorrect ranking of IT and
SALES still persisted. After a deeper analysis of extract_skills(), the real problem appeared to
be that this function was designed to be agnostic of category (RIGHT in the case of resumes, as
candidates’ true skills can belong to several categories) and was mistakenly used for generating
“required skills” list for each JD. The problem with this approach is that every word in skill-list of
ANY category that appears ANYWHERE in JD’s raw text (including recruiter boilerplate words
like "benefit," "candidate," "recruiting" in the IT JD’s compensation section, and "healthcare,"
"insurance," "medical" in the SALES (Aflac insurance) JD's text) was taken into account as a
requirement of this JD despite originating from another category's skill list.

FIX: implemented a new extract_skills_for_category(text, category) function that filtered entities
to ONLY the label matching the category of the JD in question, and used it only in JD generation.
Extract_skills() was not changed for resumes – on purpose, as category-agnostic extraction is
right here.

### Result
The per-category top-7 accuracy went from being completely broken (0/7 for IT, 0/7 for SALES)
to being 40/42 accurate for all 6 categories after the fix was implemented, which fully resolved
what looked, at several points during the day, to be an irreducible structural limitation.

### The weighting 0.7/0.3 stays over 0.9/0.1
We tested three weightings (0.7/0.3, 0.8/0.2, 0.9/0.1) using two metrics: an aggregate
category-matching sanity check (argmax for all 6 job descriptions) and the actual quality of
per-role top-7 rankings (number of correctly ranked resumes out of top-7). The metrics turned out to
be INCONGRUENT: 0.9/0.1 had higher score on the sanity check (75% vs 62.7%) but produced
WORSE rankings (IT category went down from 6/7 to 4/7 correct resumes in the top 7). 0.7/0.3 was chosen as the final weighting in our production ranking function, because the ranking
quality is actually the deliverable metric, while the sanity check was used merely as an indicator.

### Score presentation: match_percentage
Added a min-max normalized match_percentage (0-100%) alongside the raw combined_score,
solely for stakeholder comprehension (it is much easier for a recruiter to understand
"94% match" than "0.464").
Documentation: limitation - relative to the current set of ranked candidates, not
some absolute quality measurement - a "95% match" translates into "most qualified out of the
candidates considered", not "95% qualified".

### Key insight
Function correctness is determined by its USE CONTEXT, not by its implementation per se.
The extract_skills() function was correct in use with resumes but was incorrect when used
with job postings, even though it was the same code being used on seemingly identical data.

## Day 6 Findings (Skill Gap Identification)

- Added method identify_missing_skills(): set difference between JD required skills and resume
  skills (like the intersection logic that is already implemented in skill_overlap_score)
- Added method full_candidate_report(): combines ranking (Day 5) and missing_skills into
  one output for stakeholders - shows only Category, match_percentage, and
  missing_skills; (all internal columns such as similarity_score/skill_overlap removed)
- First finding: IT, SALES, HR have no missing skills even in rank 20, but FINANCE and
  HEALTHCARE show interesting missing skills
- Checked if it is a bug by checking worst ranked resumes for IT (not just the best ones)
  and found that system properly shows all 4 missing skills in WORST ranked resumes in
  IT (they have no common skills with SALES/ENGINEERING/HEALTHCARE)
- The root cause of the brief list of missing IT skills is proven by full text evidence: the IT skill list
  is quite comprehensive (29 authentic IT skills: database, network, server, sql, cisco,
  active directory, etc.) but the text of this particular job posting only uses 3-4 of them
  (application, software, technical) - the posting is a real but shallow IT support job
  description (previously marked as boilerplate-laden on Day 4) that even mentions a
  specific piece of software ("landesk") that is not found in our skill list, as it was not
  in the original list generated through TF-IDF
- Once again proves (same conclusion as on Day 5): keyword-driven extraction is possible
  to extract only those skills that EXPLICITLY mentioned in the specific job posting's text
  - no matter how comprehensive your skill list, a lack of explicit technical terms in the
  document's text makes the extraction impossible
- This is noted down as a fundamental limitation of the current technique, not as a bug -
  a truly technical IT job posting would produce longer missing skills list in the same conditions

  ## Day 7 Findings (Evaluation & Bias Analysis)

### Manual Validation of Matches
Examining real text from top ranked resumes in Healthcare, Sales, and Information-Technology.
The top matches for all three categories were manually verified as legitimate,
accurate matches by human judgment - even Information-Technology, despite being
known to have a very short skill set (4 skills), the ranking algorithm (weighted 0.7 for TF-IDF similarity)
still manages to find legitimate matches even in cases where skill_overlap is not helpful.

### Balance of Categories
All 6 categories have been verified to have a similar number of resumes (between 110-120).
No category is undersampled, therefore sample size should not affect the ranking performance
across categories.

### Testing for Bias
- Length of resume vs. similarity_score: r=0.176 (weak) - Cosine similarity is
  fairly robust to the length of the document as it was designed to be
- Length of resume vs. number of extracted skills: r=0.538 (moderate to strong)
  - GENUINE ISSUE OF FAIRNESS. Longer resumes contain more skills regardless of whether
  the candidate actually has them, which would unfairly affect concise candidates.
- DECISION: I chose not to alter the formula to adjust for this bias since the
  current 0.7/0.3 balance was carefully validated on Day 5 to return the proper top-7
  ranking in each of the six categories. Adjusting could undermine this without proving 
  improvement.

### Limitations of the Consolidated System (Days 3-7)
1. Predefined vocabulary for skill extraction: The consolidated system only extracts those
   skills which are included in a predefined list of 71 terms divided into 6 categories,
   irrespective of their importance or existence
2. Context-agnostic matching: Same words were being matched irrespective of its context
   (e.g. “Policy” in the HR vs. Finance context)
3. Bias towards resume length: Longer resumes have higher chances of skill extraction,
   irrespective of the qualifications (r = 0.538)
4. One job description per category: The ranking will be in accordance with one particular
   JD of that category and not the generalized role - changing the wording of the same JD can
   change the outcome (Day 5's JD swap test demonstrates this)
5. Category matching accuracy (Day 4, 62.7%) is the proxy validation metric and not the
   actual ranking quality metric - the per-category ranking (validated on Day 5-7) is the
   actual output and performs significantly better