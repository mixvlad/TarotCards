import os
import json
from PIL import Image
import glob
import re
import random

def get_card_order(card_filename):
    """
    Определяет порядок карты для правильной сортировки
    Возвращает кортеж (тип_карты, номер) для сортировки
    """
    filename = os.path.basename(card_filename).lower()
    
    # Старшие арканы (0-21)
    major_match = re.search(r'rws_tarot_(\d{2})_', filename)
    if major_match:
        number = int(major_match.group(1))
        return (0, number)  # 0 = старшие арканы
    
    # Младшие арканы
    # Жезлы (Wands)
    if 'wands' in filename:
        match = re.search(r'wands(\d{2})', filename)
        if match:
            number = int(match.group(1))
            return (1, number)  # 1 = жезлы
    
    # Кубки (Cups)
    if 'cups' in filename:
        match = re.search(r'cups(\d{2})', filename)
        if match:
            number = int(match.group(1))
            return (2, number)  # 2 = кубки
    
    # Мечи (Swords)
    if 'swords' in filename:
        match = re.search(r'swords(\d{2})', filename)
        if match:
            number = int(match.group(1))
            return (3, number)  # 3 = мечи
    
    # Пентакли (Pentacles/Pents)
    if 'pents' in filename or 'pentacles' in filename:
        match = re.search(r'pents(\d{2})', filename)
        if match:
            number = int(match.group(1))
            return (4, number)  # 4 = пентакли
    
    # Если не удалось определить порядок, возвращаем высокий номер
    return (999, 999)

def create_tarot_gif(cards_dir, output_path, duration=500, loop=0, resize_width=400, resize_height=600):
    """
    Создает GIF анимацию из всех карт Таро
    
    Args:
        cards_dir (str): Путь к папке с картами
        output_path (str): Путь для сохранения GIF
        duration (int): Длительность каждого кадра в миллисекундах
        loop (int): Количество повторений (0 = бесконечно)
        resize_width (int): Ширина изображений в пикселях
        resize_height (int): Высота изображений в пикселях
    """
    
    # Получаем список всех JPG файлов карт
    card_files = glob.glob(os.path.join(cards_dir, "*.jpg"))
    
    if not card_files:
        print(f"Не найдено карт в папке: {cards_dir}")
        return
    
    # Сортируем файлы по правильному порядку карт
    card_files.sort(key=get_card_order)
    
    print(f"Найдено {len(card_files)} карт")
    print("Порядок карт:")
    for i, card_file in enumerate(card_files[:10]):  # Показываем первые 10
        print(f"  {i+1}. {os.path.basename(card_file)}")
    if len(card_files) > 10:
        print(f"  ... и еще {len(card_files) - 10} карт")
    
    # Загружаем изображения
    images = []
    for card_file in card_files:
        try:
            img = Image.open(card_file)
            # Приводим к одинаковому размеру для лучшего результата
            img = img.resize((resize_width, resize_height), Image.Resampling.LANCZOS)
            # Преобразуем к палитре с 32 цветами
            img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=32)
            images.append(img)
            print(f"Загружена карта: {os.path.basename(card_file)}")
        except Exception as e:
            print(f"Ошибка при загрузке {card_file}: {e}")
    
    if not images:
        print("Не удалось загрузить ни одной карты")
        return
    
    # Создаем GIF
    try:
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=loop,
            optimize=True,
            quality=60  # Еще больше уменьшаем качество для меньшего размера
        )
        print(f"GIF успешно создан: {output_path}")
        print(f"Размер: {len(images)} кадров")
        print(f"Длительность кадра: {duration}ms")
        print(f"Размер изображений: {resize_width}x{resize_height}")
        
        # Показываем размер файла
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # в МБ
        print(f"Размер файла: {file_size:.1f} МБ")
    except Exception as e:
        print(f"Ошибка при создании GIF: {e}")

