import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapped_column

database_url = 'sqlite:///test.db'
engine = create_engine(database_url)
Base = declarative_base()


class Player(Base):
    __tablename__ = 'players_table'

    id_ = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    result_id = relationship("Result", back_populates="player")


class Result(Base):
    __tablename__ = 'results'

    id_ = Column(Integer, primary_key=True)
    player_id = mapped_column(ForeignKey("players_table.id_"))
    words_per_minute = Column(Integer, )
    player = relationship("Player", back_populates="result_id")
