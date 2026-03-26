# 🛒 E-Commerce Public Data Analysis Dashboard

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Seaborn](https://img.shields.io/badge/Seaborn-blue?style=for-the-badge&logo=seaborn)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

## 📌 Project Overview
Proyek ini merupakan tugas akhir dari kelas **Belajar Analisis Data dengan Python** di Dicoding. Proyek ini berfokus pada analisis *E-Commerce Public Dataset* untuk menggali *insight* bisnis yang bermanfaat. 

Melalui proses *data wrangling*, *exploratory data analysis* (EDA), dan visualisasi data, dashboard ini dirancang untuk menjawab tiga pertanyaan bisnis utama:
1. Kategori produk apa yang menghasilkan pendapatan tertinggi dan terendah?
2. Bagaimana demografi persebaran pelanggan berdasarkan negara bagian (*state*)?
3. Bagaimana tren jumlah pesanan per bulan selama tahun 2018?

## 📂 Directory Structure
```text
.
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   └── products_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## 🚀 Setup & Deployment
### 1. Clone Repository
Langkah pertama adalah mengunduh salinan repositori ini ke komputer Anda. Buka terminal atau command prompt, lalu jalankan perintah berikut:
```text
git clone [https://github.com/Bhenarezky/proyek-analisis-data.git](https://github.com/Bhenarezky/proyek-analisis-data.git)
cd proyek-analisis-data
```

### 2. Setup Environment
Menggunakan Shell/Terminal (Pipenv)
```text
pipenv install
pipenv shell
pip install -r requirements.txt
```

### 3. Run Streamlit App (Lokal)
Setelah proses instalasi selesai, Anda dapat menjalankan dan menguji dashboard secara lokal dengan perintah berikut:
```text
streamlit run dashboard/dashboard.py
```
Dashboard akan otomatis terbuka di browser default Anda.

### 4. Deploy to Streamlit Cloud
Proyek ini sudah dikonfigurasi agar siap di-deploy ke Streamlit Cloud. Ikuti langkah-langkah ini untuk meng-online-kan dashboard Anda:
  - Pastikan seluruh perubahan kode (termasuk requirements.txt dan dashboard.py) sudah di-push ke repositori GitHub Anda.
  - Buka situs [Streamlit Share](https://share.streamlit.io/) dan login menggunakan akun GitHub Anda.
  - Klik tombol "New app".
  - Isi formulir konfigurasi
  - Klik "Deploy!" dan tunggu beberapa saat hingga proses instalasi dependensi di server selesai.
  - Selesai! Dashboard Anda kini sudah online dan tautannya bisa langsung dibagikan.
