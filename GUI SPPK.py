import tkinter as tk
from tkinter import ttk, messagebox
import math
from sklearn import tree

# Variabel Global
kriteria = ['Pencahayaan', 'Life Time', 'Harga Satuan', 'Garansi', 'Permintaan']
costbenefit = ['benefit', 'benefit', 'cost', 'benefit', 'benefit']
bobot = [5, 4, 4, 3, 4]
data_produk = []

# Fungsi untuk Menambahkan Data Produk
def tambah_produk():
    try:
        nama = entry_nama.get()
        pencahayaan = float(entry_pencahayaan.get())
        lifetime = float(entry_lifetime.get())
        harga = (entry_harga.get())
        garansi = float(entry_garansi.get())
        permintaan = float(entry_permintaan.get())

        if not nama:
            raise ValueError("Nama produk tidak boleh kosong!")
        
        formatted_harga = format_rupiah(harga)
        harga=float(harga)
        
        data_produk.append([nama, pencahayaan, lifetime, harga, garansi, permintaan])
        tree.insert("", "end", values=(nama, pencahayaan, lifetime, formatted_harga, garansi, permintaan))
        
        # Kosongkan input setelah tambah
        entry_nama.delete(0, tk.END)
        entry_pencahayaan.delete(0, tk.END)
        entry_lifetime.delete(0, tk.END)
        entry_harga.delete(0, tk.END)
        entry_garansi.delete(0, tk.END)
        entry_permintaan.delete(0, tk.END)

    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")


# Fungsi untuk memformat harga menjadi format Rupiah
def format_rupiah(value):
    try:
        value = ''.join(filter(str.isdigit, value))
        if value == '':
            return ''
        formatted_value = '{:,}'.format(int(value)) 
        return 'Rp ' + formatted_value
    except ValueError:
        return 'Rp 0'

# Fungsi untuk update harga dengan format Rupiah
def update_harga(*args):
    harga = entry_harga.get()
    formatted_harga = format_rupiah(harga)
    entry_harga.delete(0, tk.END)
    entry_harga.insert(0, formatted_harga)
    
# Fungsi untuk validasi input angka
def validasi_input_angka(P):
    if P == "" or P.replace(".", "", 1).isdigit():
        return True
    else:
        return False
    
def center_window(window, width, height):
    # Mendapatkan ukuran layar
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Menghitung posisi untuk menempatkan jendela di tengah
    position_top = int(screen_height / 2 - height / 2)
    position_left = int(screen_width / 2 - width / 2)
    
# Fungsi untuk Membuka GUI Hasil TOPSIS
def buka_hasil_topsis(hasil):
    root.withdraw()
    # GUI Baru untuk Hasil
    hasil_window = tk.Toplevel(root)
    hasil_window.title("Hasil Perhitungan Rekomendasi")
    hasil_window.geometry("800x600")
    center_window(hasil_window, 800, 600)

    # Label untuk Judul
    tk.Label(hasil_window, text="Peringkat Rekomendasi Re-Stock", font=("Arial", 16, "bold")).pack(pady=10)

    # Frame untuk Tabel
    frame_table = tk.Frame(hasil_window)
    frame_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Membuat Tabel
    tree = ttk.Treeview(frame_table, columns=("Peringkat", "Nama Produk", "Skor","Rekomendasi"), show="headings", height=10)
    tree.pack(fill=tk.BOTH, expand=True)

    # Atur Judul Kolom
    tree.heading("Peringkat", text="Peringkat", anchor="center")
    tree.heading("Nama Produk", text="Nama Produk", anchor="center")
    tree.heading("Skor", text="Skor", anchor="center")
    tree.heading("Rekomendasi", text="Rekomendasi", anchor="center")

    # Atur Lebar Kolom
    tree.column("Peringkat", width=100, anchor="center")
    tree.column("Nama Produk", width=100, anchor="center")
    tree.column("Skor", width=100, anchor="center")
    tree.column("Rekomendasi", width=100, anchor="center")
    
    rekomendasi_tertinggi = hasil[0][0]

    # Menambahkan Data ke Tabel
    for i, (nama, skor) in enumerate(hasil, start=1):
        rekomendasi = "Prioritaskan untuk diberikan pengisian stok" if nama == rekomendasi_tertinggi else "Lakukan Pengisian Stok secara normal"
        tree.insert("", "end", values=(i, nama, f"{skor:.4f}", rekomendasi))

    # Frame Tombol
    frame_buttons = tk.Frame(hasil_window)
    frame_buttons.pack(pady=10)

    # Tombol Ulangi
    def ulangi():
        global data_produk
        data_produk.clear()  # Hapus semua data produk
        
        # Menghapus data dalam Treeview
        for item in tree.get_children():
            tree.delete(item)
        
        hasil_window.destroy()
        frame_input.destroy()
        baru()

    btn_ulang = ttk.Button(frame_buttons, text="Ulangi", command=ulangi)
    btn_ulang.grid(row=0, column=0, padx=10)

    # Tombol Exit
    def keluar():
        hasil_window.destroy()  # Tutup jendela hasil
        root.destroy()  # Tutup aplikasi utama

    btn_exit = ttk.Button(frame_buttons, text="Exit", command=keluar)
    btn_exit.grid(row=0, column=1, padx=10)
    
