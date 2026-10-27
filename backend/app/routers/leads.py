from datetime import date 
from fastapi import APIRouter , HTTPException
from pydantic import BaseModel , EmailStr , Field
from backend.app.database import get_connection
 
 router = APIRouter(prefix="/api/leads" , tags=["Travel Leads"])
 class LeadRequest(BaseModel):
  destination: str
  travel_date:date
  budget: float = Field(gt=0)
  duration: int = Field(gt=0,le=60)
  travel_style: str = "Any" email : EmailStr

  def init_leads_db():
    with get_Connection() as db:
      db.execute("" CREATE TABLE IF NOT EXISTS travel_leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT , destination TEXT NOT NULL , travel_date TEXT NOT NULL, budget REAL NOT NULL , duration INTEGER NOT NULL , 
        travel_style TEXT NOT NULL , 
        email TEXT NOT NULL , notified_options TEXT NOT NULL DEFAULT '', 
        create_at TEXT DEFAULT CURRENT_TIMESTAMP )
          """)
          db.execute("""
          CREATE TABLE IF NOT EXISTS travel_options(
            id INTEGER PRIMARY KEY AUTOINCREMENT , 
            destination TEXT NOT NULL , 
            travle_date TEXT NOT NULL,
             price REAL NOT NULL , details TEXT NOT NULL)

          """)
@router.post("")
def save_lead(lead: LeadRequest):
  init_leads_db()
  with get_connection() as db:
    cur = db.execute("""
    INSERT INTO travel_leads (
      destination , travel_date, budget , duration , travel_style  , email)
      VALUES(?,?,?,?,?,?) """ , (
      lead.destination.strip(), lead.travel_date.isoformat(),
      lead.budget , lead.duration , lead.travel_style, str(lead.email)
      )
    )
    return {"lead_id":
    cur.lastrowid , "message": "Travel alert saved"}

    @router.get("")
    def list_leads():
      init_leads_db()
      with get_connection() as db:
        rows = db. execute("""
        SELECT id , destination, travel_date , budget , duration , travel_style , email FROM travel_leads ORDER By id DESC """ ).fetchall() 
        return [dict(row) for row in rows] 
        @router.post("/options")
        def add_available = option( destination : str , 
        travel_date: date , 
        price: float = Field(gt=0),
        details : str = "Travel option available"):
         init_leads_db() withget_Connection() as db:
         cur = db.execute(""" 
          INSERT INTO travel_options ( destination , travel_date. price , details)
          VALUES(?,?,?,?) """ , ( destination.strip() , travel_date.isoformat() , price , details ))
          returns {"option_id": cur.lastrowid , "message": " option added"}
      @router.post("/check")
      def check_available_options():
        init_leads_db()
        alerts = []

        with get_connections () as db :
          leads = db.execute (" SELECT * FROM travel)
           