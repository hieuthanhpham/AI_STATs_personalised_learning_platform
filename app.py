import streamlit as st
import requests

st.title("AI-Powered Feedback System")

st.subheader("Student Submission Portal")
student_answer = st.text_area("Submit your open-ended answer here:")

if st.button("Get Feedback"):
    response = requests.post("http://backend:8000/predict", json={"answer": student_answer})
    if response.status_code == 200:
        data = response.json()
        st.write("### Feedback")
        st.write(f"Matched Concept: {data['matched_answer']}")
        st.write(f"Similarity Score: {data['similarity_score']:.2f}")
    else:
        st.error("Backend not available. Please check the server status.")
