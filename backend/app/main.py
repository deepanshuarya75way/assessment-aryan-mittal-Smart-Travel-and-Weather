from __future__ import annotations



import asyncio 
import sys 
from pathlib import Path 
from contextlib import asynccontextmanager

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
  sys.path.insert(0,str(ROOT))



from fastapi import FastAPI


from backend.app.database import init_db
from backend.app.routers  import health,plans,trips,leads
from backend.app.services.lead_service import( init_leads_db, check_all_leads
)

async def availability_loop(): 
  while True:
    await asyncio.sleep(60)
    await asyncio.to_thread(check_all_leads)




@asynccontextmanager
async def lifespan(app:FastAPI):
  init_db()
  init_leads_db()
  task = asyncio.create_task(availability_loop())


  try:
    yield
  finally:
    task.cancel()
  
  try:
    await task
  except asyncio.CancelledError:
    pass
  


app=FastAPI(
  title="Smart Travel Weather Planning Agent",
  version="2.1.0",
  lifespan=lifesapn,
)
app.add_middleware( CORSMiddleware,
  allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
app.include_router(health.router)
app.include_router(plans.router)
app.include_router(trips.router)
app.include_router(leads.router
)

@app.get("/")
def root ():
  return{
    "message":"Smart Travel API running",
    "docs":"/docs"
  }

