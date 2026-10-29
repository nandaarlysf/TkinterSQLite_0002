import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


DB_NAME = "prediksi_diabetes.db"


def koneksi_database():
    return sqlite3.connect(DB_NAME)


def buat_tabel():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien TEXT NOT NULL,
            usia INTEGER NOT NULL,
            gula_darah REAL NOT NULL,
            bmi REAL NOT NULL,
            riwayat_ortu TEXT NOT NULL,
            hasil_prediksi TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def prediksi_diabetes(gula_darah, bmi, riwayat_ortu):
  
    if gula_darah >= 200:
        if bmi >= 30 or riwayat_ortu == "Ya":
            return "Sangat Tinggi"
        return "Tinggi"

    elif 140 <= gula_darah < 200:
        if bmi >= 30 and riwayat_ortu == "Ya":
            return "Tinggi"
        return "Sedang"

    else:
        if bmi >= 30:
            if riwayat_ortu == "Ya":
                return "Sedang"
            return "Waspada"

        elif riwayat_ortu == "Ya":
            return "Waspada"

        else:
            return "Rendah"

def simpan_data():
    nama = entry_nama.get().strip()
    usia_text = entry_usia.get().strip()
    gula_text = entry_gula.get().strip()
    bmi_text = entry_bmi.get().strip()
    riwayat = combo_riwayat.get()

    # Validasi input kosong
    if not nama or not usia_text or not gula_text or not bmi_text:
        messagebox.showwarning(
            "Peringatan",
            "Semua kolom wajib diisi!"
        )
        return

    if riwayat not in ("Ya", "Tidak"):
        messagebox.showwarning(
            "Peringatan",
            "Pilih riwayat diabetes orang tua!"
        )
        return

    # Validasi angka
    try:
        usia = int(usia_text)
        gula_darah = float(gula_text.replace(",", "."))
        bmi = float(bmi_text.replace(",", "."))

    except ValueError:
        messagebox.showerror(
            "Input Tidak Valid",
            "Usia harus berupa bilangan bulat, "
            "sedangkan gula darah dan BMI harus berupa angka."
        )
        return

    if usia < 1 or usia > 120:
        messagebox.showerror(
            "Input Tidak Valid",
            "Usia harus antara 1 dan 120 tahun."
        )
        return

    if not 0 < gula_darah <= 1000:
        messagebox.showerror(
            "Input Tidak Valid",
            "Kadar gula darah harus lebih dari 0 "
            "dan tidak melebihi 1000 mg/dL."
        )
        return

    if not 0 < bmi <= 100:
        messagebox.showerror(
            "Input Tidak Valid",
            "BMI harus lebih dari 0 dan tidak melebihi 100."
        )
        return

    # Hitung hasil prediksi
    hasil = prediksi_diabetes(
        gula_darah,
        bmi,
        riwayat
    )

    # Simpan ke database
    conn = koneksi_database()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO pasien (
                nama_pasien,
                usia,
                gula_darah,
                bmi,
                riwayat_ortu,
                hasil_prediksi
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nama,
            usia,
            gula_darah,
            bmi,
            riwayat,
            hasil
        ))

        conn.commit()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Kesalahan Database",
            f"Gagal menyimpan data:\n{error}"
        )
        return

    finally:
        conn.close()

    # Tampilkan hasil prediksi
    label_hasil.config(
        text=f"Hasil Prediksi: {hasil}"
    )

    messagebox.showinfo(
        "Berhasil",
        f"Data pasien berhasil disimpan!\n\n"
        f"Nama: {nama}\n"
        f"Usia: {usia} tahun\n"
        f"Gula Darah: {gula_darah:g} mg/dL\n"
        f"BMI: {bmi:g}\n"
        f"Riwayat Diabetes Orang Tua: {riwayat}\n"
        f"Hasil Prediksi: {hasil}"
    )

    tampilkan_data()
    bersihkan_form()



def tampilkan_data():
    for item in tabel.get_children():
        tabel.delete(item)

    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nama_pasien,
            usia,
            gula_darah,
            bmi,
            riwayat_ortu,
            hasil_prediksi
        FROM pasien
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    for row in data:
        tabel.insert("", tk.END, values=row)

def bersihkan_form():
    entry_nama.delete(0, tk.END)
    entry_usia.delete(0, tk.END)
    entry_gula.delete(0, tk.END)
    entry_bmi.delete(0, tk.END)

    combo_riwayat.set("Tidak")
    label_hasil.config(text="Hasil Prediksi: -")

buat_tabel()

root = tk.Tk()
root.title("Aplikasi Prediksi Risiko Diabetes")
root.geometry("1050x680")
root.minsize(900, 600)
root.configure(bg="#F0F4F8")

header = tk.Frame(
    root,
    bg="#1565C0",
    height=75
)

header.pack(fill="x")
header.pack_propagate(False)

