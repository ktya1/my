from fastapi import APIRouter, Depends , Request, Form, status, HTTPException
from fastapi.responses import RedirectResponse

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


@router.get('/create')
async def create_post_page(
    request: Request
    ):
    return templates.TemplateResponse(
        request=request,
        name='posts/create.html'
    )


@router.post('/create')
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    all: str = Form(...),
    db: Session = Depends(get_db)
):
    

    post = Post(
        title=title,
        content=content, 
        all = all,
    )
        
    db.add(post)
    db.commit()
    db.refresh(post)

    return RedirectResponse(
        url='/posts',
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get('/{post_id}')
async def get_post_one_page(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )

    return templates.TemplateResponse(
        request=request,
        name='posts/get_one.html',
        context={'post': post}
    )


@router.get("/{post_id}/patch")
async def patch_post_page(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
        request=request,
        name="posts/patch_post.html",
        context={"post": post},
    )


@router.post("/{post_id}/patch")
async def update_post(
    post_id: int,
    title: str | None = Form(default=None),
    content: str | None = Form(default=None),
    all: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if title is not None and title.strip():
        post.title = title.strip()
    if content is not None and content.strip():
        post.content = content.strip()
        
    if all is not None and all.strip():
        post.all = all.strip()

    db.commit()
    db.refresh(post)

    return RedirectResponse(url="/posts", status_code=status.HTTP_303_SEE_OTHER)


