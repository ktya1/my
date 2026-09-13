from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = 'sqlite:///./blog.db'


engine = create_engine(
    DATABASE_URL,
    connect_args = {
        'check_same_thread': False
    }
) #'скрытые' подключения к бд, которые он хранит

#фабрика - класс, который что-то производит(sessionmaker) - мост
#cecсия - работяга на мосту
SessionLocal = sessionmaker(
    bind = engine, 
    autocommit = False, 
    autoflush = False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db   
    finally:
        db.close()