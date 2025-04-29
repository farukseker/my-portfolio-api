import os

root_dir = r"C:\Users\seker\PycharmProjects\f4v2cv"  # hedef dizin


for dirpath, dirnames, filenames in os.walk(root_dir):
    if "requirements_backup.txt" in filenames:
        file_path = os.path.join(dirpath, "requirements_backup.txt")
        try:
            os.remove(file_path)
            print(f"Silindi: {file_path}")
        except Exception as e:
            print(f"HATA: {file_path} silinemedi -> {e}")