def create_filtered_gif(cards_dir, output_path, filter_func=None, duration=500, loop=0):
    """
    Создает GIF с фильтрацией карт
    
    Args:
        cards_dir (str): Путь к папке с картами
        output_path (str): Путь для сохранения GIF
        filter_func (function): Функция фильтрации, принимает имя файла и возвращает bool
        duration (int): Длительность каждого кадра в миллисекундах
        loop (int): Количество повторений (0 = бесконечно)
    """
    
    # Получаем список всех JPG файлов карт
    card_files = glob.glob(os.path.join(cards_dir, "*.jpg"))
    
    if not card_files:
        print(f"Не найдено карт в папке: {cards_dir}")
        return
    
    # Применяем фильтр если указан
    if filter_func:
        card_files = [f for f in card_files if filter_func(os.path.basename(f))]
    
    # Сортируем файлы по правильному порядку карт
    card_files.sort(key=get_card_order)
    
    print(f"Найдено {len(card_files)} карт после фильтрации")
    
    # Загружаем изображения
    images = []
    for card_file in card_files:
        try:
            img = Image.open(card_file)
            img = img.resize((400, 600), Image.Resampling.LANCZOS)
            img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=32)
            images.append(img)
            print(f"Загружена карта: {os.path.basename(card_file)}")
        except Exception as e:
            print(f"Ошибка при загрузке {card_file}: {e}")
    
    if not images:
        print("Не удалось загрузить ни одной карты")
        return
    
    # Создаем GIF
    try:
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=loop,
            optimize=True,
            quality=60  # Уменьшаем качество для меньшего размера
        )
        print(f"GIF успешно создан: {output_path}")
        print(f"Размер: {len(images)} кадров")
        
        # Показываем размер файла
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # в МБ
        print(f"Размер файла: {file_size:.1f} МБ")
    except Exception as e:
        print(f"Ошибка при создании GIF: {e}")

def create_random_gif(cards_dir, output_path, num_cards=24, duration=83, loop=0, resize_width=200, resize_height=300):
    """
    Создает GIF из случайных карт в случайном порядке
    """
    card_files = glob.glob(os.path.join(cards_dir, "*.jpg"))
    if len(card_files) < num_cards:
        print(f"Недостаточно карт для выбора: найдено {len(card_files)}, требуется {num_cards}")
        return
    selected_files = random.sample(card_files, num_cards)
    random.shuffle(selected_files)
    images = []
    for card_file in selected_files:
        try:
            img = Image.open(card_file)
            img = img.resize((resize_width, resize_height), Image.Resampling.LANCZOS)
            img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=32)
            images.append(img)
            print(f"Добавлена карта: {os.path.basename(card_file)}")
        except Exception as e:
            print(f"Ошибка при загрузке {card_file}: {e}")
    if not images:
        print("Не удалось загрузить ни одной карты")
        return
    try:
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=loop,
            optimize=True,
            quality=60
        )
        print(f"GIF из случайных карт создан: {output_path}")
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Размер файла: {file_size:.1f} МБ")
    except Exception as e:
        print(f"Ошибка при создании GIF: {e}")

if __name__ == "__main__":
    # Пути к файлам
    base_dir = "tarot/rider-waite"
    cards_directory = os.path.join(base_dir, "cards")
    gif_directory = os.path.join(base_dir, "gif")
    os.makedirs(gif_directory, exist_ok=True)
    
    # Создаем GIF со всеми доступными картами
    create_tarot_gif(
        cards_dir=cards_directory,
        output_path=os.path.join(gif_directory, "all_tarot_cards_optimized.gif"),
        duration=83,  # ~83ms на карту (12 карт в секунду)
        loop=0,  # Бесконечный цикл
        resize_width=200,  # Еще больше уменьшаем размер
        resize_height=300
    )
    
    # Пример создания GIF только со старшими арканами (более гибкий способ)
    def is_major_arcana(filename):
        return 'rws_tarot_' in filename.lower()
    
    create_filtered_gif(
        cards_dir=cards_directory,
        output_path=os.path.join(gif_directory, "major_arcana_optimized.gif"),
        filter_func=is_major_arcana,
        duration=83  # 12 карт в секунду
    )
    
    # Пример создания GIF только с младшими арканами
    def is_minor_arcana(filename):
        return any(suit in filename.lower() for suit in ['wands', 'cups', 'swords', 'pents'])
    
    create_filtered_gif(
        cards_dir=cards_directory,
        output_path=os.path.join(gif_directory, "minor_arcana_optimized.gif"),
        filter_func=is_minor_arcana,
        duration=83  # 12 карт в секунду
    ) 
    # Случайные 24 карты в случайном порядке
    create_random_gif(
        cards_dir=cards_directory,
        output_path=os.path.join(gif_directory, "random_24_cards.gif"),
        num_cards=24,
        duration=83,
        loop=0,
        resize_width=200,
        resize_height=300
    ) 