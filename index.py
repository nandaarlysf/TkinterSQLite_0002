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

