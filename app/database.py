from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(String(50), nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(50), nullable=False)
    original_plan = Column(Text, default="")
    updated_plan = Column(Text, default="")
    nutrition_tip = Column(Text, default="")
    feedback = Column(Text, default="")

def init_db(): Base.metadata.create_all(bind=engine)
def get_user(user_id):
    db=SessionLocal()
    try: return db.query(User).filter(User.user_id==user_id).first()
    finally: db.close()
def save_user(data):
    db=SessionLocal()
    try:
        user=User(**data); db.add(user); db.commit(); return user
    finally: db.close()
def save_plan(user_id, plan, nutrition_tip):
    db=SessionLocal()
    try:
        u=db.query(User).filter(User.user_id==user_id).first()
        if u: u.original_plan=plan; u.updated_plan=plan; u.nutrition_tip=nutrition_tip; db.commit()
    finally: db.close()
def update_plan(user_id, plan, feedback):
    db=SessionLocal()
    try:
        u=db.query(User).filter(User.user_id==user_id).first()
        if u: u.updated_plan=plan; u.feedback=feedback; db.commit()
    finally: db.close()
def get_all_users():
    db=SessionLocal()
    try: return db.query(User).order_by(User.id.desc()).all()
    finally: db.close()
def delete_user(user_id):
    db=SessionLocal()
    try:
        u=db.query(User).filter(User.user_id==user_id).first()
        if u: db.delete(u); db.commit()
    finally: db.close()
