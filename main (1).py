from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date
import pymysql
import random
import hashlib
from fastapi.security import OAuth2PasswordBearer

# FastAPI app instance
app = FastAPI()

# OAuth2 setup (placeholder)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database connection setup
def get_connection():
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",  # replace with your DB username
        password="",  # replace with your DB password
        database="dcr_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Pydantic Models for Tables
class About(BaseModel):
    id: Optional[int]
    description: str
    system_developer: str
    date_created: date

class Activities(BaseModel):
    id: Optional[int]
    activity_name: str
    description: str
    day: str

class Chores(BaseModel):
    id: Optional[int]
    chores_name: str
    description: str
    day: str

class Guides(BaseModel):
    id: Optional[int]
    guide_name: str
    guide_description: str
    image: str

class MotivationalQuote(BaseModel):
    id: Optional[int]
    quote: str

# Utility function for hashing passwords
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------- CRUD Operations for "chores" -------------------
@app.post("/chores/")
def add_chores(chores: Chores):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO chores (chores_name, description, day) VALUES (%s, %s, %s)"
        cursor.execute(sql, (chores.chores_name, chores.description, chores.day))
        conn.commit()
    return {"message": "Chore added successfully"}

@app.get("/chores/")
def view_chores():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM chores")
        chores = cursor.fetchall()
    return chores

@app.put("/chores/{id}")
def update_chores(id: int, chores: Chores):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE chores SET chores_name=%s, description=%s, day=%s WHERE id=%s"
        cursor.execute(sql, (chores.chores_name, chores.description, chores.day, id))
        conn.commit()
    return {"message": "Chore updated successfully"}

@app.delete("/chores/{id}")
def delete_chores(id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM chores WHERE id=%s", id)
        conn.commit()
    return {"message": "Chore deleted successfully"}

# ---------------- CRUD Operations for "guides" -------------------
@app.post("/guides/")
def add_guide(guide: Guides):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO guides (guide_name, guide_description, image) VALUES (%s, %s, %s)"
        cursor.execute(sql, (guide.guide_name, guide.guide_description, guide.image))
        conn.commit()
    return {"message": "Guide added successfully"}

@app.get("/guides/")
def view_guides():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM guides")
        guides = cursor.fetchall()
    return guides

@app.put("/guides/{id}")
def update_guide(id: int, guide: Guides):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE guides SET guide_name=%s, guide_description=%s, image=%s WHERE id=%s"
        cursor.execute(sql, (guide.guide_name, guide.guide_description, guide.image, id))
        conn.commit()
    return {"message": "Guide updated successfully"}

@app.delete("/guides/{id}")
def delete_guide(id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM guides WHERE id=%s", id)
        conn.commit()
    return {"message": "Guide deleted successfully"}

# ---------------- CRUD Operations for "motivational_qoute" -------------------
@app.post("/quotes/")
def add_quote(quote: MotivationalQuote):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO motivational_qoute (quote) VALUES (%s)"
        cursor.execute(sql, (quote.quote,))
        conn.commit()
    return {"message": "Quote added successfully"}

@app.get("/quotes/")
def view_quotes():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM motivational_qoute")
        quotes = cursor.fetchall()
    return quotes

@app.put("/quotes/{id}")
def update_quote(id: int, quote: MotivationalQuote):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE motivational_qoute SET quote=%s WHERE id=%s"
        cursor.execute(sql, (quote.quote, id))
        conn.commit()
    return {"message": "Quote updated successfully"}

@app.delete("/quotes/{id}")
def delete_quote(id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM motivational_qoute WHERE id=%s", id)
        conn.commit()
    return {"message": "Quote deleted successfully"}

# ---------------- CRUD Operations for "activities" -------------------
@app.post("/activities/")
def add_activity(activity: Activities):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO activities (activity_name, description, day) VALUES (%s, %s, %s)"
        cursor.execute(sql, (activity.activity_name, activity.description, activity.day))
        conn.commit()
    return {"message": "Activity added successfully"}

@app.get("/activities/")
def view_activities():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM activities")
        activities = cursor.fetchall()
    return activities

@app.put("/activities/{id}")
def update_activity(id: int, activity: Activities):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE activities SET activity_name=%s, description=%s, day=%s WHERE id=%s"
        cursor.execute(sql, (activity.activity_name, activity.description, activity.day, id))
        conn.commit()
    return {"message": "Activity updated successfully"}

@app.delete("/activities/{id}")
def delete_activity(id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM activities WHERE id=%s", id)
        conn.commit()
    return {"message": "Activity deleted successfully"}

# ---------------- CRUD Operations for "about" -------------------

# ----------------- View Chores by Day (Monday to Sunday) -------------------
@app.get("/chores/day/{day}")
def view_chores_by_day(day: str):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM chores WHERE day=%s"
        cursor.execute(sql, (day,))
        chores = cursor.fetchall()
    if not chores:
        raise HTTPException(status_code=404, detail="No chores found for the given day")
    return chores

# ----------------- View 1 Random Quote Every Day -------------------
@app.get("/quote/random")
def view_random_quote():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM motivational_qoute")
        quotes = cursor.fetchall()
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found")
    return random.choice(quotes)

# ----------------- Register and Login for Admin -------------------
@app.post("/admin/register")
def register_admin(username: str, password: str):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "INSERT INTO admin (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))
        conn.commit()
    return {"message": "Admin registered successfully"}

@app.post("/admin/login")
def login_admin(username: str, password: str):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "username": username}


# ----------------- Run the Server -------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
