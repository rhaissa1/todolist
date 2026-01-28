import json
import os
import platform
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict
from tabulate import tabulate

# Import winsound hanya untuk Windows
if platform.system() == "Windows":
    import winsound

# File untuk menyimpan data
DATA_FILE = "tasks.json"

# Kata-kata semangat motivasi
MOTIVASI = [
    "💪 Kamu bisa! Jangan menyerah!",
    "🌟 Setiap tugas selesai adalah pencapaian!",
    "⚡ Semangat! Kamu lebih kuat dari yang kamu kira!",
    "🎯 Fokus pada target, sukses ada di depan!",
    "🚀 Terbang tinggi menuju kesuksesan!",
    "✨ Kamu adalah bintang yang bersinar terang!",
    "🏆 Jadilah versi terbaik dari dirimu!",
    "💖 Cinta diri sendiri dengan menyelesaikan tugas!",
    "🌈 Setelah hujan datanglah pelangi kesuksesan!",
    "🎪 Hidup adalah petualangan, nikmati perjalanannya!",
    "🎨 Kamu melukis masa depanmu dengan kerja keras!",
    "🌺 Berkembanglah seperti bunga di musim semi!",
    "🦋 Transformasi kecil menuju kesuksesan besar!",
    "🌙 Malam gelap pasti akan berganti dengan fajar!",
    "☀️ Setiap hari adalah kesempatan baru untuk bersinar!"
]

def get_motivasi_random():
    """Menampilkan kata motivasi random"""
    return random.choice(MOTIVASI)

def show_cute_animation():
    """Menampilkan animasi imut"""
    animasi = ["◜◝◜◝", "◝◜◝◜"]
    for _ in range(3):
        for anim in animasi:
            print(f"\r  {anim}  Sedang memproses...  {anim}  ", end="", flush=True)
            time.sleep(0.3)
    print("\r✅ Selesai!                          \n")

class TodoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Memuat data tugas dari file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Menyimpan data tugas ke file"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
    
    def add_task(self, nama_tugas: str, mata_pelajaran: str, deadline: str) -> None:
        """Menambah tugas baru"""
        # Validasi format tanggal
        try:
            datetime.strptime(deadline, "%d-%m-%Y")
        except ValueError:
            print("❌ Format tanggal salah! Gunakan format DD-MM-YYYY")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "nama_tugas": nama_tugas,
            "mata_pelajaran": mata_pelajaran,
            "deadline": deadline,
            "status": "Belum Selesai",
            "tanggal_dibuat": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Tugas '{nama_tugas}' berhasil ditambahkan!")
        print(f"📝 {get_motivasi_random()}\n")
    
    def display_tasks(self) -> None:
        """Menampilkan semua tugas dengan format tabel, diurutkan berdasarkan deadline tercepat"""
        if not self.tasks:
            print("📭 Tidak ada tugas. Mulai tambahkan tugas baru!")
            print(f"💌 {get_motivasi_random()}\n")
            return
        
        # Urutkan berdasarkan deadline tercepat
        sorted_tasks = sorted(self.tasks, key=lambda x: datetime.strptime(x['deadline'], "%d-%m-%Y"))
        
        table_data = []
        for task in sorted_tasks:
            status_emoji = self._get_status_emoji(task['status'])
            table_data.append([
                task['id'],
                task['nama_tugas'],
                task['mata_pelajaran'],
                task['deadline'],
                f"{status_emoji} {task['status']}"
            ])
        
        print("\n")
        print(tabulate(table_data, 
                      headers=["ID", "NAMA TUGAS", "MATA PELAJARAN", "DEADLINE", "STATUS"],
                      tablefmt="grid",
                      stralign="left"))
        print()
    
    def delete_task(self, task_id: int) -> None:
        """Menghapus tugas berdasarkan ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                nama = task['nama_tugas']
                self.tasks.remove(task)
                # Perbarui ID setelah penghapusan
                for i, t in enumerate(self.tasks, 1):
                    t['id'] = i
                self.save_tasks()
                print(f"✅ Tugas '{nama}' berhasil dihapus!")
                print(f"💪 {get_motivasi_random()}\n")
                return
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!\n")
    
    def update_task_status(self, task_id: int, status: str) -> None:
        """Mengubah status tugas"""
        status_valid = ["Belum Selesai", "Sedang Dikerjakan", "Selesai"]
        
        if status not in status_valid:
            print(f"❌ Status tidak valid! Pilih dari: {', '.join(status_valid)}")
            return
        
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                self.save_tasks()
                print(f"✅ Status tugas '{task['nama_tugas']}' diubah menjadi '{status}'!")
                if status == "Selesai":
                    print("🎉 Hebat! Kamu telah menyelesaikan satu tugas!")
                    print(f"   {get_motivasi_random()}\n")
                else:
                    print()
                return
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!\n")
    
    def edit_task(self, task_id: int, nama_tugas: str = None, mata_pelajaran: str = None, deadline: str = None) -> None:
        """Mengedit tugas"""
        for task in self.tasks:
            if task['id'] == task_id:
                if nama_tugas:
                    task['nama_tugas'] = nama_tugas
                if mata_pelajaran:
                    task['mata_pelajaran'] = mata_pelajaran
                if deadline:
                    try:
                        datetime.strptime(deadline, "%d-%m-%Y")
                        task['deadline'] = deadline
                    except ValueError:
                        print("❌ Format tanggal salah! Gunakan format DD-MM-YYYY\n")
                        return
                
                self.save_tasks()
                print(f"✅ Tugas berhasil diperbarui!\n")
                return
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!\n")
    
    def search_tasks(self, keyword: str) -> None:
        """Mencari tugas berdasarkan kata kunci"""
        results = [task for task in self.tasks if keyword.lower() in task['nama_tugas'].lower() or keyword.lower() in task['mata_pelajaran'].lower()]
        
        if not results:
            print(f"❌ Tidak ada tugas yang cocok dengan '{keyword}'\n")
            return
        
        # Urutkan berdasarkan deadline
        sorted_results = sorted(results, key=lambda x: datetime.strptime(x['deadline'], "%d-%m-%Y"))
        
        table_data = []
        for task in sorted_results:
            status_emoji = self._get_status_emoji(task['status'])
            table_data.append([
                task['id'],
                task['nama_tugas'],
                task['mata_pelajaran'],
                task['deadline'],
                f"{status_emoji} {task['status']}"
            ])
        
        print("\n")
        print(tabulate(table_data, 
                      headers=["ID", "NAMA TUGAS", "MATA PELAJARAN", "DEADLINE", "STATUS"],
                      tablefmt="grid",
                      stralign="left"))
        print()
    
    def sort_by_deadline(self) -> None:
        """Menampilkan tugas yang diurutkan berdasarkan deadline"""
        sorted_tasks = sorted(self.tasks, key=lambda x: datetime.strptime(x['deadline'], "%d-%m-%Y"))
        
        if not sorted_tasks:
            print("📭 Tidak ada tugas!")
            return
        
        table_data = []
        for task in sorted_tasks:
            status_emoji = self._get_status_emoji(task['status'])
            table_data.append([
                task['id'],
                task['nama_tugas'],
                task['mata_pelajaran'],
                task['deadline'],
                f"{status_emoji} {task['status']}"
            ])
        
        print("\n📋 TUGAS DIURUTKAN BERDASARKAN DEADLINE:\n")
        print(tabulate(table_data, 
                      headers=["ID", "NAMA TUGAS", "MATA PELAJARAN", "DEADLINE", "STATUS"],
                      tablefmt="grid",
                      stralign="left"))
        print()
    
    def show_details(self, task_id: int) -> None:
        """Menampilkan detail tugas"""
        for task in self.tasks:
            if task['id'] == task_id:
                print("\n" + "="*50)
                print("📝 DETAIL TUGAS")
                print("="*50)
                print(f"ID: {task['id']}")
                print(f"Nama Tugas: {task['nama_tugas']}")
                print(f"Mata Pelajaran: {task['mata_pelajaran']}")
                print(f"Deadline: {task['deadline']}")
                print(f"Status: {task['status']}")
                print(f"Tanggal Dibuat: {task['tanggal_dibuat']}")
                print("="*50 + "\n")
                return
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!\n")
    
    def _get_status_emoji(self, status: str) -> str:
        """Mengembalikan emoji berdasarkan status"""
        status_emojis = {
            "Belum Selesai": "⏳",
            "Sedang Dikerjakan": "⚙️",
            "Selesai": "✅"
        }
        return status_emojis.get(status, "❓")
    
    def check_upcoming_deadlines(self) -> None:
        """Mengecek dan memberikan alarm untuk tugas yang mendekati deadline"""
        today = datetime.now()
        upcoming_tasks = []
        
        for task in self.tasks:
            if task['status'] != "Selesai":
                deadline_date = datetime.strptime(task['deadline'], "%d-%m-%Y")
                days_left = (deadline_date - today).days
                
                # Alarm jika deadline dalam 3 hari ke depan
                if 0 <= days_left <= 3:
                    upcoming_tasks.append((task, days_left))
        
        if upcoming_tasks:
            print("\n" + "⚠️ " * 25)
            print("🚨 ALARM! ADA TUGAS YANG MENDEKATI DEADLINE!")
            print("⚠️ " * 25 + "\n")
            
            table_data = []
            for task, days_left in upcoming_tasks:
                if days_left == 0:
                    warning = "🔴 HARI INI!"
                elif days_left == 1:
                    warning = "🟠 BESOK!"
                else:
                    warning = f"🟡 {days_left} hari lagi"
                
                table_data.append([
                    task['id'],
                    task['nama_tugas'],
                    task['mata_pelajaran'],
                    task['deadline'],
                    warning
                ])
            
            print(tabulate(table_data, 
                          headers=["ID", "NAMA TUGAS", "MATA PELAJARAN", "DEADLINE", "⚠️ ALERT"],
                          tablefmt="grid",
                          stralign="left"))
            print()
            
            # Mainkan sound alarm
            self._play_alarm_sound()
        else:
            print("✅ Semua tugas masih aman, tidak ada yang mendekati deadline!\n")
    
    def _play_alarm_sound(self) -> None:
        """Memainkan suara alarm"""
        try:
            if platform.system() == "Windows":
                # Windows
                winsound.Beep(1000, 500)
                winsound.Beep(1000, 500)
            elif platform.system() == "Darwin":
                # macOS
                os.system("afplay /System/Library/Sounds/Alarm.aiff")
            else:
                # Linux
                print("\a" * 3)  # Bell character untuk Linux
        except Exception as e:
            print(f"(Tidak bisa memainkan alarm: {e})")

def print_menu():
    """Menampilkan menu utama"""
    print("\n" + "="*50)
    print("📚 APLIKASI TODOLIST 📚")
    print("="*50)
    print("1. 📋 Tampilkan Semua Tugas")
    print("2. ➕ Tambah Tugas Baru")
    print("3. ✏️  Edit Tugas")
    print("4. 🗑️  Hapus Tugas")
    print("5. 🔍 Cari Tugas")
    print("6. � Lihat Detail Tugas")
    print("7. 🔄 Ubah Status Tugas")
    print("8. 🚨 Cek Reminder/Alarm")
    print("9. ❌ Keluar")
    print("="*50)
    print(f"✨ {get_motivasi_random()} ✨\n")

def main():
    """Fungsi utama aplikasi"""
    todo = TodoList()
    
    while True:
        print_menu()
        pilihan = input("Pilih menu (1-9): ").strip()
        
        if pilihan == "1":
            # Tampilkan semua tugas
            todo.display_tasks()
        
        elif pilihan == "2":
            # Tambah tugas
            print("\n➕ TAMBAH TUGAS BARU")
            show_cute_animation()
            nama_tugas = input("Nama Tugas: ").strip()
            if not nama_tugas:
                print("❌ Nama tugas tidak boleh kosong!\n")
                continue
            
            mata_pelajaran = input("Mata Pelajaran: ").strip()
            if not mata_pelajaran:
                print("❌ Mata pelajaran tidak boleh kosong!\n")
                continue
            
            deadline = input("Deadline (DD-MM-YYYY): ").strip()
            if not deadline:
                print("❌ Deadline tidak boleh kosong!\n")
                continue
            
            todo.add_task(nama_tugas, mata_pelajaran, deadline)
        
        elif pilihan == "3":
            # Edit tugas
            print("\n✏️  EDIT TUGAS")
            todo.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang ingin diedit: ").strip())
            except ValueError:
                print("❌ ID harus berupa angka!\n")
                continue
            
            print("(Kosongkan input jika tidak ingin mengubah)")
            nama_tugas = input("Nama Tugas Baru: ").strip()
            mata_pelajaran = input("Mata Pelajaran Baru: ").strip()
            deadline = input("Deadline Baru (DD-MM-YYYY): ").strip()
            
            todo.edit_task(task_id, 
                          nama_tugas if nama_tugas else None,
                          mata_pelajaran if mata_pelajaran else None,
                          deadline if deadline else None)
        
        elif pilihan == "4":
            # Hapus tugas
            print("\n🗑️  HAPUS TUGAS")
            todo.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang ingin dihapus: ").strip())
            except ValueError:
                print("❌ ID harus berupa angka!\n")
                continue
            
            todo.delete_task(task_id)
        
        elif pilihan == "5":
            # Cari tugas
            print("\n🔍 CARI TUGAS")
            keyword = input("Masukkan kata kunci pencarian: ").strip()
            if not keyword:
                print("❌ Kata kunci tidak boleh kosong!\n")
                continue
            
            todo.search_tasks(keyword)
        
        elif pilihan == "6":
            # Lihat detail tugas
            print("\n📝 LIHAT DETAIL TUGAS")
            todo.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas: ").strip())
            except ValueError:
                print("❌ ID harus berupa angka!\n")
                continue
            
            todo.show_details(task_id)
        
        elif pilihan == "7":
            # Ubah status tugas
            print("\n🔄 UBAH STATUS TUGAS")
            todo.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas: ").strip())
            except ValueError:
                print("❌ ID harus berupa angka!\n")
                continue
            
            print("Status yang tersedia:")
            print("1. Belum Selesai")
            print("2. Sedang Dikerjakan")
            print("3. Selesai")
            status_pilihan = input("Pilih status (1-3): ").strip()
            
            status_map = {"1": "Belum Selesai", "2": "Sedang Dikerjakan", "3": "Selesai"}
            if status_pilihan in status_map:
                todo.update_task_status(task_id, status_map[status_pilihan])
            else:
                print("❌ Pilihan status tidak valid!\n")
        
        elif pilihan == "8":
            # Cek reminder/alarm
            print("\n🚨 CEK REMINDER/ALARM TUGAS")
            todo.check_upcoming_deadlines()
        
        elif pilihan == "9":
            # Keluar
            print("\n👋 Terima kasih telah menggunakan Aplikasi TodoList!")
            print(f"🌟 {get_motivasi_random()} 🌟")
            print("💝 Sampai jumpa lagi!\n")
            break
        
        else:
            print("❌ Pilihan tidak valid! Silakan pilih menu 1-9.\n")

if __name__ == "__main__":
    main()
