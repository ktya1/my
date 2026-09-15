from fastapi import FastAPI
import sqlite3 
from pydantic import BaseModel

app = FastAPI()

conn = sqlite3.connect('news.db', check_same_thread = False)



conn.execute('''
             create table if not exists news (
                id integer primary key autoincrement,
                title text not null,
                content text not null
            )
        ''')
conn.commit()

class NewsCreate(BaseModel):
    title:str
    content:str


class NewsList(NewsCreate):
    id:int


@app.get('/api/news', response_model=list[NewsList])
def get_news():
    cursor = conn.execute(
            'select * from news'
    )

    news = cursor.fetchall()

    return [
        NewsList(id=id, title=title, content=content) 
        for id, title, content in news
    ]

@app.post('/api/news', response_model=NewsList)
def create_news(news:NewsCreate):
    cursor = conn.execute(
                'insert into news (title, content) value (?,?)',
                (news.title, news.content)
    )

    conn.commit()
    return NewsList(
        id=cursor.lastrowid,
        title=news.title,
        content=news.content
    )
    