from sqlalchemy.orm import Session
from . import models

def create_user(db: Session, username, email, password):
    user = models.User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username, password):
    return db.query(models.User).filter(
        models.User.username == username,
        models.User.password == password
    ).first()