from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from database import create_db_and_tables
from ai_router import router as ai_router
from stock_router import router as stock_router


app = FastAPI(title="BrewIntelligence - API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(ai_router)
app.include_router(stock_router)

@app.get("/")
def root():
    return {"message": "Backend connected to Frontend successfully!"}
