"""Blogly application."""

from flask import Flask, redirect, render_template, request, url_for
from models import db, connect_db, User

app = Flask(__name__)

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Connect the database
connect_db(app)

# Create the tables within the application context
with app.app_context():
    db.create_all()

# Route: Redirect from '/' to the users list
@app.route('/')
def root():
    """Redirect to the list of users."""
    return redirect(url_for('list_users'))

# Route: Show all users
@app.route('/users')
def list_users():
    """Show all users."""
    users = User.query.all()
    return render_template('user_list.html', users=users)

# Route: Show the form to create a new user
@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Show form to create a new user."""
    return render_template('new_user_form.html')

# Route: Process the form to create a new user
@app.route('/users/new', methods=["POST"])
def create_user():
    """Process form submission for a new user."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('list_users'))

# Route: Show user details
@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details for a specific user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

# Route: Show the form to edit a user
@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user_form(user_id):
    """Show form to edit a specific user."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)

# Route: Process the form to edit a user
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Process form to edit a user."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()
    return redirect(url_for('show_user', user_id=user.id))

# Route: Delete a user
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a specific user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('list_users'))

if __name__ == "__main__":
    app.run(debug=True)
