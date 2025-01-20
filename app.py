import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Data dummy untuk masing-masing modul
# Modul Sales
sales_data = pd.DataFrame({
    'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Pendapatan': [random.randint(5000, 10000) for _ in range(5)]
})

# Modul Stock Barang (Menambahkan ID, Nama, Jenis, Warna, Ukuran, Jumlah, Harga)
stock_data = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Nama': ['Produk A', 'Produk B', 'Produk C', 'Produk D'],
    'Jenis': ['Elektronik', 'Pakaian', 'Makanan', 'Peralatan'],
    'Warna': ['Merah', 'Biru', 'Hijau', 'Hitam'],
    'Ukuran': ['M', 'L', 'XL', 'S'],
    'Jumlah': [random.randint(20, 100) for _ in range(4)],
    'Harga': [random.randint(100, 500) for _ in range(4)]
})

# Modul Finansial
financial_data = pd.DataFrame({
    'Kategori': ['Pendapatan', 'Pengeluaran'],
    'Jumlah': [random.randint(5000, 15000), random.randint(1000, 5000)]
})

# Modul HR
hr_data = pd.DataFrame({
    'Posisi': ['Manager', 'Staff', 'Supervisor'],
    'Jumlah Karyawan': [2, 10, 3]
})

# Fungsi untuk membuat grafik
def create_sales_fig():
    return px.bar(sales_data, x='Bulan', y='Pendapatan', title='Sales Pendapatan')

def create_stock_fig():
    return px.pie(stock_data, names='Nama', values='Jumlah', title='Distribusi Stok Barang')

def create_financial_fig():
    return px.pie(financial_data, names='Kategori', values='Jumlah', title='Pemasukan dan Pengeluaran')

def create_hr_fig():
    return px.bar(hr_data, x='Posisi', y='Jumlah Karyawan', title='Jumlah Karyawan Berdasarkan Posisi')

# Layout untuk Dashboard Streamlit
st.title("Dashboard Perusahaan")

# Bagian Sales
st.subheader('Sales Pendapatan')
st.plotly_chart(create_sales_fig())

# Input untuk update Sales
st.text_input('Bulan', key='sales_bulan')
st.number_input('Pendapatan', key='sales_pendapatan', min_value=0)

if st.button('Update Sales'):
    bulan = st.session_state.sales_bulan
    pendapatan = st.session_state.sales_pendapatan
    if bulan and pendapatan:
        sales_data = sales_data.append({'Bulan': bulan, 'Pendapatan': int(pendapatan)}, ignore_index=True)
        st.success('Data Sales berhasil diperbarui!')
    st.plotly_chart(create_sales_fig())

# Bagian Stock Barang
st.subheader('Stock Barang')
st.plotly_chart(create_stock_fig())

# Input untuk update Stock Barang
st.number_input('ID Barang', key='stock_id', min_value=1)
st.text_input('Nama Barang', key='stock_nama')
st.text_input('Jenis Barang', key='stock_jenis')
st.text_input('Warna Barang', key='stock_warna')
st.text_input('Ukuran Barang', key='stock_ukuran')
st.number_input('Jumlah Barang', key='stock_jumlah', min_value=1)
st.number_input('Harga Barang', key='stock_harga', min_value=0)

if st.button('Update Stock'):
    id_barang = st.session_state.stock_id
    nama = st.session_state.stock_nama
    jenis = st.session_state.stock_jenis
    warna = st.session_state.stock_warna
    ukuran = st.session_state.stock_ukuran
    jumlah = st.session_state.stock_jumlah
    harga = st.session_state.stock_harga
    
    if id_barang and nama and jenis and warna and ukuran and jumlah and harga:
        new_row = {
            'ID': int(id_barang),
            'Nama': nama,
            'Jenis': jenis,
            'Warna': warna,
            'Ukuran': ukuran,
            'Jumlah': int(jumlah),
            'Harga': int(harga)
        }
        stock_data = stock_data.append(new_row, ignore_index=True)
        st.success('Data Stock Barang berhasil diperbarui!')
    st.plotly_chart(create_stock_fig())

# Bagian Finansial
st.subheader('Pemasukan dan Pengeluaran')
st.plotly_chart(create_financial_fig())

# Input untuk update Finansial
st.text_input('Kategori (Pendapatan/Pengeluaran)', key='financial_kategori')
st.number_input('Jumlah', key='financial_jumlah', min_value=0)

if st.button('Update Finansial'):
    kategori = st.session_state.financial_kategori
    jumlah = st.session_state.financial_jumlah
    if kategori and jumlah:
        financial_data = financial_data.append({'Kategori': kategori, 'Jumlah': int(jumlah)}, ignore_index=True)
        st.success('Data Finansial berhasil diperbarui!')
    st.plotly_chart(create_financial_fig())

# Bagian HR
st.subheader('Jumlah Karyawan Berdasarkan Posisi')
st.plotly_chart(create_hr_fig())

# Input untuk update HR
posisi = st.selectbox('Pilih Posisi', hr_data['Posisi'])
jumlah_karyawan = st.number_input('Jumlah Karyawan', key='hr_jumlah', min_value=0)

if st.button('Update HR'):
    if jumlah_karyawan > 0:
        hr_data.loc[hr_data['Posisi'] == posisi, 'Jumlah Karyawan'] = int(jumlah_karyawan)
        st.success(f'Jumlah Karyawan untuk posisi {posisi} berhasil diperbarui!')
    st.plotly_chart(create_hr_fig())
