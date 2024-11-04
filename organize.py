import os
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

current_dir = Path(os.getcwd())
watch_folder = current_dir
base_folder = current_dir

os.makedirs(base_folder, exist_ok=True)

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        organize_files()

def organize_files():
    for filename in os.listdir(watch_folder):
        file_path = watch_folder / filename
        if file_path.is_file() and "_" in filename:
            parts = filename.split("_")
            if len(parts) > 3:
                category = parts[3].split(".")[0].lower()
                category_folder = base_folder / category
                os.makedirs(category_folder, exist_ok=True)
                shutil.move(file_path, category_folder / filename)
                print(f"ย้ายไฟล์ {filename} ไปยังหมวดหมู่ {category}")
            else:
                print(f"ไม่สามารถจัดระเบียบไฟล์ {filename} ได้ เพราะไม่มีหมวดหมู่ที่ถูกต้อง")

if __name__ == "__main__":
    organize_files()

    if not watch_folder.exists():
        print(f"ไม่พบโฟลเดอร์ 'Work' ที่ตำแหน่ง: {current_dir}")
    else:
        event_handler = NewFileHandler()
        observer = Observer()
        observer.schedule(event_handler, str(watch_folder), recursive=False)
        observer.start()
        try:
            print(f"กำลังตรวจสอบไฟล์ใหม่ในโฟลเดอร์: {watch_folder}")
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
