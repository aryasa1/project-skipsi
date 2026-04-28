import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Dictionary slang
slangwords = {
       # --- TEMUAN KHUSUS DATA CETTA MANDARIN ---
    "bngt": "banget", "bgt": "banget", "bgtt": "banget", "bgttt": "banget",
    "bagusss": "bagus", "bagussss": "bagus", "bestttttttt": "bagus",
    "ama": "sama", "sm": "sama", "ky": "kayak", "kayak": "seperti",
    "ga": "tidak", "gak": "tidak", "gk": "tidak", "ngga": "tidak", "nggak": "tidak", "ndak": "tidak",
    "tp": "tapi", "tpi": "tapi", "sdh": "sudah", "udah": "sudah", "ud": "sudah",
    "klo": "kalau", "kalo": "kalau", "kl": "kalau", "klw": "kalau",
    "jg": "juga", "jga": "juga", "dr": "dari", "dri": "dari",
    "utk": "untuk", "bwt": "buat", "dlm": "dalam", "krn": "karena", "karna": "karena",
    "sy": "saya", "gw": "saya", "gua": "saya", "ak": "saya", "akuwh": "aku",
    "kt": "kita", "pake": "pakai", "pakek": "pakai", "makasih": "terima kasih", "tks": "terima kasih",
    "thx": "terima kasih", "thankyou": "terima kasih", "mndarin": "mandarin",
    "interaktif": "komunikatif", "oke": "ok", "okee": "ok", "okey": "ok",
    # --- POSITIF / PUJIAN ---
    "bagusss": "bagus", "bagussss": "bagus", "bestttttttt": "bagus", "mantap": "bagus",
    "keren": "bagus", "mantul": "bagus", "kece": "bagus", "top": "bagus",
    "oke": "ok", "okee": "ok", "okey": "ok", "okeey": "ok",
    "seru": "menyenangkan", "seruu": "menyenangkan", "asik": "menyenangkan", "asyik": "menyenangkan",

    # --- NEGATIF / KRITIK ---
    "kurang": "tidak baik", "jelek": "tidak baik", "lambat": "lambat", "lemot": "lambat",
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
    "gregetan": "gemas", "sabar": "sabar", "suka": "suka", "senang": "suka",

    # --- DAFTAR UMUM (DARI DATA SEBELUMNYA) ---
    "@": "di", "abis": "habis", "wtb": "beli", "masi": "masih", "wts": "jual", "wtt": "tukar",
    "maks": "maksimal", "plisss": "tolong", "indo": "indonesia", "ad": "ada", "rv": "redvelvet",
    "plis": "tolong", "pls": "tolong", "cr": "sumber", "cod": "bayar ditempat", "adlh": "adalah",
    "aj": "saja", "aja": "saja", "ajj": "saja", "akika": "aku", "alay": "norak", "alow": "halo",
    "ambilin": "ambilkan", "ancur": "hancur", "anjrit": "anjing", "anjir": "anjing", "anter": "antar",
    "ap2": "apa-apa", "apasih": "apa sih", "apes": "sial", "aps": "apa", "aq": "saya",
    "asbun": "asal bunyi", "aseekk": "asyik", "asem": "asam", "aspal": "asli tetapi palsu",
    "astul": "asal tulis", "ato": "atau", "awak": "saya", "ay": "sayang", "ayank": "sayang",
    "b4": "sebelum", "bakalan": "akan", "bangedh": "banget", "bcanda": "bercanda", "bdg": "bandung",
    "begajulan": "nakal", "beliin": "belikan", "bentar": "sebentar", "ber3": "bertiga", "beresin": "membereskan",
    "bete": "bosan", "beud": "banget", "bg": "abang", "bgmn": "bagaimana", "bijimane": "bagaimana",
    "bkl": "akan", "bknnya": "bukannya", "blh": "boleh", "bln": "bulan", "blum": "belum",
    "bnci": "benci", "bnran": "yang benar", "bodor": "lucu", "bokap": "ayah", "boker": "buang air besar",
    "bokis": "bohong", "boljug": "boleh juga", "br": "baru", "brg": "bareng", "bro": "saudara laki-laki",
    "bru": "baru", "bs": "bisa", "bsen": "bosan", "bt": "buat", "btw": "ngomong-ngomong",
    "buaya": "tidak setia", "bubbu": "tidur", "bubu": "tidur", "bw": "bawa", "byk": "banyak",
    "byrin": "bayarkan", "cabal": "sabar", "cadas": "keren", "calo": "makelar", "can": "belum",
    "capcus": "pergi", "caper": "cari perhatian", "ce": "cewek", "cekal": "cegah tangkal",
    "cemen": "penakut", "cengengesan": "tertawa", "cepet": "cepat", "cew": "cewek", "chuyunk": "sayang",
    "cimeng": "ganja", "ciyh": "sih", "ckepp": "cakep", "ckp": "cakep", "cmpur": "campur",
    "cong": "banci", "conlok": "cinta lokasi", "cowwyy": "maaf", "cp": "siapa", "cpe": "capek",
    "cppe": "capek", "cucok": "cocok", "cuex": "cuek", "cumi": "Cuma miscall", "cups": "culun",
    "curanmor": "pencurian kendaraan bermotor", "curcol": "curahan hati colongan", "cwek": "cewek",
    "cyin": "cinta", "d": "di", "dah": "deh", "dapet": "dapat", "de": "adik", "dek": "adik",
    "demen": "suka", "deyh": "deh", "dgn": "dengan", "diancurin": "dihancurkan", "dimaafin": "dimaafkan",
    "dimintak": "diminta", "disono": "di sana", "dket": "dekat", "dkk": "dan kawan-kawan",
    "dll": "dan lain-lain", "dlu": "dulu", "dngn": "dengan", "dodol": "bodoh", "doku": "uang",
    "dongs": "dong", "dpt": "dapat", "dri": "dari", "drmn": "darimana", "drtd": "dari tadi",
    "dst": "dan seterusnya", "dtg": "datang", "duh": "aduh", "duren": "durian", "ed": "edisi",
    "egp": "emang gue pikirin", "eke": "aku", "elu": "kamu", "emangnya": "memangnya", "emng": "memang",
    "endak": "tidak", "enggak": "tidak", "envy": "iri", "ex": "mantan", "folbek": "follow back",
    "fyi": "sebagai informasi", "gaada": "tidak ada", "gag": "tidak", "gaje": "tidak jelas",
    "gak papa": "tidak apa-apa", "gpp": "tidak apa-apa", "gan": "juragan", "gaptek": "gagap teknologi",
    "gawe": "kerja", "gbs": "tidak bisa", "gebetan": "orang yang disuka", "geje": "tidak jelas",
    "ghiy": "lagi", "gile": "gila", "gimana": "bagaimana", "githu": "gitu", "gj": "tidak jelas",
    "gmana": "bagaimana", "gn": "begini", "goblok": "bodoh", "gowes": "mengayuh sepeda",
    "gpny": "tidak punya", "gr": "gede rasa", "gretongan": "gratisan", "gtau": "tidak tahu",
    "guoblok": "goblok", "hallow": "halo", "helo": "halo", "hey": "hai", "hlm": "halaman",
    "hny": "hanya", "hoax": "isu bohong", "hr": "hari", "hrus": "harus", "huff": "mengeluh",
    "hum": "rumah", "ilang": "hilang", "ilfil": "tidak suka", "imoetz": "imut", "item": "hitam",
    "itungan": "hitungan", "iye": "iya", "ja": "saja", "jadiin": "jadi", "jaim": "jaga image",
    "jayus": "tidak lucu", "jdi": "jadi", "jem": "jam", "jgnkan": "jangankan", "jir": "anjing",
    "jln": "jalan", "jomblo": "tidak punya pacar", "jutek": "galak", "k": "ke", "kabor": "kabur",
    "kacrut": "kacau", "kagak": "tidak", "kalo": "kalau", "kampret": "sialan", "karna": "karena",
    "katrok": "kampungan", "kayanya": "kayaknya", "kbr": "kabar", "kdu": "harus", "kemaren": "kemarin",
    "kepengen": "mau", "kepingin": "mau", "ketrima": "diterima", "kgiatan": "kegiatan", "kibul": "bohong",
    "klianz": "kalian", "klw": "kalau", "km": "kamu", "kmps": "kampus", "kmrn": "kemarin",
    "knal": "kenal", "knp": "kenapa", "kongkow": "kumpul", "kpn": "kapan", "krenz": "keren",
    "krm": "kirim", "ktmu": "ketemu", "kuper": "kurang pergaulan", "kw": "imitasi", "kyk": "seperti",
    "la": "lah", "lam": "salam", "lebay": "berlebihan", "leh": "boleh", "lelet": "lambat",
    "lemot": "lambat", "lgi": "lagi", "lgsg": "langsung", "liat": "lihat", "lmyn": "lumayan",
    "lo": "kamu", "loe": "kamu", "lola": "lambat berfikir", "louph": "cinta", "lp": "lupa",
    "luchuw": "lucu", "lum": "belum", "luthu": "lucu", "maacih": "terima kasih", "mabal": "bolos",
    "macem": "macam", "macih": "masih", "maem": "makan", "maho": "homo", "maksain": "memaksa",
    "malem": "malam", "mam": "makan", "maneh": "kamu", "maniez": "manis", "mao": "mau",
    "masukin": "masukkan", "melu": "ikut", "mepet": "dekat", "mgu": "minggu", "mlah": "malah",
    "mngkn": "mungkin", "mo": "mau", "mokad": "mati", "moso": "masa", "mpe": "sampai",
    "msk": "masuk", "mslh": "masalah", "mulu": "melulu", "mumpung": "selagi", "musti": "mesti",
    "muupz": "maaf", "nanam": "menanam", "nanya": "bertanya", "napa": "kenapa", "nasgor": "nasi goreng",
    "nda": "tidak", "ndiri": "sendiri", "ne": "ini", "nembak": "menyatakan cinta", "ngaku": "mengaku",
    "ngambil": "mengambil", "ngapah": "kenapa", "ngaret": "terlambat", "ngasih": "memberikan",
    "ngeles": "berkilah", "ngelidur": "menggigau", "ngga": "tidak", "ngibul": "berbohong",
    "ngiler": "mau", "ngiri": "iri", "ngisiin": "mengisikan", "ngmng": "bicara", "ngomong": "bicara",
    "ngurus": "mengurus", "nie": "ini", "nih": "ini", "nmr": "nomor", "nntn": "nonton",
    "nobar": "nonton bareng", "ntar": "nanti", "ntn": "nonton", "numpuk": "bertumpuk",
    "nutupin": "menutupi", "nyari": "mencari", "nyicil": "mencicil", "nyokap": "ibu", "ogah": "tidak mau",
    "ol": "online", "ongkir": "ongkos kirim", "oot": "keluar topik", "ortu": "orang tua",
    "otw": "sedang jalan", "pacal": "pacar", "pake": "pakai", "pala": "kepala", "pede": "percaya diri",
    "perhatiin": "perhatikan", "pesenan": "pesanan", "pi": "tapi", "pisan": "sangat",
    "plg": "paling", "pst": "pasti", "pw": "nyaman", "qmu": "kamu", "re": "balas", "rempong": "sulit",
    "repp": "balas", "rhs": "rahasia", "rmh": "rumah", "ru": "baru", "ruz": "terus", "saia": "saya",
    "salting": "salah tingkah", "sampe": "sampai", "samsek": "sama sekali", "sapose": "siapa",
    "sbb": "sebagai berikut", "sbh": "sebuah", "sbnrny": "sebenarnya", "scr": "secara",
    "sdgkn": "sedangkan", "sdkt": "sedikit", "se7": "setuju", "sempet": "sempat", "sgt": "sangat",
    "shg": "sehingga", "sj": "saja", "skalian": "sekalian", "sklh": "sekolah", "skt": "sakit",
    "slesai": "selesai", "sll": "selalu", "slma": "selama", "slsai": "selesai", "smpt": "sempat",
    "smw": "semua", "sndiri": "sendiri", "songong": "sombong", "sory": "maaf", "sotoy": "sok tahu",
    "spa": "siapa", "spt": "seperti", "stiap": "setiap", "stlh": "setelah", "suk": "masuk",
    "sumpek": "sempit", "syg": "sayang", "t4": "tempat", "tajir": "kaya", "tau": "tahu",
    "taw": "tahu", "td": "tadi", "tdk": "tidak", "telat": "terlambat", "temen": "teman",
    "tengil": "menyebalkan", "tepar": "terkapar", "tggu": "tunggu", "tgu": "tunggu",
    "thankz": "terima kasih", "thn": "tahun", "tks": "terima kasih", "tlp": "telepon",
    "tls": "tulis", "tmbah": "tambah", "tmen2": "teman-teman", "tmpt": "tempat", "tngu": "tunggu",
    "tnyta": "ternyata", "tpi": "tapi", "trima": "terima kasih", "trm": "terima", "trs": "terus",
    "ttg": "tentang", "tuch": "tuh", "tuir": "tua", "tw": "tahu", "u": "kamu", "ud": "sudah",
    "udah": "sudah", "ujg": "ujung", "unyu": "lucu", "uplot": "unggah", "urang": "saya",
    "usah": "perlu", "utk": "untuk", "wat": "buat", "wkt": "waktu", "yaudah": "ya sudah",
    "yg": "yang", "yl": "yang lain", "yo": "iya", "yowes": "ya sudah", "yup": "iya"
    
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