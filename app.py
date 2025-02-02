from flask import Flask, redirect, url_for, session, render_template, request
import os
import diary_login  # User authentication module
import diary_messages  # Diary messages module
from werkzeug.utils import secure_filename  # For handling file uploads

app = Flask(__name__)
app.secret_key = 'YourSecretKeyHere'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home Page (Diary Messages)
@app.route('/')
def index():
    if not diary_login.is_login():
        return redirect('/login')

    user = diary_login.get_user()
    messages = diary_messages.load_messages(user)

    return render_template('index.html', user=user, messages=messages)


# Login Page
@app.route('/login')
def login():
    return render_template('login.html')


# Signup Page
@app.route('/signup')
def signup():
    return render_template('signup.html')


# Process Login
@app.route('/try_login', methods=['POST'])
def try_login():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')

    if diary_login.try_login(user, pw):
        return redirect('/')

    return show_msg('ログインに失敗しました')


# Process Signup
@app.route('/try_signup', methods=['POST'])
def try_signup():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')

    if not user or not pw:
        return show_msg("ユーザー名とパスワードを入力してください")

    if diary_login.add_user(user, pw):
        # ✅ Automatically log in the new user after signup
        session['login'] = user
        return redirect('/')  # Redirect to their personal diary immediately
    else:
        return show_msg("そのユーザー名はすでに存在します")


# Logout
@app.route('/logout')
def logout():
    diary_login.try_logout()
    return show_msg('ログアウトしました')


# Send a Diary Entry
@app.route('/send', methods=['POST'])
def send_message():
    if not diary_login.is_login():
        return redirect('/login')

    user = diary_login.get_user()
    message = request.form.get('message', '')

    # Handle image upload
    file = request.files.get('image')
    filename = None
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = ""  # Assign an empty string if no valid file is provided

    if message or filename:
        diary_messages.save_message(user, message, filename)

    return redirect('/')


# Delete a Diary Entry
@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if not diary_login.is_login():
        return redirect('/login')

    user = diary_login.get_user()
    diary_messages.delete_message(user, entry_id)

    return redirect('/')


# Edit a Diary Entry
@app.route('/edit/<int:entry_id>')
def edit_entry(entry_id):
    if not diary_login.is_login():
        return redirect('/login')

    user = diary_login.get_user()
    entry = diary_messages.get_entry(user, entry_id)
    if not entry:
        return "Entry not found", 404

    return render_template('edit.html', entry_id=entry_id, entry=entry)


# Update a Diary Entry
@app.route('/update/<int:entry_id>', methods=['POST'])
def update_entry(entry_id):
    if not diary_login.is_login():
        return redirect('/login')

    user = diary_login.get_user()
    updated_text = request.form.get('message', '')
    new_image = request.files.get('image')

    # Handle new image upload if provided
    new_image_filename = None
    if new_image and new_image.filename:  # Check if the file is valid
        filename = secure_filename(
            new_image.filename)  # Ensure filename is safe
        new_image_filename = filename
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    diary_messages.update_entry(user, entry_id, updated_text,
                                new_image_filename)
    return redirect('/')


# Show a Message Page
def show_msg(msg):
    return render_template('msg.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
