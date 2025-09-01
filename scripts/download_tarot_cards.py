import requests
import os
import time

# Сопоставление ваших имён файлов с кодами на сайте
card_url_map = {
    # Старшие арканы
    "00_Fool.jpg": "RWSa-T-00.png",
    "01_Magician.jpg": "RWSa-T-01.png",
    "02_High_Priestess.jpg": "RWSa-T-02.png",
    "03_Empress.jpg": "RWSa-T-03.png",
    "04_Emperor.jpg": "RWSa-T-04.png",
    "05_Hierophant.jpg": "RWSa-T-05.png",
    "06_Lovers.jpg": "RWSa-T-06.png",
    "07_Chariot.jpg": "RWSa-T-07.png",
    "08_Strength.jpg": "RWSa-T-08.png",
    "09_Hermit.jpg": "RWSa-T-09.png",
    "10_Wheel_of_Fortune.jpg": "RWSa-T-10.png",
    "11_Justice.jpg": "RWSa-T-11.png",
    "12_Hanged_Man.jpg": "RWSa-T-12.png",
    "13_Death.jpg": "RWSa-T-13.png",
    "14_Temperance.jpg": "RWSa-T-14.png",
    "15_Devil.jpg": "RWSa-T-15.png",
    "16_Tower.jpg": "RWSa-T-16.png",
    "17_Star.jpg": "RWSa-T-17.png",
    "18_Moon.jpg": "RWSa-T-18.png",
    "19_Sun.jpg": "RWSa-T-19.png",
    "20_Judgement.jpg": "RWSa-T-20.png",
    "21_World.jpg": "RWSa-T-21.png",
    # Кубки (Cups) - исправленные коды
    "Cups01.jpg": "RWSa-C-0A.png",  # Ace 0A
    "Cups02.jpg": "RWSa-C-02.png",
    "Cups03.jpg": "RWSa-C-03.png",
    "Cups04.jpg": "RWSa-C-04.png",
    "Cups05.jpg": "RWSa-C-05.png",
    "Cups06.jpg": "RWSa-C-06.png",
    "Cups07.jpg": "RWSa-C-07.png",
    "Cups08.jpg": "RWSa-C-08.png",
    "Cups09.jpg": "RWSa-C-09.png",
    "Cups10.jpg": "RWSa-C-10.png",
    "Cups11.jpg": "RWSa-C-J1.png",  # Page = J1
    "Cups12.jpg": "RWSa-C-J2.png",  # Knight = J2
    "Cups13.jpg": "RWSa-C-QU.png",  # Queen
    "Cups14.jpg": "RWSa-C-KI.png",  # King
    # Пентакли (Pents) - исправленные коды
    "Pents01.jpg": "RWSa-P-0A.png",  # Ace 0A
    "Pents02.jpg": "RWSa-P-02.png",
    "Pents03.jpg": "RWSa-P-03.png",
    "Pents04.jpg": "RWSa-P-04.png",
    "Pents05.jpg": "RWSa-P-05.png",
    "Pents06.jpg": "RWSa-P-06.png",
    "Pents07.jpg": "RWSa-P-07.png",
    "Pents08.jpg": "RWSa-P-08.png",
    "Pents09.jpg": "RWSa-P-09.png",
    "Pents10.jpg": "RWSa-P-10.png",
    "Pents11.jpg": "RWSa-P-J1.png",  # Page = J1
    "Pents12.jpg": "RWSa-P-J2.png",  # Knight = J2
    "Pents13.jpg": "RWSa-P-QU.png",  # Queen
    "Pents14.jpg": "RWSa-P-KI.png",  # King
    # Мечи (Swords) - исправленные коды
    "Swords01.jpg": "RWSa-S-0A.png",  # Ace 0A
    "Swords02.jpg": "RWSa-S-02.png",
    "Swords03.jpg": "RWSa-S-03.png",
    "Swords04.jpg": "RWSa-S-04.png",
    "Swords05.jpg": "RWSa-S-05.png",
    "Swords06.jpg": "RWSa-S-06.png",
    "Swords07.jpg": "RWSa-S-07.png",
    "Swords08.jpg": "RWSa-S-08.png",
    "Swords09.jpg": "RWSa-S-09.png",
    "Swords10.jpg": "RWSa-S-10.png",
    "Swords11.jpg": "RWSa-S-J1.png",  # Page = J1
    "Swords12.jpg": "RWSa-S-J2.png",  # Knight = J2
    "Swords13.jpg": "RWSa-S-QU.png",  # Queen
    "Swords14.jpg": "RWSa-S-KI.png",  # King
    # Жезлы (Wands) - исправленные коды
    "Wands01.jpg": "RWSa-W-0A.png",  # Ace 0A
    "Wands02.jpg": "RWSa-W-02.png",
    "Wands03.jpg": "RWSa-W-03.png",
    "Wands04.jpg": "RWSa-W-04.png",
    "Wands05.jpg": "RWSa-W-05.png",
    "Wands06.jpg": "RWSa-W-06.png",
    "Wands07.jpg": "RWSa-W-07.png",
    "Wands08.jpg": "RWSa-W-08.png",
    "Wands09.jpg": "RWSa-W-09.png",
    "Wands10.jpg": "RWSa-W-10.png",
    "Wands11.jpg": "RWSa-W-J1.png",  # Page = J1
    "Wands12.jpg": "RWSa-W-J2.png",  # Knight = J2
    "Wands13.jpg": "RWSa-W-QU.png",  # Queen
    "Wands14.jpg": "RWSa-W-KI.png",  # King
    # Рубашки карт
    "Cover.jpg": "RWSa-X-BA.png",  # Обычная рубашка
    "Cover_Rare.jpg": "RWSa-X-RL.png",  # Редкая рубашка
}

