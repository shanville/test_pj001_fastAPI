# main.py
from models import User, Base  # 相対インポートから絶対インポートに変更
from database import engine, SessionLocal
from schemas import UserCreate  # 必要に応じて他のファイルも同様に修正

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[UserCreate])  # レスポンスモデルの型を適切に設定
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

