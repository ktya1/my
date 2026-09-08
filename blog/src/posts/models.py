from database import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String,  Text

class Post(Base):
    __tablename__ = 'posts'
    #mapped - связь между типами данных. Помогает среде разработке
    id: Mapped[int] = mapped_column(
        primary_key = True
    )

    title: Mapped[str] = mapped_column(
        String(200), # ограничение 200 символов
        nullable=False, 
        
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    