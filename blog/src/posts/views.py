from fastapi import APIRouter, Depends , Request

from pathlib import Path
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from database import get_db
from posts.models import Post

BASE_DIR = Path( __file__).resolve().parents[2] #корень приложения 
TEMPLATES_DIR = BASE_DIR / 'templates'

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))



router = APIRouter(
    prefix= '/posts' ,
    tags= ['Pages'] #для группировки обработчиков
)

@router.get('/')
async def list_posts_page( 
    request: Request, 
    db:Session = Depends(get_db)
    ):
    posts = db.query(Post).all()
    return templates.TemplateResponse(
        request=request, 
        name='posts/list.html', 
        context={
            'posts' : posts, 
        }


    )

