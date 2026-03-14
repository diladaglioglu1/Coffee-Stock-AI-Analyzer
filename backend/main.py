from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Bunu ekle
from database import create_db_and_tables
from ai_router import router as ai_router

app = FastAPI(title="BrewIntelligence - API")

# --- CORS AYARLARI BURAYA ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında her yerden gelen isteğe izin verir
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST vb. tüm metodlara izin verir
    allow_headers=["*"],  # Tüm başlıklara (header) izin verir
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(ai_router)

@app.get("/")
def root():
    return {"message": "Backend connected to Frontend successfully!"}
