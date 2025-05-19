from sqlalchemy import Column, Integer, String, Float, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./feedback_log.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class FeedbackLog(Base):
    __tablename__ = "feedback_log"
    id = Column(Integer, primary_key=True, index=True)
    student_answer = Column(String)
    matched_answer = Column(String)
    similarity_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

def log_feedback(student_answer, matched_answer, similarity_score):
    db = SessionLocal()
    log_entry = FeedbackLog(
        student_answer=student_answer,
        matched_answer=matched_answer,
        similarity_score=similarity_score
    )
    db.add(log_entry)
    db.commit()
    db.close()
