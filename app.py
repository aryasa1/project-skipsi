from flask import Flask, render_template, request, redirect, session, url_for # Tambahkan url_for di sini
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/klasifikasi'
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class DataPengajar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_pengajar = db.Column(db.String(250), unique=True, nullable=False)


@app.route('/')
def home():
    return redirect('/login')

from flask import flash # Tambahkan flash untuk pesan error

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 1. Cari user di tabel 'users' berdasarkan username
        user_data = users.query.filter_by(username=username).first()

        # 2. Cek apakah user ketemu DAN password-nya cocok
        if user_data and user_data.password == password:
            # Jika benar, buat session dan ke dashboard
            session['user'] = user_data.username
            return redirect(url_for('dashboard'))
        else:
            # Kirim notifikasi error
            flash('Username atau Password salah!', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Pastikan 'users' sesuai dengan nama class di model kamu
        new_user = users(
            username=username, 
            email=email, 
            password=password
        )
            
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    username_login = session['user']
    return render_template('index.html', nama_user=username_login)

@app.route('/data_pengajar')
def data_pengajar():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Ambil nomor halaman dari URL (default halaman 1)
    page = request.args.get('page', 1, type=int)
    
    # Ambil data: 10 data per halaman
    # error_out=False supaya kalau halamannya tidak ada, tidak muncul error 404
    pengajar_paginated = DataPengajar.query.paginate(page=page, per_page=10, error_out=False)
        
    return render_template('data_pengajar.html', data=pengajar_paginated)

@app.route('/rekapan')
def rekapan():

    return render_template('rekapan.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
