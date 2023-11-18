from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from dto.blog import BlogCreate, BlogUpdate
from auth.auth import oauth2_scheme, decode_access_token
from repository import blog as blog_repository

BlogRouter = APIRouter()

# @desc   get all blogs
# @route  GET /api/blog/
# @access Public
@BlogRouter.get("/")
def get_blogs(db: Session =  Depends(get_db)):
    return blog_repository.get_blogs(db)

# @desc   get a single blog by id
# @route  GET /api/blog/{blog_id}
# @access Public
@BlogRouter.get("/{blog_id}")
def get_blog(blog_id: str, db: Session =  Depends(get_db)  ):
    blog = blog_repository.get_blog(db, blog_id)
    if (blog):
        return blog
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
# @desc   create new blog
# @route  POST /api/blog/
# @access Private
@BlogRouter.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreate, db: Session =  Depends(get_db), token: str =Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = blog_repository.get_user_by_username(db=db, username=username)
    blog_with_author = blog.model_copy(update={"author_id":user.id})
    return blog_repository.create_blog(db=db, blog=blog_with_author)

# @desc   update a blog
# @route  PATCH /api/blog/{blog_id}
# @access Private
@BlogRouter.patch("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: str, blog : BlogUpdate , db: Session =  Depends(get_db), token: str =Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    new_blog = blog_repository.update_blog(db, blog_id, blog)
    if not new_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return new_blog

# @desc   delete a blog
# @route  DELETE /api/blog/{blog_id}
# @access Private
@BlogRouter.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: str, db: Session =  Depends(get_db), token: str =Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    blog = blog_repository.delete_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return


# @desc   get all blogs by author
# @route  GET /api/blog/author/{author_id}
# @access Public
@BlogRouter.get("/author/{author_id}")
def get_blogs_by_author(author_id: str, db: Session =  Depends(get_db)):
    return blog_repository.get_blogs_by_author(db, author_id)

