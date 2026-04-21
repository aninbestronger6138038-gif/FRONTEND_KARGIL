import { useState } from 'react'
import React from 'react'


function App() {
  const [text, setText] = useState("");
  const [notes, setNotes] = useState([]);
  const [editId, setEditId] = useState(null);

  const handleAddOrUpdate = () => {
    if (text.trim() === "") return;

    if (editId !== null) {
      const updatedNotes = notes.map((note) =>
        note.id === editId ? { ...note, text: text } : note
      );
      setNotes(updatedNotes);
      setEditId(null);
    } else {
      const newNote = {
        id: Date.now(),
        text: text,
      };
      setNotes([...notes, newNote]);
    }

    setText("");
  };

  const handleDelete = (id) => {
    const filteredNotes = notes.filter((note) => note.id !== id);
    setNotes(filteredNotes);

    if (editId === id) {
      setEditId(null);
      setText("");
    }
  };

  const handleEdit = (id) => {
    const noteToEdit = notes.find((note) => note.id === id);
    setText(noteToEdit.text);
    setEditId(id);
  };

  return (
    <div>
      <h2>Notes App</h2>

      <div >
        <input
          type="text"
          placeholder="Enter a note"
          value={text}
          onChange={(e) => setText(e.target.value)}
         
        />
        <button onClick={handleAddOrUpdate}>
          {editId !== null ? "Update Note" : "Add Note"}
        </button>
      </div>

      <div >
        {notes.map((note) => (
          <div key={note.id} >
            <p>{note.text}</p>
            <div >
              <button onClick={() => handleEdit(note.id)} >
                Update
              </button>
              <button onClick={() => handleDelete(note.id)} >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