judul = tk.Label(
    header,
    text="APLIKASI PREDIKSI RISIKO DIABETES",
    font=("Arial", 18, "bold"),
    bg="#1565C0",
    fg="white"
)

judul.pack(pady=20)

frame_form = tk.LabelFrame(
    root,
    text="Form Input Data Pasien",
    font=("Arial", 11, "bold"),
    bg="white",
    padx=20,
    pady=15
)

frame_form.pack(
    fill="x",
    padx=20,
    pady=15
)


# Nama pasien
tk.Label(
    frame_form,
    text="Nama Pasien",
    bg="white",
    font=("Arial", 10)
).grid(row=0, column=0, sticky="w", pady=7)

entry_nama = ttk.Entry(
    frame_form,
    width=30
)

entry_nama.grid(
    row=0,
    column=1,
    padx=10,
    pady=7
)


# Usia
tk.Label(
    frame_form,
    text="Usia (tahun)",
    bg="white",
    font=("Arial", 10)
).grid(row=1, column=0, sticky="w", pady=7)

entry_usia = ttk.Entry(
    frame_form,
    width=30
)

entry_usia.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# Gula darah
tk.Label(
    frame_form,
    text="Gula Darah (mg/dL)",
    bg="white",
    font=("Arial", 10)
).grid(row=0, column=2, sticky="w", pady=7, padx=(30, 0))

entry_gula = ttk.Entry(
    frame_form,
    width=30
)

entry_gula.grid(
    row=0,
    column=3,
    padx=10,
    pady=7
)


# BMI
tk.Label(
    frame_form,
    text="BMI",
    bg="white",
    font=("Arial", 10)
).grid(row=1, column=2, sticky="w", pady=7, padx=(30, 0))

entry_bmi = ttk.Entry(
    frame_form,
    width=30
)

entry_bmi.grid(
    row=1,
    column=3,
    padx=10,
    pady=7
)


# Riwayat diabetes orang tua
tk.Label(
    frame_form,
    text="Riwayat Diabetes Orang Tua",
    bg="white",
    font=("Arial", 10)
).grid(row=2, column=0, sticky="w", pady=7)

combo_riwayat = ttk.Combobox(
    frame_form,
    values=["Ya", "Tidak"],
    state="readonly",
    width=27
)

combo_riwayat.grid(
    row=2,
    column=1,
    padx=10,
    pady=7,
    sticky="w"
)

combo_riwayat.set("Tidak")

frame_tombol = tk.Frame(
    root,
    bg="#F0F4F8"
)

frame_tombol.pack(
    fill="x",
    padx=20,
    pady=5
)


btn_simpan = tk.Button(
    frame_tombol,
    text="Simpan & Prediksi",
    command=simpan_data,
    bg="#2E7D32",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=8
)

btn_simpan.pack(side="left", padx=5)


btn_bersihkan = tk.Button(
    frame_tombol,
    text="Bersihkan Form",
    command=bersihkan_form,
    bg="#EF6C00",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=8
)

btn_bersihkan.pack(side="left", padx=5)


btn_refresh = tk.Button(
    frame_tombol,
    text="Muat Ulang Data",
    command=tampilkan_data,
    bg="#1565C0",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=8
)

btn_refresh.pack(side="left", padx=5)

label_hasil = tk.Label(
    root,
    text="Hasil Prediksi: -",
    font=("Arial", 13, "bold"),
    bg="#F0F4F8",
    fg="#1565C0"
)

label_hasil.pack(pady=10)

frame_tabel = tk.LabelFrame(
    root,
    text="Riwayat Data Pasien",
    font=("Arial", 11, "bold"),
    bg="white",
    padx=10,
    pady=10
)

frame_tabel.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(5, 15)
)


kolom = (
    "id",
    "nama_pasien",
    "usia",
    "gula_darah",
    "bmi",
    "riwayat_ortu",
    "hasil_prediksi"
)

tabel = ttk.Treeview(
    frame_tabel,
    columns=kolom,
    show="headings"
)

tabel.heading("id", text="ID")
tabel.heading("nama_pasien", text="Nama Pasien")
tabel.heading("usia", text="Usia")
tabel.heading("gula_darah", text="Gula Darah")
tabel.heading("bmi", text="BMI")
tabel.heading("riwayat_ortu", text="Riwayat Ortu")
tabel.heading("hasil_prediksi", text="Hasil Prediksi")

tabel.column("id", width=45, anchor="center")
tabel.column("nama_pasien", width=180)
tabel.column("usia", width=70, anchor="center")
tabel.column("gula_darah", width=110, anchor="center")
tabel.column("bmi", width=80, anchor="center")
tabel.column("riwayat_ortu", width=120, anchor="center")
tabel.column("hasil_prediksi", width=130, anchor="center")


scrollbar = ttk.Scrollbar(
    frame_tabel,
    orient="vertical",
    command=tabel.yview
)

tabel.configure(
    yscrollcommand=scrollbar.set
)

tabel.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)

tampilkan_data()

root.mainloop()
