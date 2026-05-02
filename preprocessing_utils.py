import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Dictionary slang
slangwords = {
     "bngt": "banget", "bgt": "banget", "bgtt": "banget", "bgttt": "banget", "bangett": "banget",
    "bagusss": "bagus", "bagussss": "bagus", "baguus": "bagus", "bgus": "bagus", "bestttttttt": "bagus",
    "ama": "sama", "sm": "sama", "sma": "sama", "ky": "kayak", "kayak": "seperti", "kek": "seperti",
    "ga": "tidak", "gak": "tidak", "gk": "tidak", "ngga": "tidak", "nggak": "tidak", "nggaa": "tidak",
    "engga": "tidak", "enggak": "tidak", "ndak": "tidak", "tak": "tidak",
    "tp": "tapi", "tpi": "tapi", "tapii": "tapi",
    "sdh": "sudah", "udah": "sudah", "ud": "sudah", "udh": "sudah",
    "klo": "kalau", "kalo": "kalau", "kl": "kalau", "klw": "kalau", "kaloo": "kalau",
    "jg": "juga", "jga": "juga", "dr": "dari", "dri": "dari",
    "utk": "untuk", "untk": "untuk", "bwt": "buat", "bt": "buat",
    "dlm": "dalam", "krn": "karena", "karna": "karena", "krna": "karena",
    "sy": "saya", "sya": "saya", "gw": "saya", "gua": "saya", "gue": "saya",
    "ak": "saya", "aq": "saya", "akuwh": "aku", "akuu": "aku",
    "kt": "kita", "kitaa": "kita",
    "pake": "pakai", "pakek": "pakai", "pkai": "pakai",
    "makasih": "terima kasih", "mksh": "terima kasih", "maksi": "terima kasih",
    "tks": "terima kasih", "thx": "terima kasih", "thankyou": "terima kasih", "ty": "terima kasih",
    "mndarin": "mandarin", "mandarinn": "mandarin", "mandrin": "mandarin",
    "interaktif": "komunikatif", "komunikatiff": "komunikatif",
    "oke": "ok", "okee": "ok", "okey": "ok", "okee": "ok", "okkk": "ok",
    "laoshi": "pengajar", "laoshinya": "pengajarnya", "laoshi2": "pengajar",
    "shifu": "pengajar", "teacher": "pengajar", "teachernya": "pengajarnya",
    "ngajar": "mengajar", "ngajarin": "mengajar", "ngajarnya": "mengajarnya",
    "ajarin": "mengajar", "bljr": "belajar", "beljr": "belajar",
    "muridnya": "siswa", "student": "siswa", "studennya": "siswa", "anaknya": "siswa",
    "fokusin": "fokus", "fokusnyaa": "fokus", "fokuss": "fokus",
    "konsen": "fokus", "konsennya": "fokus",
    "responnya": "respons", "respon": "respons", "ngerespon": "merespons",
    "jawabnya": "menjawab", "jawb": "jawab",
    "lumayan": "cukup", "lumayann": "cukup", "cukupp": "cukup",
    "cukp": "cukup", "cukub": "cukup",
    "lancarrr": "lancar", "lancarr": "lancar", "lancar2": "lancar",
    "pelan2": "pelan", "pelann": "pelan",
    "masi": "masih", "msh": "masih", "msih": "masih",
    "blm": "belum", "belom": "belum", "lom": "belum",
    "susah": "sulit", "susa": "sulit", "sulittt": "sulit",
    "bingungg": "bingung", "bingungg": "bingung",
    "kureng": "kurang", "krg": "kurang", "kurangg": "kurang",
    "kurleb": "kurang lebih",
    "lebihh": "lebih", "lebh": "lebih",
    "cepet": "cepat", "cpet": "cepat", "cepettt": "cepat",
    "telat": "terlambat", "telatt": "terlambat",
    "dateng": "datang", "dtg": "datang",
    "ngerjain": "mengerjakan", "ngerja": "mengerjakan", "kerjain": "mengerjakan",
    "nulis": "menulis", "bacain": "membaca", "ngulang": "mengulang",
    "pahaminnya": "memahami", "paham": "memahami", "pahamnya": "memahami",
    "ngerti": "mengerti", "ngertii": "mengerti", "ngertiin": "mengerti",
    "aktiftt": "aktif", "aktiff": "aktif",
    "pasifff": "pasif", "pasifnya": "pasif",
    "pd": "percaya diri", "pede": "percaya diri", "maluu": "malu",
    "malu2": "malu", "grogi": "gugup",
    "semangatt": "semangat", "semngat": "semangat", "antusiass": "antusias",
    "rapii": "rapi", "rapih": "rapi",
    "jelass": "jelas", "jls": "jelas",
    "pronouncenya": "pelafalan", "pronounce": "pelafalan",
    "pelafalannyaa": "pelafalan", "ngomong": "berbicara",
    "vocab": "kosakata", "vocabs": "kosakata", "kosakataa": "kosakata",
    "grammar": "tata bahasa", "grammarnya": "tata bahasa",
    "udhbisa": "sudah bisa", "suda bisa": "sudah bisa",
    "masihragu": "masih ragu", "kurangfokus": "kurang fokus",
    "kurangaktif": "kurang aktif", "kurangpd": "kurang percaya diri",

    # --- POSITIF / PUJIAN ---
    "bagusss": "bagus", "bagussss": "bagus", "bestttttttt": "bagus", "mantap": "bagus",
    "keren": "bagus", "mantul": "bagus", "kece": "bagus", "top": "bagus",
    "oke": "ok", "okee": "ok", "okey": "ok", "okeey": "ok",
    "seru": "menyenangkan", "seruu": "menyenangkan", "asik": "menyenangkan", "asyik": "menyenangkan",

    # --- NEGATIF / KRITIK ---
    "kurang": "buruk", "jelek": "buruk", "lambat": "lambat", "lemot": "lambat",
    "lelet": "lambat", "ngaret": "lambat", "bosan": "membosankan", "bete": "membosankan",
    "gaje": "tidak jelas", "ga jelas": "tidak jelas", "aneh": "tidak jelas",

    # --- KATA KERJA & AKTIVITAS ---
    "laoshi": "guru", "laoshinya": "guru", "baca": "membaca", "nulis": "menulis",
    "ngajar": "mengajar", "pake": "pakai", "pakek": "pakai", "ngomong": "bicara",
    "ngmng": "bicara", "tanya": "bertanya", "nanya": "bertanya", "ngasih": "memberi",

    # --- KATA GANTI & PEMBANTU ---
    "sy": "saya", "gw": "saya", "gua": "saya", "ak": "saya", "aku": "saya", "urang": "saya",
    "km": "kamu", "kamu": "kamu", "lo": "kamu", "loe": "kamu", "ente": "kamu",
    "ga": "tidak", "gak": "tidak", "gk": "tidak", "ngga": "tidak", "nggak": "tidak", "ndak": "tidak", "kagak": "tidak",
    "tp": "tapi", "tpi": "tapi", "tapi": "tapi",
    "klo": "kalau", "kalo": "kalau", "kl": "kalau", "klw": "kalau",
    "jg": "juga", "jga": "juga", "juga": "juga",
    "yg": "yang", "yang": "yang",
    "bngt": "banget", "bgt": "banget", "bgtt": "banget", "bgttt": "banget", "bangett": "banget", "beud": "banget",

    # --- KATA HUBUNG / LAINNYA ---
    "makasih": "terima kasih", "tks": "terima kasih", "thx": "terima kasih", "thankyou": "terima kasih",
    "sama": "sama", "ama": "sama", "sm": "sama",
    "dr": "dari", "dri": "dari", "dari": "dari",
    "utk": "untuk", "untuk": "untuk",
    "dlm": "dalam", "dalam": "dalam",
    "krn": "karena", "karna": "karena", "karena": "karena",
    "sudah": "sudah", "udah": "sudah", "sdh": "sudah", "ud": "sudah",
    "bisa": "bisa", "bs": "bisa", "bisa2": "bisa",
    "gregetan": "gemas", "sabar": "sabar", "suka": "suka", "senang": "suka"
    
}

def cleaningText(text):
    text = str(text).lower()
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # Hapus mention
    text = re.sub(r'https?:\/\/\S+', '', text) # Hapus link
    text = re.sub(r'[^a-zA-Z\s]', '', text)    # Hapus karakter non-huruf
    return re.sub(r'\s+', ' ', text).strip()  # Hapus spasi ganda

def fix_slangwords(text):
    words = text.split()
    return " ".join([slangwords.get(w, w) for w in words])

def stemmingText(text):
    return stemmer.stem(text)

def run_pipeline(text):
    text = cleaningText(text)
    text = fix_slangwords(text)
    return stemmingText(text)