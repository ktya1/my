from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from database import get_db

from users.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from users.models import User
from users.schemas import (
    Token,
    UserCreate,
    UserRead,
)


router = APIRouter(
    prefix='/api/users', 
    tags = ['Users API'],
)

@router.post(
    path='/register',
    response_model=UserRead
)

async def register(
    user: UserCreate, 
    db: Session = Depends(get_db),

) -> User:

    existing_user = (
        db.query(User).filter(user.username == user.username).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='Username already exists',
        )

    new_user = User(
        username = user.username,
        hashed_password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit
    db.refresh(new_user)

    return new_user



@router.post(
    path='/login',
    response_model=Token,
)

async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), #придут данные из формы ввода
    db: Session = Depends(get_db),
) -> dict[str, str]:
    db_user = (
        db.query(User)
        .filter(
            User.username == form_data.username,
        )
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail='Invalid username or password',
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail='Invalid username or password',
        )

    token = create_access_token(db_user.username)

    return {
        'access_token': token,
        'token_type': 'bearer',
    }


@router.get(
    path='/profile',
    response_model=UserRead
)

async def profile(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user

