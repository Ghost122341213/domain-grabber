# Domain Grabber

Script Python untuk mengambil daftar **root domain** berdasarkan ekstensi tertentu (.id, .co.id, .ac.id, dll.) dari **Archive.org CDX API**

## ✨ Fitur
- Ambil daftar domain dari [web.archive.org CDX API](https://archive.org/help/wayback_api.php).
- Mendukung multi-ekstensi sekaligus (dipisahkan koma).
- Target jumlah domain per ekstensi bisa diatur.
- User-Agent berganti otomatis untuk menghindari rate limit.
- Tampilan CLI interaktif dan berwarna menggunakan **Rich**.
- Penyimpanan hasil otomatis ke file .txt dengan timestamp.

## 📦 Instalasi
Pastikan Python **3.8+** sudah terpasang.

1. Clone repositori ini:
   
bash
   git clone https://github.com/bimantaraz/domain-grabber.git
   cd domain-grabber

2. Install dependensi:
bash
   pip install -r requirements.txt
   
## 🚀 Cara Menggunakan

Jalankan:
bash
python grabber.py
Contoh input:

Ekstensi: id, co.id, ac.id
Jumlah root domain per ekstensi: 50
Mode hati-hati (delay tambahan kecil)? [Y/n]: y
Output akan tersimpan di file:

grab_id_20250812_153045.txt
grab_co.id_20250812_153045.txt
grab_ac.id_20250812_153045.txt
## 📄 Contoh Output File

abc.ac.id
def.ac.id
example.co.id
universitas.ac.id
### **📄 requirements.txt**


requests>=2.31.0
rich>=13.7.1
urllib3>=2.2.2

## ⚠ Catatan

* Gunakan ekstensi spesifik (`co.id`, `ac.id`, `go.id`) untuk mengurangi risiko rate-limit.
* Jika terkena **403** atau **429**, coba jalankan kembali setelah beberapa menit atau gunakan target jumlah lebih kecil.
* Archive.org CDX API tidak selalu mengembalikan hasil lengkap, jadi hasil dapat berbeda tiap eksekusi.
