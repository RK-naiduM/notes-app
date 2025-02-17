import React, { useState, useEffect } from "react";
import axios from "axios";

function NotesApp() {
    const [notes, setNotes] = useState([]);
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");

    // Fetch notes when the component loads
    useEffect(() => {
        axios.get("http://127.0.0.1:8000/notes")
            .then(response => {
                setNotes(response.data);
            })
            .catch(error => {
                console.log("There was an error fetching the notes:", error);
            });
    }, []);

    // Handle creating a new note
    const handleCreateNote = () => {
        axios.post("http://127.0.0.1:8000/notes", { title, content })
            .then(response => {
                // Fetch updated list of notes after creating a new one
                axios.get("http://127.0.0.1:8000/notes")
                    .then(response => {
                        setNotes(response.data);
                        setTitle("");
                        setContent("");
                        alert("Note created successfully!");
                    })
                    .catch(error => {
                        console.log("Error fetching notes:", error);
                    });
            })
            .catch(error => {
                console.log("Error creating note:", error);
            });
    };
    

    return (
        <div>
            <h1>Notes App</h1>

            <div>
                <h2>Create a New Note</h2>
                <input
                    type="text"
                    placeholder="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <textarea
                    placeholder="Content"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                />
                <button onClick={handleCreateNote}>Add Note</button>
            </div>

            <div>
                <h2>All Notes</h2>
                <ul>
                    {notes.map((note) => (
                        <li key={note.id}>
                            <h3>{note.title}</h3>
                            <p>{note.content}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default NotesApp;
