# Resume Screening System — Future Interns Task 3

## Problem Statement

Automatic screening and ranking of resumes based on job description, extraction of candidate’s skills and identification of skill gaps.

## Data

Raw data is not present in this repo (see .gitignore). Dataset link: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
To replicate, download the CSV file and put it into Google Drive folder at FUTURE_ML_03/data/, or in data/ directory if run locally outside of Colab.

## Dataset

- **Source:** Kaggle - [Resume Dataset by snehaanbhawal]
- **Files:** Resume.csv, data-folder consisting all the resumes in pdf formats
- **Number of samples:** 2,484 resumes in total
- **Categories:** 24 in total
- **Categories used in this project:** Information-Technology, Engineering, Finance, Sales, HR, Healthcare
  (out of all 24 categories due to unique skill vocabulary in each of them, verified using word frequency analysis. CONSULTANT category was also considered, but excluded because of lack of distinctive terminology;
  DESIGNER was considered, but excluded because of overlap with ENGINEERING category)
- **Job Descriptions:** not present in the resume dataset; need to be separately sourced for each of the selected 6 categories, because this task requires comparison of resumes with specific job descriptions, not classification of resumes into categories

## Scope

Explore the resume dataset, perform cleaning and analysis of resumes, extract skills,
source job descriptions for selected categories, develop a resume-JD matching/score
algorithm, rank candidates, and uncover skill gaps compared to job descriptions.

## Approach (Outline)

Loading Data -> Selecting and Verifying Categories -> Text Cleaning -> Extracting Skills ->
Source Job Descriptions -> Resume-JD Similarity Matching -> Candidate Ranking ->
Skill Gaps Identification

## Progress (Day 1 of 10)

- Repository set up (FUTURE_ML_03)
- Dataset selection and download (from Kaggle)
- Environment setup (Colab + Drive)
- Dataset loading and exploration
- Select 6 categories using word-frequency analysis and drop 2 categories
(CONSULTANT, DESIGNER) due to poor categorical distinction
- Discovered the gap: need to source job descriptions separately (not in the original dataset)