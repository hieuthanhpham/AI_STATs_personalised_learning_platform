from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch
from database import log_feedback

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

class AnswerRequest(BaseModel):
    answer: str

@app.post("/predict")
def predict_feedback(request: AnswerRequest):
    ideal_answers = [
        "The expected value of a discrete random variable is the weighted average of all possible values.",
        "A binomial distribution describes the number of successes in n independent trials."
    ]
    embeddings = model.encode(ideal_answers, convert_to_tensor=True)
    student_embedding = model.encode(request.answer, convert_to_tensor=True)
    similarity_scores = util.cos_sim(student_embedding, embeddings)
    best_match = int(similarity_scores.argmax())

    log_feedback(request.answer, ideal_answers[best_match], float(similarity_scores[0][best_match]))

    return {
        "matched_answer": ideal_answers[best_match],
        "similarity_score": float(similarity_scores[0][best_match])
    }
