from sqlalchemy.orm import Session

from models.blog import Blog 
from dto.blog import BlogCreate, BlogUpdate

def get_blogs(db: Session):
    return db.query(Blog).all()

def get_blog(db: Session, id: str):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog

def create_blog(db: Session, blog: BlogCreate):
    db_blog = Blog(title=blog.title, body=blog.body, author_id= blog.author_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_blog(db: Session, id: str, bew_blog: BlogUpdate):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog: 
        return None
    for field, value in bew_blog:
        if value is not None:
            setattr(blog, field, value)
    db.commit()
    return blog


def delete_blog(db: Session, id: str):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog: 
        return None
    db.delete(blog)
    db.commit()
    return blog

def get_blogs_by_author(db: Session, id: str):
    return db.query(Blog).filter(Blog.author_id == id).all()