# Fungsi untuk Menghitung TOPSIS
def hitung_topsis():
    if not data_produk:
        messagebox.showerror("Error", "Tidak ada data produk untuk dihitung.")
        return
    
    # Ekstrak data kriteria
    alternatif = [item[0] for item in data_produk]
    data = [item[1:] for item in data_produk]

    # Langkah 1: Hitung pembagi
    pembagi = [math.sqrt(sum(row[j] ** 2 for row in data)) for j in range(len(kriteria))]

    # Langkah 2: Normalisasi
    normalisasi = [[row[j] / pembagi[j] for j in range(len(kriteria))] for row in data]

    # Langkah 3: Normalisasi Terbobot
    normalisasi_terbobot = [[normalisasi[i][j] * bobot[j] for j in range(len(kriteria))] for i in range(len(data))]

    # Langkah 4: Solusi Ideal Positif dan Negatif
    solusi_ideal_positif = [max(column) if costbenefit[j] == 'benefit' else min(column)
                            for j, column in enumerate(zip(*normalisasi_terbobot))]
    solusi_ideal_negatif = [min(column) if costbenefit[j] == 'benefit' else max(column)
                            for j, column in enumerate(zip(*normalisasi_terbobot))]

    # Langkah 5: Jarak ke Solusi Ideal Positif dan Negatif
    jarak_positif = [math.sqrt(sum((normalisasi_terbobot[i][j] - solusi_ideal_positif[j]) ** 2
                                   for j in range(len(kriteria)))) for i in range(len(data))]
    jarak_negatif = [math.sqrt(sum((normalisasi_terbobot[i][j] - solusi_ideal_negatif[j]) ** 2
                                   for j in range(len(kriteria)))) for i in range(len(data))]

    # Langkah 6: Hitung Skor Akhir
    skor = [jarak_negatif[i] / (jarak_positif[i] + jarak_negatif[i]) for i in range(len(data))]

    """# Hasil Peringkat
    hasil = sorted(zip(alternatif, skor), key=lambda x: x[1], reverse=True)
    hasil_text = "\n".join([f"{i+1}. {item[0]}: {item[1]:.4f}" for i, item in enumerate(hasil)])

    # Menambahkan Rekomendasi
    rekomendasi = f"\nRekomendasi: Prioritaskan {hasil[0][0]} untuk pengisian stok."

    # Gabungan hasil peringkat dan rekomendasi 
    output = f"Peringkat:\n{hasil_text}{rekomendasi}"
    # Tampilkan Hasil
    buka_hasil_topsis(output)"""

    # Hasil Peringkat
    hasil = sorted(zip(alternatif, skor), key=lambda x: x[1], reverse=True)

    # Menampilkan Hasil dalam Bentuk Tabel
    buka_hasil_topsis(hasil)

root = tk.Tk()
root.title("Rekomendasi Stok Barang Toko Lampu")
root.geometry('900x600')  # Ukuran jendela yang lebih lebar

# Frame untuk Input Data (kiri)
frame_input = tk.Frame(root, padx=20, pady=20)
frame_input.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

tk.Label(frame_input, text="Input Data Produk", font=("Arial", 14, "bold")).pack(pady=10)

# Membuat validasi command untuk hanya menerima angka
vcmd = (root.register(validasi_input_angka), '%P')

# Menambahkan label dan entry field
tk.Label(frame_input, text="Nama Produk:").pack(anchor="w", pady=5)
entry_nama = ttk.Entry(frame_input, width=30)
entry_nama.pack(pady=5)

tk.Label(frame_input, text="Pencahayaan (Lumens):").pack(anchor="w", pady=5)
entry_pencahayaan = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
entry_pencahayaan.pack(pady=5)

tk.Label(frame_input, text="Life Time (Jam):").pack(anchor="w", pady=5)
entry_lifetime = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
entry_lifetime.pack(pady=5)

tk.Label(frame_input, text="Harga Satuan (Rp):").pack(anchor="w", pady=5)
entry_harga = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
entry_harga.pack(pady=5)


tk.Label(frame_input, text="Garansi (Tahun):").pack(anchor="w", pady=5)
entry_garansi = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
entry_garansi.pack(pady=5)

