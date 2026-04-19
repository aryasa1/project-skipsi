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
    recent_teachers = DataPengajar.query.order_by(DataPengajar.id.desc()).limit(5).all()

    stats = [
        {"title": "Total Pengajar", "value": 5, "icon": "fa-users", "accent": "primary"},
        {"title": "Hasil Klasifikasi", "value": 4, "icon": "fa-bar-chart", "accent": "secondary"},
        {"title": "Data Processed", "value": 2, "icon": "fa-file-text-o", "accent": "success"},
        {"title": "Avg. Score", "value": "86.9", "icon": "fa-line-chart", "accent": "warning"},
    ]

    return render_template(
        'index.html',
        nama_user=username_login,
        active_page='dashboard',
        page_title='Dashboard',
        page_subtitle='Ringkasan sistem klasifikasi dan akses cepat ke tiap modul.',
        stats=stats,
        recent_teachers=recent_teachers
    )

@app.route('/data_pengajar')
def data_pengajar():
    if 'user' not in session:
        return redirect(url_for('login'))

    search_query = request.args.get('q', '', type=str).strip()

    # Ambil nomor halaman dari URL (default halaman 1)
    page = request.args.get('page', 1, type=int)

    query = DataPengajar.query.order_by(DataPengajar.nama_pengajar.asc())
    if search_query:
        query = query.filter(DataPengajar.nama_pengajar.ilike(f'%{search_query}%'))

    # Ambil data: 10 data per halaman
    # error_out=False supaya kalau halamannya tidak ada, tidak muncul error 404
    pengajar_paginated = query.paginate(page=page, per_page=10, error_out=False)

    return render_template(
        'data_pengajar.html',
        data=pengajar_paginated,
        search_query=search_query,
        active_page='data_pengajar',
        page_title='Data Pengajar',
        page_subtitle='Kelola data pengajar dan cari entri yang sudah tersimpan.'
    )

@app.route('/rekapan')
def rekapan():
    if 'user' not in session:
        return redirect(url_for('login'))

    summary_cards = [
        {"title": "Excellent", "value": 12, "accent": "success"},
        {"title": "Very Good", "value": 18, "accent": "primary"},
        {"title": "Good", "value": 7, "accent": "warning"},
        {"title": "Average Score", "value": "86.9", "accent": "secondary"},
    ]

    classification_rows = [
        {"no": 1, "pengajar": "Dr. Ahmad Maulana", "kategori": "Excellent", "skor": "95.5"},
        {"no": 2, "pengajar": "Prof. Siti Nurhaliza", "kategori": "Very Good", "skor": "88.2"},
        {"no": 3, "pengajar": "Ir. Budi Santoso", "kategori": "Good", "skor": "78.9"},
        {"no": 4, "pengajar": "Dra. Indah Permata", "kategori": "Very Good", "skor": "85.3"},
    ]

    return render_template(
        'rekapan.html',
        summary_cards=summary_cards,
        classification_rows=classification_rows,
        active_page='rekapan',
        page_title='Rekapan Klasifikasi',
        page_subtitle='Ringkasan hasil klasifikasi dan performa tiap pengajar.'
    )

@app.route('/preprocessing')
def preprocessing():
    if 'user' not in session:
        return redirect(url_for('login'))

    pipeline_steps = [
        {"title": "Upload Dataset", "description": "Unggah file mentah sebelum diproses lebih lanjut."},
        {"title": "Cleansing Data", "description": "Rapikan format, hapus duplikasi, dan validasi kolom inti."},
        {"title": "Run Classification", "description": "Lanjutkan ke proses klasifikasi setelah data siap."},
    ]

    recent_jobs = [
        {"file": "dataset_semester1.csv", "status": "Processed", "tanggal": "2026-04-15"},
        {"file": "dataset_semester2.csv", "status": "Pending", "tanggal": "2026-04-16"},
        {"file": "dataset_semester3.csv", "status": "Processed", "tanggal": "2026-04-14"},
    ]

    return render_template(
        'preprocessing.html',
        pipeline_steps=pipeline_steps,
        recent_jobs=recent_jobs,
        active_page='preprocessing',
        page_title='Pre-Processing',
        page_subtitle='Pantau alur persiapan data sebelum klasifikasi dijalankan.'
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
