import json
import os
from datetime import datetime
from typing import List, Dict

# File untuk menyimpan data
DATA_FILE = "tasks.json"

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
    
    def display_tasks(self) -> None:
        """Menampilkan semua tugas"""
        if not self.tasks:
            print("📭 Tidak ada tugas. Mulai tambahkan tugas baru!")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<5} {'NAMA TUGAS':<30} {'MATA PELAJARAN':<20} {'DEADLINE':<15} {'STATUS':<15}")
        print("="*100)
        
        for task in self.tasks:
            print(f"{task['id']:<5} {task['nama_tugas']:<30} {task['mata_pelajaran']:<20} {task['deadline']:<15} {task['status']:<15}")
        
        print("="*100 + "\n")
    
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
                return
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!")
    
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
                return
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!")
    
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
                        print("❌ Format tanggal salah! Gunakan format DD-MM-YYYY")
                        return
                
                self.save_tasks()
                print(f"✅ Tugas berhasil diperbarui!")
                return
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!")
    
    def search_tasks(self, keyword: str) -> None:
        """Mencari tugas berdasarkan kata kunci"""
        results = [task for task in self.tasks if keyword.lower() in task['nama_tugas'].lower() or keyword.lower() in task['mata_pelajaran'].lower()]
        
        if not results:
            print(f"❌ Tidak ada tugas yang cocok dengan '{keyword}'")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<5} {'NAMA TUGAS':<30} {'MATA PELAJARAN':<20} {'DEADLINE':<15} {'STATUS':<15}")
        print("="*100)
        
        for task in results:
            print(f"{task['id']:<5} {task['nama_tugas']:<30} {task['mata_pelajaran']:<20} {task['deadline']:<15} {task['status']:<15}")
        
        print("="*100 + "\n")
    
    def sort_by_deadline(self) -> None:
        """Menampilkan tugas yang diurutkan berdasarkan deadline"""
        sorted_tasks = sorted(self.tasks, key=lambda x: datetime.strptime(x['deadline'], "%d-%m-%Y"))
        
        if not sorted_tasks:
            print("📭 Tidak ada tugas!")
            return
        
        print("\n" + "="*100)
        print("📋 TUGAS DIURUTKAN BERDASARKAN DEADLINE:")
        print("="*100)
        print(f"{'ID':<5} {'NAMA TUGAS':<30} {'MATA PELAJARAN':<20} {'DEADLINE':<15} {'STATUS':<15}")
        print("="*100)
        
        for task in sorted_tasks:
            print(f"{task['id']:<5} {task['nama_tugas']:<30} {task['mata_pelajaran']:<20} {task['deadline']:<15} {task['status']:<15}")
        
        print("="*100 + "\n")
    
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
        
        print(f"❌ Tugas dengan ID {task_id} tidak ditemukan!")

def print_menu():
    """Menampilkan menu utama"""
    print("\n" + "="*50)
    print("📚 APLIKASI TODOLIST")
    print("="*50)
    print("1. 📋 Tampilkan Semua Tugas")
    print("2. ➕ Tambah Tugas Baru")
    print("3. ✏️  Edit Tugas")
    print("4. 🗑️  Hapus Tugas")
    print("5. 🔍 Cari Tugas")
    print("6. 📅 Urutkan Tugas berdasarkan Deadline")
    print("7. 📝 Lihat Detail Tugas")
    print("8. 🔄 Ubah Status Tugas")
    print("9. ❌ Keluar")
    print("="*50)

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
            nama_tugas = input("Nama Tugas: ").strip()
            if not nama_tugas:
                print("❌ Nama tugas tidak boleh kosong!")
                continue
            
            mata_pelajaran = input("Mata Pelajaran: ").strip()
            if not mata_pelajaran:
                print("❌ Mata pelajaran tidak boleh kosong!")
                continue
            
            deadline = input("Deadline (DD-MM-YYYY): ").strip()
            if not deadline:
                print("❌ Deadline tidak boleh kosong!")
                continue
            
            todo.add_task(nama_tugas, mata_pelajaran, deadline)
        
        elif pilihan == "3":
            # Edit tugas
            print("\n✏️  EDIT TUGAS")
            todo.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang ingin diedit: ").strip())
            except ValueError:
                print("❌ ID harus berupa angka!")
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
                print("❌ ID harus berupa angka!")
                continue
            
            todo.delete_task(task_id)
        
        elif pilihan == "5":
            # Cari tugas
            print("\n🔍 CARI TUGAS")
            keyword = input("Masukkan kata kunci pencarian: ").strip()
            if not keyword:
                print("❌ Kata kunci tidak boleh kosong!")
                continue
            
            todo.search_tasks(keyword)
        
        elif pilihan == "6":
            # Urutkan berdasarkan deadline
            todo.sort_by_deadline()
        
        elif pilihan == "7":
            # Lihat detail tugas
            print("\n📝 LIHAT DETAIL TUGAS")
            todo.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas: ").strip())
            except ValueError:
                print("❌ ID harus berupa angka!")
                continue
            
            todo.show_details(task_id)
        
        elif pilihan == "8":
            # Ubah status tugas
            print("\n🔄 UBAH STATUS TUGAS")
            todo.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas: ").strip())
            except ValueError:
                print("❌ ID harus berupa angka!")
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
                print("❌ Pilihan status tidak valid!")
        
        elif pilihan == "9":
            # Keluar
            print("\n👋 Terima kasih telah menggunakan Aplikasi TodoList!")
            break
        
        else:
            print("❌ Pilihan tidak valid! Silakan pilih menu 1-9.")

if __name__ == "__main__":
    main()
