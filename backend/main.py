from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from database import get_db_connection

app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define Note model
class Note(BaseModel):
    title: str
    content: str

# (GET) Fetch All Notes
@app.get("/notes")
def get_notes():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    
    # Access rows as dictionaries
    return [{"id": note["id"], "title": note["title"], "content": note["content"]} for note in notes]

# (POST) Add a New Note
@app.post("/notes")
def create_note(note: Note):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (note.title, note.content))
    conn.commit()
    conn.close()
    return {"message": "Note created successfully!"}

# (GET) Fetch a Single Note by ID
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {"id": note["id"], "title": note["title"], "content": note["content"]}

# (PUT) Update a Note
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (updated_note.title, updated_note.content, note_id))
    conn.commit()
    conn.close()
    
    return {"message": "Note updated successfully!"}

# (DELETE) Delete a Note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Note deleted successfully!"}
