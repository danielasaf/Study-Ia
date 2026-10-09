from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import Base, engine
from models import usuario, plano
from routers import auth, plano as plano_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Study IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6767", "http://127.0.0.1:6767",
                   "http://localhost:5500", "http://127.0.0.1:5500",
                   "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,         prefix="/auth",  tags=["Autenticação"])
app.include_router(plano_router.router, prefix="/plano", tags=["Planos"])

@app.get("/")
def root():
    return {"status": "Study IA online 🚀"}
