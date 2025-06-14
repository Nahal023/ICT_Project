import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# === Helper Functions ===
def load_notes():
    if os.path.exists('notes.json'):
        with open('notes.json', 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open('notes.json', 'w') as f:
        json.dump(notes, f, indent=4)

# === Initialize Notes ===
notes = load_notes()

# === Routes ===

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        note_text = request.form.get('note')
        if note_text:
            notes.append({'note': note_text})
            save_notes(notes)
            return redirect(url_for('view_notes'))
    return render_template('add_note.html')

@app.route('/view_notes', methods=['GET'])
def view_notes():
    return render_template('view_notes.html', notes=notes)

@app.route('/delete_note/<int:index>')
def delete_note(index):
    if 0 <= index < len(notes):
        notes.pop(index)
        save_notes(notes)
    return redirect(url_for('view_notes'))

@app.route('/edit_note/<int:index>')
def edit_note(index):
    if 0 <= index < len(notes):
        return render_template('edit_note.html', index=index, note=notes[index]['note'])
    return redirect(url_for('view_notes'))

@app.route('/update_note/<int:index>', methods=['POST'])
def update_note(index):
    if 0 <= index < len(notes):
        updated_text = request.form.get('note')
        if updated_text:
            notes[index]['note'] = updated_text
            save_notes(notes)
    return redirect(url_for('view_notes'))

if __name__ == '__main__':
    app.run(debug=True)



