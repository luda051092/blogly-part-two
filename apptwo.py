from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cake'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():

   posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
   return render_template("posts/homepage.html", posts=posts)
 
@app.errorhandler(404)
def page_not_found(e):
   
   return render_template('404.html'), 404
########################################################
# User route
@app.route('/users')
def users_index():
    """Show page w info on all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():

    return render_template('users/new.html')

@app.route('/users/new', methods=[POST])
def users_new():
    """Handle form submission for creating user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")
    
    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show page w info on specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id/edit')
def users_edit(user_id):
    """Show form to edit existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating exisiting user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")
    
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Deleting existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")



##########################################################
# Posts route

 @app.route('/users/<int:user_id>/posts/new')
    def post_new_form(user_id):
        """Display form to handle new posts on a per user basis"""

        user = User.query.get_or_404(user_id)
       

        return render_template('post_new.html', user=user)

    @app.route('/users/int:user_id>/posts/new', methods=["POST"])
    def post_new(user_id):
        """Submit post request on form submit to add blog to db"""

        user = User.query.get_or_404(user_id)
        new_post = Post(title=request.form['title'],
                        content=request.form['content'],
                        user=user)


        db.session.add(new_post)
        db.session.commit()
        flash(f"Post '{new_post.title}' added.")

        return redirect(f"/users/{user_id}")

        @app.route('/posts/<int:post_id>')
        def posts_show(post_id):
            """Show page w info on specific post"""

            post = Post.query.get_or_404(post_id)
            return render_template('posts/show.html', post=post)

        @app.route('/posts/<int:post_id>/edit')
        def posts_edit(post_id):
            """Form to edit posts"""

            post = Post.query.get_or_404(post_id)
            return render_template('post_edit.html', post=post)

        @app.route('/posts/<int:post_id>/edit', methods=["POST"])
        def post_update(post_id):
            """Handle editing per post id"""

            post = Post.query.get_or_404(post_id)
            post.title = request.form['title']
            post.body = request.form['body']

            db.session.add(post)
            db.session.commit()
            flash(f"Post '{post.title}' edited.")

            
            return redirect(f"/users/ {post.user_id}")

        @app.route('/posts/<int:post_id>/delete', methods=["POST"])
        def post_delete(post_id):
            """Deletes a specified post"""

            post = Post.query.get_or_404(post_id)

            db.session.delete(post)
            db.session.commit()
            flash(f"Post '{post.title}' deleted.")

            return redirect(f"/users/ {post.user_id}")
        
        