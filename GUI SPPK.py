import tkinter as tk
from tkinter import ttk, messagebox
import math

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
        harga = float(entry_harga.get())
        garansi = float(entry_garansi.get())
        permintaan = float(entry_permintaan.get())

        if not nama:
            raise ValueError("Nama produk tidak boleh kosong!")

        # Tambahkan data ke list produk
        data_produk.append([nama, [pencahayaan, lifetime, harga, garansi, permintaan]])
        listbox_produk.insert(tk.END, f"{nama}: {pencahayaan}, {lifetime}, {harga}, {garansi}, {permintaan}")

        # Kosongkan input setelah tambah
        entry_nama.delete(0, tk.END)
        entry_pencahayaan.delete(0, tk.END)
        entry_lifetime.delete(0, tk.END)
        entry_harga.delete(0, tk.END)
        entry_garansi.delete(0, tk.END)
        entry_permintaan.delete(0, tk.END)

    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")
# Fungsi untuk Membuka GUI Hasil TOPSIS
def buka_hasil_topsis(hasil):
    # GUI Baru untuk Hasil
    hasil_window = tk.Toplevel(root)
    hasil_window.title("Hasil TOPSIS")

    # Hitung ukuran hasil untuk menyesuaikan ukuran window
    max_line_length = max(len(line) for line in hasil.split("\n"))
    num_lines = len(hasil.split("\n"))
    window_width = min(600, max_line_length * 8)  # Atur lebar maksimum
    window_height = min(400, num_lines * 25 + 100)  # Atur tinggi berdasarkan jumlah baris
    hasil_window.geometry(f"{window_width}x{window_height}")

    # Teks Hasil
    tk.Label(hasil_window, text="Hasil Peringkat TOPSIS", font=("Arial", 14)).pack(pady=10)
    hasil_text = tk.Text(hasil_window, wrap=tk.WORD, font=("Arial", 12))
    hasil_text.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
    hasil_text.insert(tk.END, hasil)
    hasil_text.config(state="disabled")  # Tidak bisa diedit

    # Frame Tombol
    frame_buttons = tk.Frame(hasil_window)
    frame_buttons.pack(pady=10)

    # Tombol Ulangi
    def ulangi():
        global data_produk
        data_produk.clear()  # Hapus semua data produk
        listbox_produk.delete(0, tk.END)  # Kosongkan Listbox
        hasil_window.destroy()  # Tutup jendela hasil

    btn_ulang = ttk.Button(frame_buttons, text="Ulangi", command=ulangi)
    btn_ulang.grid(row=0, column=0, padx=10)

    # Tombol Exit
    btn_exit = ttk.Button(frame_buttons, text="Exit", command=root.destroy)
    btn_exit.grid(row=0, column=1, padx=10)

# Fungsi untuk Menghitung TOPSIS
def hitung_topsis():
    if not data_produk:
        messagebox.showerror("Error", "Tidak ada data produk untuk dihitung.")
        return

    # Ekstrak data kriteria
    alternatif = [item[0] for item in data_produk]
    data = [item[1] for item in data_produk]

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

    # Hasil Peringkat
    hasil = sorted(zip(alternatif, skor), key=lambda x: x[1], reverse=True)
    hasil_text = "\n".join([f"{i+1}. {item[0]}: {item[1]:.4f}" for i, item in enumerate(hasil)])

    # Menambahkan Rekomendasi
    rekomendasi = f"\nRekomendasi: Prioritaskan {hasil[0][0]} untuk pengisian stok."

    #gabungan hasil peringkat dan rekomendasi 
    output = f"Peringkat:\n{hasil_text}{rekomendasi}"
    # Buka GUI Hasil
    buka_hasil_topsis(output)

# GUI Tkinter
root = tk.Tk()
root.title("Aplikasi TOPSIS")
root.geometry("800x600")

# Frame untuk Input Data
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(frame_input, text="Input Data Produk", font=("Arial", 14)).pack(pady=10)

tk.Label(frame_input, text="Nama Produk:").pack(anchor="w")
entry_nama = ttk.Entry(frame_input, width=30)
entry_nama.pack()

tk.Label(frame_input, text="Pencahayaan (Lumens):").pack(anchor="w")
entry_pencahayaan = ttk.Entry(frame_input, width=30)
entry_pencahayaan.pack()

tk.Label(frame_input, text="Life Time (Jam):").pack(anchor="w")
entry_lifetime = ttk.Entry(frame_input, width=30)
entry_lifetime.pack()

tk.Label(frame_input, text="Harga Satuan (Rp):").pack(anchor="w")
entry_harga = ttk.Entry(frame_input, width=30)
entry_harga.pack()

tk.Label(frame_input, text="Garansi (Tahun):").pack(anchor="w")
entry_garansi = ttk.Entry(frame_input, width=30)
entry_garansi.pack()

tk.Label(frame_input, text="Permintaan (Unit/Bulan):").pack(anchor="w")
entry_permintaan = ttk.Entry(frame_input, width=30)
entry_permintaan.pack()

btn_tambah = ttk.Button(frame_input, text="Tambah", command=tambah_produk)
btn_tambah.pack(pady=10)

# Frame untuk List Produk
frame_list = tk.Frame(root, padx=10, pady=10)
frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(frame_list, text="Daftar Produk", font=("Arial", 14)).pack(pady=10)

listbox_produk = tk.Listbox(frame_list, width=50, height=20)
listbox_produk.pack(pady=10, fill=tk.BOTH, expand=True)

btn_hitung = ttk.Button(frame_list, text="Hitung TOPSIS", command=hitung_topsis)
btn_hitung.pack(pady=10)

# Jalankan GUI
root.mainloop()
