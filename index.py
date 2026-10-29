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

    