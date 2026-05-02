"""
=========================================================
Nom du fichier : models.py
Description : Définition des modèles de données (tables) pour la base de données.
Objectif : Représenter la structure des tables de la base de données sous forme de classes Python (ORM).
Fonctionnement : Définit les colonnes, les types de données et les relations pour les tables 'users', 'messages', etc. à l'aide de SQLAlchemy.
=========================================================
"""

from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_banned = Column(Boolean, default=False)

    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), nullable=False) # 'user' ou 'assistant' ou 'system'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")

    def __repr__(self):
        return f"<Message(role={self.role}, user_id={self.user_id})>"
