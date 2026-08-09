import streamlit as st
import pandas as pd
import numpy as np
import pickle
import spacy

st.title("Resume Screening System")
st.write("Rank resumes against a job description and identify skill gaps.")

# Load data
@st.cache_data
def load_data():
    df_resume = pd.read_pickle('data/df_cleaned_resume.pkl')
    df_jd = pd.read_pickle('data/df_cleaned_jd.pkl')
    similarity_matrix = np.load('data/similarity_matrix.npy')
    return df_resume, df_jd, similarity_matrix

df_cleaned_resume, df_cleaned_jd, similarity_matrix = load_data()

st.write(f"Loaded {df_cleaned_resume.shape[0]} resumes and {df_cleaned_jd.shape[0]} job descriptions.")

st.header("Find Candidates for a Job Role")

selected_category = st.selectbox(
    "Select a job category:",
    options=list(df_cleaned_jd['category'])
)

top_n = st.slider("Number of candidates to show:", min_value=3, max_value=20, value=7)

def skill_overlap_score(resume_skills, jd_skills):
    if len(jd_skills) == 0:
        return 0.0
    overlap = set(resume_skills) & set(jd_skills)
    return len(overlap) / len(jd_skills)

def identify_missing_skills(resume_skills, jd_skills):
    missing = set(jd_skills) - set(resume_skills)
    return list(missing)

def full_candidate_report(jd_category, top_n=10):
    jd_idx = list(df_cleaned_jd['category']).index(jd_category)
    jd_skills = df_cleaned_jd.iloc[jd_idx]['extracted_skills']
    
    results = df_cleaned_resume.copy()
    results['similarity_score'] = similarity_matrix[:, jd_idx]
    results['skill_overlap'] = results['extracted_skills'].apply(lambda skills: skill_overlap_score(skills, jd_skills))
    results['combined_score'] = (0.7 * results['similarity_score']) + (0.3 * results['skill_overlap'])
    results['missing_skills'] = results['extracted_skills'].apply(lambda skills: identify_missing_skills(skills, jd_skills))
    
    min_score = results['combined_score'].min()
    max_score = results['combined_score'].max()
    results['match_percentage'] = ((results['combined_score'] - min_score) / (max_score - min_score) * 100).round(1)
    
    ranked = results.sort_values('combined_score', ascending=False)
    return ranked[['Category', 'match_percentage', 'missing_skills']].head(top_n)

if st.button("Rank Candidates", key="rank_button"):
    st.session_state['report'] = full_candidate_report(selected_category, top_n)

if 'report' in st.session_state:
    report = st.session_state['report']
    st.dataframe(report)
    
    st.subheader("View Resume Details")
    selected_resume_idx = st.selectbox("Select a resume to view:", options=report.index, key="resume_select")
    
    if st.button("Show Resume Text", key="show_resume_button"):
        st.write(df_cleaned_resume.loc[selected_resume_idx, 'Resume_str'][:1500])