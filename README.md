# Resume Screening System — Future Interns Task 3

## Problem Statement
Screen and score resumes based on the provided job description, and detect missing skills for
recruiters' initial, automated filtering.

## Dataset
- Resumes: Kaggle - snehaanbhawal/resume-dataset (6 of 24 categories used: IT, Engineering,
  Finance, Sales, HR, Healthcare)
- Job Descriptions: Kaggle - PromptCloudHQ/us-jobs-on-monstercom (1 posting per category)

## Approach
Text cleaning (spaCy) → rule-based skill extraction (EntityRuler) → TF-IDF & cosine similarity
→ ranking (0.7 similarity + 0.3 skill overlap) → gap analysis of missing skills → bias detection
→ Streamlit app.

## Major Findings
- No JDs available in the resume dataset; curated and prepared a new JD dataset
- Identified and resolved rare word contamination problem (company names affect TF-IDF score) via spaCy NER
- Detected a critical bug in the code – JD skill extraction relied on the same function
  as in resume skills extraction and thus incorrectly recognized some boilerplate items as
  skills (fixed the bug and increased per-category ranking precision from 0% (0/7) to 90% (40/42) for 6 categories)
- Discovered a clear, measurable fairness issue: the length of the resume influences skills extraction
  (r = 0.538); documented it rather than fixed without documenting, because current scoring formula is accurate

## Results
- Category-level accuracy of top-7 ranked: 40/42 correct in 6 categories
- Manual verification (resume content check by hand) for ranking in 3 categories
- Functional Streamlit prototype app (local)

## Limitations
- Fixed set of skill keywords – cannot identify any skills that are not on the list
- The same keyword has different meaning in various industries (e.g., "policy")
- Long resumes have an edge in scoring (proven, analyzed, unadjusted)
- Ranking corresponds to a specific job opening, not a general profile

Full debug log for each day and analysis: [PROJECT_LOG.md](PROJECT_LOG.md)