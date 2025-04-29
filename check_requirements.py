import subprocess
import configparser
import os


# git-config.ini dosyasını oku
def get_config():
    config = configparser.ConfigParser()
    config.read('git-config.ini')
    return config['settings']['auto_update'].lower() == 'true'


# Yüklü paketleri pip freeze ile al
def get_installed_packages():
    return subprocess.check_output(["pip", "freeze"]).decode("utf-8").splitlines()


def main():
    # git-config.ini dosyasındaki auto_update ayarını al
    auto_update = get_config()

    # Yüklü paketleri al
    installed_packages = get_installed_packages()

    # requirements.txt dosyasını oku
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            pass

    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()

    # Yüklü paketlerle requirements.txt'deki paketleri karşılaştır
    missing_packages = [pkg for pkg in installed_packages if pkg not in required_packages]

    if missing_packages:
        print(f"Yeni kütüphaneler bulundu: {missing_packages}")

        # Eğer auto_update True ise, requirements.txt dosyasını otomatik güncelle
        if auto_update:
            with open('requirements.txt', 'a') as f:
                for pkg in missing_packages:
                    f.write(pkg + '\n')
            print("requirements.txt otomatik olarak güncellendi.")
        else:
            # Eğer auto_update False ise, kullanıcıya güncellemesi için mesaj göster
            print("requirements.txt dosyasını güncellemek için 'pip freeze > requirements.txt' komutunu çalıştırabilirsiniz.")
    else:
        print("requirements.txt zaten güncel.")


if __name__ == "__main__":
    # main()
    ...