# =========================================================
# SISTEM PENDUKUNG KEPUTUSAN METODE WEIGHTED PRODUCT (WP)
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# TAMBAHAN AGAR STREAMLIT STABIL
plt.switch_backend('Agg')

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="SPK Metode WP",
    page_icon="📊",
    layout="wide"
)

# CUSTOM CSS 
st.markdown("""
<style>
/* Background Aplikasi & Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #f8fafc; /* Abu-abu ultra terang */
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #f1f5f9; /* Abu-abu soft */
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] * {
    color: #1e293b;
}

/* Sidebar Project Info Card */
.sidebar-info {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    margin-top: 15px;
}

/* Header & Card Styling */
.card-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); /* Gradasi Biru */
    padding: 30px;
    border-radius: 16px;
    color: white;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
    margin-bottom: 25px;
}

.card-header h1 {
    color: white !important;
    font-size: 32px !important;
    font-weight: 700;
    margin: 0;
}

.card-header p {
    color: #bfdbfe !important;
    font-size: 16px;
    margin-top: 8px;
    margin-bottom: 0;
}

.card {
    background-color: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
}

/* Metric Card */
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.02);
    border-bottom: 4px solid #2563eb; /* Aksen bawah biru */
}

.metric-card h1 {
    color: #1e3a8a !important;
    font-size: 36px !important;
    font-weight: 700;
    margin: 0;
}

.metric-card p {
    color: #64748b !important;
    font-size: 14px;
    font-weight: 500;
    margin-top: 4px;
    margin-bottom: 0;
}

/* Button Customization */
.stButton > button {
    width: 100%;
    background: #2563eb;
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}

.stButton > button:hover {
    background: #1d4ed8;
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    transform: translateY(-1px);
}

/* Typography Overrides */
h1, h2, h3, h4 {
    color: #1e3a8a !important;
    font-weight: 600 !important;
}

/* Member Card (Profil Page) */
.member-card {
    background: #fdfdfd;
    border-left: 5px solid #2563eb;
    padding: 15px 20px;
    margin: 10px 0;
    border-radius: 4px 12px 12px 4px;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# HEADER UTAMA
st.markdown("""
<div class="card-header">
    <h1>📊 SPK Metode Weighted Product</h1>
    <p>Sistem Pendukung Keputusan untuk perangkingan produk fashion secara objektif dan terukur.</p>
</div>
""", unsafe_allow_html=True)

# LOAD DATASET
@st.cache_data
def load_data():
    df = pd.read_csv("styles.csv", on_bad_lines='skip')
    return df

try:
    df_raw = load_data()
except:
    st.error("❌ File styles.csv tidak ditemukan.")
    st.stop()

required_cols = ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage', 'productDisplayName']
available_cols = [col for col in required_cols if col in df_raw.columns]

if len(available_cols) < 9:
    st.error("❌ Kolom dataset tidak lengkap.")
    st.stop()

# PREPROCESSING DATA
spk_df = df_raw[available_cols].dropna().copy()
kriteria = ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage']

# SIDEBAR NAVIGATION 
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h2 style='margin-bottom: 0px; color: #1e3a8a;'>🎯 SPK-WP Panel</h2>
    <span style='color: #64748b; font-size: 13px;'>Decision Support System</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📌 Navigasi Utama")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Dashboard", "Dataset", "Perhitungan WP", "Visualisasi", "Profil Kelompok"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Informasi Project")
st.sidebar.markdown("""
<div class="sidebar-info">
    <small style="color: #64748b; display:block;"><b>Metode :</b></small>
    <span style="font-size: 14px; color: #1e3a8a; font-weight:600;">Weighted Product (WP)</span>
    <div style="margin-top: 8px;"></div>
    <small style="color: #64748b; display:block;"><b>Studi Kasus:</b></small>
    <span style="font-size: 14px; color: #334155;">Fashion Product Dataset</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='text-align: center; margin-top: 50px; color: #94a3b8; font-size: 11px;'>
    © 2026 Project Sistem Cerdas dan Pendukung Keputusan<br>Kelompok 6<br>All Rights Reserved.
</div>
""", unsafe_allow_html=True)

# ==================================
# DASHBOARD
# ==================================
if menu == "Dashboard":
    st.markdown("## 📈 Ringkasan Eksekutif")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h1>{spk_df.shape[0]:,}</h1><p>Total Baris Data</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h1>{spk_df.shape[1]}</h1><p>Total Kolom Atribut</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h1>{len(kriteria)}</h1><p>Total Kriteria WP</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Distribusi Gender Produk")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        
        sns.countplot(data=spk_df, x='gender', hue='gender', palette='Blues_r', legend=False, ax=ax)
        ax.set_xlabel("Kategori Gender", color="#475569", fontsize=10)
        ax.set_ylabel("Jumlah Item", color="#475569", fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cbd5e1')
        ax.spines['bottom'].set_color('#cbd5e1')
        
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================================
# DATASET
# ==================================
elif menu == "Dataset":
    st.markdown("## 📂 Eksplorasi Dataset")
    st.markdown(f"""
    <div class="card" style="background-color: #f1f5f9; border: none;">
        💡 <b>Informasi Log:</b> Menampilkan data bersih setelah proses drop nilai kosong (Missing Values). <br>
        Dimensi Data saat ini: <b>{spk_df.shape[0]} baris</b> × <b>{spk_df.shape[1]} kolom</b>.
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(spk_df, use_container_width=True, height=500)

# ==================================
# PERHITUNGAN WP
# ================================== 
elif menu == "Perhitungan WP":
    st.markdown("## ⚙️ Inti Komputasi Weighted Product")
    
    with st.expander("ℹ️ Lihat Detail Rumus & Prosedur Matematika WP", expanded=False):
        st.markdown("#### 1. Perbaikan / Normalisasi Bobot Kriteria")
        st.latex(r'\text{Bobot Ternormalisasi } (w_j) = \frac{\text{Bobot kriteria}}{\text{Total seluruh bobot kriteria}}')
        
        st.markdown("#### 2. Perhitungan Nilai Vektor S (Preferensi Alternatif)")
        st.latex(r'S_i = \prod_{j=1}^{n} (r_{i,j})^{w_j}')
        st.markdown("""
        *Keterangan:*
        - $S$ = Preferensi alternatif
        - $r$ = Nilai kriteria/rating kecocokan
        - $w$ = Nilai bobot ternormalisasi
        - $i$ = Indeks alternatif
        - $j$ = Indeks kriteria
        - $n$ = Jumlah kriteria
        """)
        
        st.markdown("#### 3. Perhitungan Vektor V (Preferensi Alternatif Ternormalisasi)")
        st.latex(r'V_i = \frac{S_i}{\sum_{i=1}^{m} S_i}')
        st.markdown("""
        *Keterangan:*
        - $V$ = Preferensi alternatif ternormalisasi
        - $S$ = Preferensi alternatif
        - $i$ = Indeks alternatif
        - $m$ = Jumlah alternatif
        """)

    # Kontrol Input Bobot
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎛️ Atur Tingkat Kepentingan Kriteria (Skala 1 - 5)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        w_gender = st.slider("Gender", 1, 5, 3)
        w_master = st.slider("Master Category", 1, 5, 3)
    with col2:
        w_sub = st.slider("Sub Category", 1, 5, 3)
        w_article = st.slider("Article Type", 1, 5, 3)
    with col3:
        w_colour = st.slider("Base Colour", 1, 5, 3)
        w_season = st.slider("Season", 1, 5, 3)
    with col4:
        w_year = st.slider("Year", 1, 5, 3)
        w_usage = st.slider("Usage", 1, 5, 3)
    st.markdown('</div>', unsafe_allow_html=True)

    bobot = np.array([w_gender, w_master, w_sub, w_article, w_colour, w_season, w_year, w_usage], dtype=float)
    bobot_norm = bobot / bobot.sum()

    # Tipe Atribut
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🏷️ Tentukan Tipe Atribut Kriteria")
    cols = st.columns(4)
    atribut = []
    for i, k in enumerate(kriteria):
        with cols[i % 4]:
            pilihan = st.selectbox(f"Sifat {k}", ["Benefit", "Cost"], key=f"attr_{k}")
            atribut.append(1 if pilihan == "Benefit" else 0)
    atribut = np.array(atribut)
    st.markdown('</div>', unsafe_allow_html=True)

    # Konfigurasi Output
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📌 Parameter Output")
    jumlah_tampil = st.text_input("Jumlah data teratas yang ingin ditampilkan dalam tabel hasil ranking:", value="10")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 Jalankan Perhitungan"):
        try:
            jumlah_tampil = int(jumlah_tampil)
            if jumlah_tampil < 1:
                st.error("Jumlah ranking minimal harus 1")
            else:
                with st.spinner("Melakukan kalkulasi matriks keputusan..."):
                    proses_df = spk_df.copy()
                    
                    # ENCODING DATA KATEGORIKAL MENJADI RATING NUMERIK (r_ij)
                    for col in kriteria:
                        proses_df[col] = proses_df[col].astype('category').cat.codes + 1
                    
                    # R_ij matriks
                    R = proses_df[kriteria].values.astype(float)
                    R_norm = np.zeros_like(R)
                    
                    # NORMALISASI NILAI RATING BERDASARKAN COST/BENEFIT
                    for j in range(R.shape[1]):
                        if atribut[j] == 1:
                            R_norm[:, j] = R[:, j] / R[:, j].max()
                        else:
                            R_norm[:, j] = R[:, j].min() / R[:, j]
                    
                    R_norm = np.where(R_norm == 0, 1e-9, R_norm)
                    
                    # IMPLEMENTASI RUMUS GAMBAR 2: S_i = PRODUCT (r_ij ^ w_j)
                    S = np.prod(np.power(R_norm, bobot_norm), axis=1)
                    
                    # IMPLEMENTASI RUMUS GAMBAR 3: V_i = S_i / SUM(S_i)
                    V = S / np.sum(S)
                    
                    proses_df['Nilai Preferensi'] = V
                    hasil = proses_df[['productDisplayName', 'Nilai Preferensi']].sort_values(by='Nilai Preferensi', ascending=False)
                    hasil.reset_index(drop=True, inplace=True)
                    hasil.index += 1
                    hasil.rename_axis("Ranking", inplace=True)
                    
                    st.success("🎉 Komputasi Sukses Selesai Berdasarkan Standar Rumus WP!")
                    
                    # Tabel Hasil
                    st.markdown("### 🏆 Hasil Perangkingan Produk")
                    st.dataframe(hasil.head(jumlah_tampil), use_container_width=True, height=400)
                    
                    # Grafik Hasil Top 10
                    if jumlah_tampil >= 10:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown("### 📊 Visualisasi Perbandingan Nilai Preferensi Top 10")
                        top10 = hasil.head(10)
                        fig, ax = plt.subplots(figsize=(10, 5))
                        sns.barplot(data=top10, y='productDisplayName', x='Nilai Preferensi', hue='productDisplayName', palette='Blues_r', legend=False, ax=ax)
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        st.pyplot(fig, clear_figure=True)
                        plt.close(fig)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download Button
                    csv = hasil.to_csv().encode('utf-8')
                    st.download_button(label="📥 Ekspor Semua Hasil (.CSV)", data=csv, file_name="hasil_perangkingan_wp.csv", mime="text/csv")
        except ValueError:
            st.error("Sistem gagal memproses. Pastikan input jumlah ranking berupa angka numerik valid.")

# ==================================
# VISUALISASI
# ==================================
elif menu == "Visualisasi":
    st.markdown("<h2>📊 Analitik & Visualisasi Lanjutan</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Tren Rilis Produk (Tahun)", "🌡️ Matriks Korelasi Fitur", "🍕 Segmentasi Kategori Utama"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        spk_df['year'] = spk_df['year'].astype(int)
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        sns.countplot(data=spk_df, x='year', hue='year', palette='Blues', legend=False, ax=ax1)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        st.pyplot(fig1, clear_figure=True)
        plt.close(fig1)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        encode_df = spk_df[kriteria].apply(
            lambda x:
            x.astype('category').cat.codes
        )
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        sns.heatmap(
            encode_df.corr(),
            cmap='Blues',
            annot=True,
            ax=ax2
        )
        ax2.set_title("Heatmap Korelasi")
        plt.xticks(rotation=0, fontsize=7)  
        plt.yticks(rotation=0, fontsize=7)
        st.pyplot(fig2, clear_figure=True)
        plt.close(fig2)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Proporsi Distribusi Kategori Produk")
        
        kategori = spk_df['masterCategory'].value_counts()
        top4 = kategori.head(4)
        others = pd.Series({'Others': kategori.iloc[4:].sum()})
        kategori_final = pd.concat([top4, others])
        
        fig3, ax3 = plt.subplots(figsize=(7, 7))
        colors = ['#1e3a8a', '#2563eb', '#3b82f6', '#60a5fa', '#cbd5e1']
        
        wedges, texts, autotexts = ax3.pie(
            kategori_final.values, 
            labels=kategori_final.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors,
            pctdistance=0.75,    
            labeldistance=1.1,   
            textprops={'fontsize': 11}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
            
        ax3.axis('equal')  
        st.pyplot(fig3, clear_figure=True)
        plt.close(fig3)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================================
# PROFIL KELOMPOK
# ==================================
elif menu == "Profil Kelompok":
    st.markdown("## 👨‍💻 Profil Tim & Proyek")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        <div class="card" style="height: 100%;">
            <h3>👥 Anggota Pengembang</h3>
            <div class="member-card">
                <b>Akbar Faqih</b><br>
                <span style="color: #64748b; font-size: 13px;">NIM. 123240207</span>
            </div>
            <div class="member-card">
                <b>Arilda Sarifah Umahatika</b><br>
                <span style="color: #64748b; font-size: 13px;">NIM. 123240030</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="card" style="height: 100%;">
            <h3>ℹ️ Spesifikasi Sistem</h3>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
                <tr style="border-bottom: 1px solid #edf2f7;"><td style="padding: 8px 0; font-weight:600;"> Metode SPK</td><td style="color:#2563eb;">Weighted Product (WP)</td></tr>
                <tr style="border-bottom: 1px solid #edf2f7;"><td style="padding: 8px 0; font-weight:600;"> Studi Kasus</td><td>Fashion Product Recommender</td></tr>
                <tr style="border-bottom: 1px solid #edf2f7;"><td style="padding: 8px 0; font-weight:600;"> Framework</td><td>Python & Streamlit (UI)</td></tr>
                <tr><td style="padding: 8px 0; font-weight:600;"> Dataset</td><td><a href="https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset" target="_blank" style="color:#2563eb; text-decoration:none;">Kaggle Fashion Dataset Link</a></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style="text-align: center; background-color: #f1f5f9; border:none;">
        <h4 style="margin:0 0 8px 0;">🎯 Tujuan Pembuatan Aplikasi</h4>
        <p style="margin:0; max-width: 700px; display: inline-block; color: #475569;">
            Sistem ini dirancang sebagai instrumen bantu pengambilan keputusan objektif dalam memilih produk fashion terbaik yang disesuaikan secara dinamis berdasarkan preferensi bobot subjektif dari pengguna.
        </p>
    </div>
    """, unsafe_allow_html=True)