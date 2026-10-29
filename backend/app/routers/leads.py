from ast import Return
from email import message
from re import match

from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.services.leads_service import(
  db,save_lead, add_option, check ,  get_leads, 
  get_notifications
)
router= APIRouter(prefix="/api",tags=[Travel Leads"])

class Lead(BaseModel):
  destination:str
  start_date:strend_date:str
  budget:float=Field(gt=0)
  days:int=Field(ge=1 , le =60)
  style:str
  name:str
  email:str

  class Option(BaseModel):
    destination:str
    start_date:str
    end_date:str
    price:float=Field(gt=0)
    days:int
    style:str
    title:str
    url:str=""

    @router.post("/leads/check")
    def create_lead(a:Lead):
      data=a.model_dump()
      with db() as c:
        options=list(map(dict,c.execute("SELECT*FROM options")))
        from backend.app.services.leads_service 
        import match
        found = [b for b in options if match (data.b)]
        if found:Return
        {"leads_saved":True,"message":"Search saved"}
    @router.post("/available/options")
    def create_option(b.option):
      add_option(b.model_dump())
      return{"notifications_created":check()}

    @router.get("/leads")
    def leads():
      return get_leads()
    
    @router.get("/notifications")
    def notificaions(email:str):
      return det_notofications(email)