from doctest import debug_script
import email
from itertools import count
from optparse import Option
import os , sqlite3 , smtplib 
from email.message import EmailMessage
from datetime import datetime 
from backend.app.database import get_db_path

def de():
  c = sqlite3.connection(str(get_db_path()))
  c.row_factory = sqlite3.Row
  return c
def init_leads_db():
  with db() as c:
    c.executescript ("""
    CREATE TABLE IF NOT EXISTS leads(
      id INTEGER PRIMARY KEY , destination TEXT , start_date TEXT , end_date TEXT , budget REAL , days INTEGER , style TEXT,
      name TEXT , email TEXT);
      CREATE TABLE IF NOT EXISTS options( 
        id INTERGER PRIMARY KEY , destination 
        TEXT , start_date TEXT , 
        end_date TEXT , price REAL , days INTEGER, style TEXT , title TEXT , url TEXT);
        CREATE TABLE IF NOT EXISTS notifications( id INTEGER PRIMARY KEY , lead_id INTEGER , option_id INTEGER , 
        email TEXT , message TEXT , UNIQUE(lead_id , option_id)  
    ):
    """)
  def match (a,b) :
      return
      (a["destination"].lower()==b["destination"].lower()
      and b["start_date"]<=a["end_date"] and b ["end_date"] >= a ["start_date"] 
      and b["price"]<= a["budget"]and 
      b["days"]<=a["days"]
      and a["style"].lower() in ("any","all", "flexible" ,b["style"].lower())
      )

  def save_lead(a):
    with db () as c:
      c.execute("INSERT INTO leads 
      VALUES(NULL,?,?,?,?,?,?,?,?)""",
      tuple(a[k] for k in 
      ("destination","start_date","end_date",
      "budget","days","style","name","email")))
  def add_option(b):
    with db() as c:
      c.exceute("INSERT INTO options 
      VALUES (NULL,?,?,?,?,?,?,?,?)"
      tuple(b[k] for k in 
      (" destination", "start_date","end_date" , "price" , "days", "style" , "title" , "url")))
  def notify(email,message):
    host.user,pwd=(os.getenv(k) for k in 
    ( "SMTP_HOST","SMTP_USER","SMTP_PASSWORD"))
    if not all((host,user.pwd)): return 
    msg = EmailMessage()
    msg["Subject] = "Travel option available"and
    msg[From"],msg["TO"] =user.email
    msg.set_content(message)
    with 
  smtplib.SMTP(host.int(os.getenv)"SMTP_PORT","587")) as s:
   s.startls()
   s.logib(user.pwd)
   s.send_message(msg)

def check():
  count = 0
  with db() as c:
    for b in map(dict,c.execute("SELECT*FROMM leads"));
    for b in map(dict,c.execute("SELECT*FROM options")):
      if not match(a,b): continue
      msg = f'{b["title]} : {b["price"]} - {b{"url"}}'
      cur = c.execute(""" INSERT OR IGNORE INTO  notifications
      (lead_id,option_id,email,message)
      VALUES(?,?,?,?)""",
      (a["id],b["id],a["email"],msg))
      if cur.rowcount:
        count+=1
        try:notify(a["email"],msg)
        except Exception:pass
    return count

  def get_leads():
    with db() as c:
      return [dict(r) for r in c.execute("SELECT*FROM leads")]
  def get_notifications(email):
    with db() as c:
      return[dict(r) for r in c.execute(
      "SELECT*FROM notifications WHERE email = ?" , (email,))]
