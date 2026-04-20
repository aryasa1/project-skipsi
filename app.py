import os
import csv
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/klasifikasi'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)

ALLOWED_UPLOAD_EXTENSIONS = {'csv', 'xlsx', 'xls'}


def ensure_upload_folder():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def is_allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS
    )


def get_recent_uploads(limit=10):
    ensure_upload_folder()
    uploaded_files = []

    for entry in os.scandir(app.config['UPLOAD_FOLDER']):
        if not entry.is_file():
            continue

        stats = entry.stat()
        uploaded_files.append(
            {
                'file': entry.name,
                'status': 'Uploaded',
                'tanggal': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M'),
            }
        )

    uploaded_files.sort(key=lambda item: item['tanggal'], reverse=True)
    return uploaded_files[:limit]


def get_latest_uploaded_file():
    ensure_upload_folder()
    files = [entry for entry in os.scandir(app.config['UPLOAD_FOLDER']) if entry.is_file()]
    if not files:
        return None
    return max(files, key=lambda entry: entry.stat().st_mtime)


def normalize_headers(header_row, width):
    headers = []
    for index in range(width):
        raw_value = header_row[index] if index < len(header_row) else ''
        label = str(raw_value).strip() if raw_value is not None else ''
        headers.append(label or f'Kolom {index + 1}')
    return headers


def parse_csv_dataset(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csv_file:
        rows = list(csv.reader(csv_file))
    return rows


def parse_xlsx_dataset(file_path):
    from openpyxl import load_workbook

    workbook = load_workbook(file_path, read_only=True, data_only=True)
    try:
        worksheet = workbook.active
        return [list(row) for row in worksheet.iter_rows(values_only=True)]
    finally:
        workbook.close()


def parse_xls_dataset(file_path):
    import xlrd

    workbook = xlrd.open_workbook(file_path)
    worksheet = workbook.sheet_by_index(0)
    return [worksheet.row_values(index) for index in range(worksheet.nrows)]


def get_uploaded_dataset_preview(limit=100):
    latest_file = get_latest_uploaded_file()
    if latest_file is None:
        return {'headers': [], 'rows': [], 'total_rows': 0}

    extension = latest_file.name.rsplit('.', 1)[1].lower()
    raw_rows = []

    if extension == 'csv':
        raw_rows = parse_csv_dataset(latest_file.path)
    elif extension == 'xlsx':
        raw_rows = parse_xlsx_dataset(latest_file.path)
    elif extension == 'xls':
        raw_rows = parse_xls_dataset(latest_file.path)

    cleaned_rows = []
    for row in raw_rows:
        normalized_row = ['' if cell is None else str(cell) for cell in row]
        if any(str(cell).strip() for cell in normalized_row):
            cleaned_rows.append(normalized_row)

    if not cleaned_rows:
        return {'headers': [], 'rows': [], 'total_rows': 0}

    headers = normalize_headers(cleaned_rows[0], max(len(row) for row in cleaned_rows))
    data_rows = []
    for row in cleaned_rows[1:limit + 1]:
        padded_row = row + [''] * (len(headers) - len(row))
        data_rows.append(padded_row[:len(headers)])

    return {
        'headers': headers,
        'rows': data_rows,
        'total_rows': max(len(cleaned_rows) - 1, 0),
    }


def is_ajax_request():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def render_page(template_name, partial_name, **context):
    if is_ajax_request():
        return render_template(partial_name, **context)
    return render_template(template_name, **context)

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

    return render_page(
        'index.html',
        '_dashboard_content.html',
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

    return render_page(
        'data_pengajar.html',
        '_data_pengajar_content.html',
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

    return render_page(
        'rekapan.html',
        '_rekapan_content.html',
        summary_cards=summary_cards,
        classification_rows=classification_rows,
        active_page='rekapan',
        page_title='Rekapan Klasifikasi',
        page_subtitle='Ringkasan hasil klasifikasi dan performa tiap pengajar.'
    )

@app.route('/preprocessing', methods=['GET', 'POST'])
def preprocessing():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        uploaded_file = request.files.get('dataset_file')

        if uploaded_file is None or uploaded_file.filename == '':
            flash('Pilih file terlebih dahulu sebelum upload.', 'danger')
            return redirect(url_for('preprocessing'))

        if not is_allowed_file(uploaded_file.filename):
            flash('Format file tidak didukung. Gunakan CSV, XLSX, atau XLS.', 'danger')
            return redirect(url_for('preprocessing'))

        ensure_upload_folder()
        original_name = secure_filename(uploaded_file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        saved_name = f'{timestamp}_{original_name}'
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_name)

        uploaded_file.save(save_path)
        flash(f'File {original_name} berhasil diupload.', 'success')
        return redirect(url_for('preprocessing'))

    pipeline_steps = [
        {"title": "Upload Dataset", "description": "Unggah file mentah sebelum diproses lebih lanjut."},
        {"title": "Cleansing Data", "description": "Rapikan format, hapus duplikasi, dan validasi kolom inti."},
        {"title": "Run Classification", "description": "Lanjutkan ke proses klasifikasi setelah data siap."},
    ]
    dataset_preview = get_uploaded_dataset_preview()

    return render_page(
        'preprocessing.html',
        '_preprocessing_content.html',
        pipeline_steps=pipeline_steps,
        dataset_preview=dataset_preview,
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
