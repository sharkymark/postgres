import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for flash messages

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        return conn
    except psycopg2.OperationalError as e:
        app.logger.error(f"Database connection error: {e}")
        # In a real app, you might want to handle this more gracefully
        # For this example, we'll let the error propagate up
        raise

@app.route('/')
def index():
    """Displays all entries from the table."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email, started_on FROM mytable ORDER BY started_on DESC')
    entries = cur.fetchall()
    cur.close()
    conn.close()
    # Convert datetime objects to strings for display if needed
    entries_display = [
        (id, name, email, started_on.strftime('%Y-%m-%d %H:%M:%S') if started_on else None)
        for id, name, email, started_on in entries
    ]
    return render_template('index.html', entries=entries_display)

@app.route('/add', methods=('GET', 'POST'))
def add():
    """Handles adding a new entry."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        started_on_str = request.form['started_on']

        if not name or not email:
            flash('Name and Email are required!', 'error')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                # Handle optional timestamp
                started_on = datetime.fromisoformat(started_on_str) if started_on_str else datetime.now()
                cur.execute('INSERT INTO mytable (name, email, started_on) VALUES (%s, %s, %s)',
                            (name, email, started_on))
                conn.commit()
                flash('Entry added successfully!', 'success')
            except (ValueError, psycopg2.Error) as e:
                 flash(f'Error adding entry: {e}', 'error')
                 conn.rollback() # Rollback in case of error
            finally:
                cur.close()
                conn.close()
            return redirect(url_for('index'))

    # For GET request, just show the form part of index.html
    # Or redirect back to index which includes the form
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    """Handles editing an existing entry."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email, started_on FROM mytable WHERE id = %s', (id,))
    entry = cur.fetchone()
    cur.close()

    if not entry:
        flash(f'Entry with id {id} not found.', 'error')
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        started_on_str = request.form['started_on']

        if not name or not email:
            flash('Name and Email are required!', 'error')
            # Re-fetch entry data to pass back to the template on error
            entry_display = (entry[0], entry[1], entry[2], entry[3].isoformat() if entry[3] else '')
            return render_template('edit.html', entry=entry_display)
        else:
            try:
                started_on = datetime.fromisoformat(started_on_str) if started_on_str else entry[3] # Keep original if empty
                cur = conn.cursor()
                cur.execute('UPDATE mytable SET name = %s, email = %s, started_on = %s WHERE id = %s',
                            (name, email, started_on, id))
                conn.commit()
                flash('Entry updated successfully!', 'success')
            except (ValueError, psycopg2.Error) as e:
                 flash(f'Error updating entry: {e}', 'error')
                 conn.rollback()
            finally:
                if cur: cur.close()
                conn.close()
            return redirect(url_for('index'))

    conn.close()
    # Format timestamp for the input field
    entry_display = (entry[0], entry[1], entry[2], entry[3].isoformat(sep='T', timespec='minutes') if entry[3] else '')
    return render_template('edit.html', entry=entry_display)


@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    """Handles deleting an entry."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM mytable WHERE id = %s', (id,))
        conn.commit()
        flash('Entry deleted successfully!', 'success')
    except psycopg2.Error as e:
        flash(f'Error deleting entry: {e}', 'error')
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Use environment variables for host and port if available
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    app.run(host=host, port=port, debug=True) # Enable debug for development