tk.Label(frame_input, text="Permintaan (Unit/Bulan):").pack(anchor="w", pady=5)
entry_permintaan = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
entry_permintaan.pack(pady=5)

# Tombol untuk tambah produk
btn_tambah = ttk.Button(frame_input, text="Tambah", command=tambah_produk)
btn_tambah.pack(pady=10)

# Frame untuk List Produk (kanan)
frame_list = tk.Frame(root, padx=20, pady=20)
frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Membuat Treeview untuk menampilkan tabel produk
tree = ttk.Treeview(frame_list, columns=("Nama", "Pencahayaan", "Lifetime", "Harga", "Garansi", "Permintaan"), show="headings")
tree.pack(fill="both", expand=True)

# Atur judul kolom
tree.heading("Nama", text="Nama Produk")
tree.heading("Pencahayaan", text="Pencahayaan")
tree.heading("Lifetime", text="Lifetime")
tree.heading("Harga", text="Harga")
tree.heading("Garansi", text="Garansi")
tree.heading("Permintaan", text="Permintaan")

# Atur lebar kolom
tree.column("Nama", width=150, anchor="center")
tree.column("Pencahayaan", width=100, anchor="center")
tree.column("Lifetime", width=100, anchor="center")
tree.column("Harga", width=100, anchor="center")
tree.column("Garansi", width=100, anchor="center")
tree.column("Permintaan", width=100, anchor="center")

# Tombol Hitung TOPSIS
btn_hitung = ttk.Button(frame_list, text="Hitung Rekomendasi", command=hitung_topsis)
btn_hitung.pack(pady=10)

def baru():
    root = tk.Tk()
    root.title("Rekomendasi Stok Barang Toko Lampu")
    root.geometry('900x600')  # Ukuran jendela yang lebih lebar

    # Frame untuk Input Data (kiri)
    frame_input = tk.Frame(root, padx=20, pady=20)
    frame_input.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_input, text="Input Data Produk", font=("Arial", 14, "bold")).pack(pady=10)

    # Membuat validasi command untuk hanya menerima angka
    vcmd = (root.register(validasi_input_angka), '%P')

    # Menambahkan label dan entry field
    tk.Label(frame_input, text="Nama Produk:").pack(anchor="w", pady=5)
    entry_nama = ttk.Entry(frame_input, width=30)
    entry_nama.pack(pady=5)

    tk.Label(frame_input, text="Pencahayaan (Lumens):").pack(anchor="w", pady=5)
    entry_pencahayaan = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
    entry_pencahayaan.pack(pady=5)

    tk.Label(frame_input, text="Life Time (Jam):").pack(anchor="w", pady=5)
    entry_lifetime = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
    entry_lifetime.pack(pady=5)

    tk.Label(frame_input, text="Harga Satuan (Rp):").pack(anchor="w", pady=5)
    entry_harga = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
    entry_harga.pack(pady=5)
    
    tk.Label(frame_input, text="Garansi (Tahun):").pack(anchor="w", pady=5)
    entry_garansi = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
    entry_garansi.pack(pady=5)

    tk.Label(frame_input, text="Permintaan (Unit/Bulan):").pack(anchor="w", pady=5)
    entry_permintaan = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
    entry_permintaan.pack(pady=5)

    # Tombol untuk tambah produk
    btn_tambah = ttk.Button(frame_input, text="Tambah", command=tambah_produk)
    btn_tambah.pack(pady=10)

    # Frame untuk List Produk (kanan)
    frame_list = tk.Frame(root, padx=20, pady=20)
    frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Membuat Treeview untuk menampilkan tabel produk
    tree = ttk.Treeview(frame_list, columns=("Nama", "Pencahayaan", "Lifetime", "Harga", "Garansi", "Permintaan"), show="headings")
    tree.pack(fill="both", expand=True)

    # Atur judul kolom
    tree.heading("Nama", text="Nama Produk")
    tree.heading("Pencahayaan", text="Pencahayaan")
    tree.heading("Lifetime", text="Lifetime")
    tree.heading("Harga", text="Harga")
    tree.heading("Garansi", text="Garansi")
    tree.heading("Permintaan", text="Permintaan")

    # Atur lebar kolom
    tree.column("Nama", width=150, anchor="center")
    tree.column("Pencahayaan", width=100, anchor="center")
    tree.column("Lifetime", width=100, anchor="center")
    tree.column("Harga", width=100, anchor="center")
    tree.column("Garansi", width=100, anchor="center")
    tree.column("Permintaan", width=100, anchor="center")

    # Tombol Hitung TOPSIS
    btn_hitung = ttk.Button(frame_list, text="Hitung Rekomendasi", command=hitung_topsis)
    btn_hitung.pack(pady=10)
    root.iconbitmap('logo.ico')
    root.mainloop()

root.iconbitmap('logo.ico')
root.mainloop()

