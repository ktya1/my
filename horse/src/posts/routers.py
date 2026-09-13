from fastapi import APIRouter, Depends, HTTPException, status
from posts.schemas import PostRead, PostCreate , PostUpdatePatch, PostPut
from sqlalchemy.orm import Session
from database import get_db
from posts.models import Post

router = APIRouter(
    prefix = '/api/posts',
    tags= ['API']
)


@router.get('/', response_model=list[PostRead])
async def list_posts(db:Session = Depends(get_db)):
    return db.query(Post).all()


@router.post('/', response_model= PostRead)
async def create_posts(
    data: PostCreate,
    db:Session = Depends(get_db)
):
    post = Post(
        title = data.title,
        content = data.content,
    )


    db.add(post)
    db.commit()

    db.refresh(post)#обнова состояния из db(добавление айди)

    return post


#удаление постаs
@router.delete("/{post_id}") # post_id , как и в 38 строчке(переход на пост)
async def delete_post(
    post_id: int, 
    db: Session = Depends(get_db)
    ):
    if post_id <= 0:
            raise HTTPException(status_code=404, detail="this value cannot be negative")

    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    db.delete(post)
    db.commit()

#извлечение одного поста
@router.get('/{post_id}', response_model=PostRead)
async def get_post_one(post_id: int, db: Session = Depends(get_db)):

    if post_id <= 0:
        raise HTTPException(status_code=400, detail="this value cannot be negative")
    post = db.query(Post).filter(Post.id == post_id).first() 
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")  
    return post

#изменение поста жестким put
@router.put('/{post_id}', response_model= PostRead)
async def update_post_put(
    post_id: int, 
    data: PostPut,
    db: Session = Depends(get_db)
):

    post = db.get(Post, post_id)
    

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")


    post.title = data.title
    post.content = data.content
    
    db.commit()
    db.refresh(post)

    return post

#изменение поста мягким patch
@router.patch('/{post_id}', response_model= PostRead)
async def update_post_put(
    post_id:int, 
    data: PostUpdatePatch,
    db: Session = Depends(get_db), 
    
):
    
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(status_code=404, detail='post not found')

    if data.title is not None:
        post.title = data.title

    if data.content is not None:
        post.content = data.content

    db.commit()
    db.refresh(post)

    return post