# Альтернативные варианты для рубашки
back_alternatives = [
    "RWSa-back.png",
    "RWSa-cardback.png",
    "RWSa-T-back.png",
    "back.png",
    "cardback.png",
    "RWSa-back.jpg",
    "RWSa-cardback.jpg"
]

# Альтернативные коды для недостающих карт
missing_cards_alternatives = {
    "Cups01.jpg": ["RWSa-C-00.png", "RWSa-C-A.png"],
    "Pents01.jpg": ["RWSa-P-00.png", "RWSa-P-A.png"],
    "Swords01.jpg": ["RWSa-S-00.png", "RWSa-S-A.png"],
    "Wands01.jpg": ["RWSa-W-00.png", "RWSa-W-A.png"],
    "Cups13.jpg": ["RWSa-C-Q.png", "RWSa-C-J3.png"],
    "Cups14.jpg": ["RWSa-C-K.png", "RWSa-C-J4.png"],
    "Pents13.jpg": ["RWSa-P-Q.png", "RWSa-P-J3.png"],
    "Pents14.jpg": ["RWSa-P-K.png", "RWSa-P-J4.png"],
    "Swords13.jpg": ["RWSa-S-Q.png", "RWSa-S-J3.png"],
    "Swords14.jpg": ["RWSa-S-K.png", "RWSa-S-J4.png"],
    "Wands13.jpg": ["RWSa-W-Q.png", "RWSa-W-J3.png"],
    "Wands14.jpg": ["RWSa-W-K.png", "RWSa-W-J4.png"],
}

base_url = "https://steve-p.org/cards/pix/"
download_dir = "tarot/rider-waite/full"
os.makedirs(download_dir, exist_ok=True)

def download_all():
    for local_name, remote_name in card_url_map.items():
        url = base_url + remote_name
        out_path = os.path.join(download_dir, local_name)
        
        # Пропускаем уже скачанные файлы
        if os.path.exists(out_path):
            print(f"Пропускаю {local_name} (уже существует)")
            continue
            
        try:
            print(f"Скачиваю {url} → {local_name} ...", end=" ")
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(resp.content)
                print("OK")
            else:
                print(f"НЕ НАЙДЕНО (status {resp.status_code})")
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(0.2)
    
    # Пробуем альтернативные варианты для недостающих карт
    print("\nПробуем альтернативные варианты для недостающих карт:")
    for local_name, alternatives in missing_cards_alternatives.items():
        out_path = os.path.join(download_dir, local_name)
        if os.path.exists(out_path):
            print(f"Пропускаю {local_name} (уже существует)")
            continue
            
        for alt in alternatives:
            url = base_url + alt
            try:
                print(f"Пробуем {url} → {local_name} ...", end=" ")
                resp = requests.get(url, timeout=30)
                if resp.status_code == 200:
                    with open(out_path, "wb") as f:
                        f.write(resp.content)
                    print("OK")
                    break
                else:
                    print(f"НЕ НАЙДЕНО (status {resp.status_code})")
            except Exception as e:
                print(f"Ошибка: {e}")
            time.sleep(0.2)
    
    # Пробуем альтернативные варианты для рубашки
    print("\nПробуем альтернативные варианты для рубашки:")
    for alt in back_alternatives:
        url = base_url + alt
        out_path = os.path.join(download_dir, "Cover.jpg")
        try:
            print(f"Пробуем {url} ...", end=" ")
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(resp.content)
                print("OK - рубашка найдена!")
                break
            else:
                print(f"НЕ НАЙДЕНО (status {resp.status_code})")
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(0.2)

if __name__ == "__main__":
    download_all() 