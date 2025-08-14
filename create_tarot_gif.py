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

def create_telegram_optimized_gif(cards_dir, output_path, num_cards_pool=12, num_frames=10, duration=100, loop=0):
    """
    Создает GIF оптимизированный для Telegram (меньше размер, быстрее анимация)
    Telegram лучше распознает GIF с определенными параметрами
    """
    # Получаем все доступные карты
    card_files = glob.glob(os.path.join(cards_dir, "*.jpg"))
    
    # Исключаем обложки из выборки
    card_files = [f for f in card_files if 'Cover' not in os.path.basename(f)]
    
    if len(card_files) < num_cards_pool:
        print(f"Недостаточно карт: найдено {len(card_files)}, требуется {num_cards_pool}")
        return
    
    # Выбираем пул карт для использования
    card_pool = random.sample(card_files, num_cards_pool)
    
    # Параметры композиции - оптимизированы для Telegram
    frame_width = 256  # Кратно 16 для лучшего сжатия
    frame_height = 144  # Кратно 16 для лучшего сжатия
    card_height = 128  # Меньший размер для экономии места
    card_width = int(card_height * 0.6)  # Соотношение сторон карт 0.6
    padding_top = (frame_height - card_height) // 2  # Центрируем по вертикали
    
    # Рассчитываем горизонтальные отступы
    total_cards_width = card_width * 3
    remaining_width = frame_width - total_cards_width
    padding_between = remaining_width // 4  # 4 промежутка: слева, между картами (2), справа
    
    frames = []
    
    for frame_num in range(num_frames):
        # Создаем пустой кадр с темным фоном
        frame = Image.new('RGB', (frame_width, frame_height), color=(20, 20, 20))
        
        # Случайно выбираем 3 карты из пула
        selected_cards = random.sample(card_pool, 3)
        
        # Размещаем карты на кадре
        for i, card_file in enumerate(selected_cards):
            try:
                # Загружаем и изменяем размер карты
                card = Image.open(card_file)
                card = card.resize((card_width, card_height), Image.Resampling.LANCZOS)
                
                # Вычисляем позицию карты
                x_position = padding_between + i * (card_width + padding_between)
                y_position = padding_top
                
                # Вставляем карту в кадр
                frame.paste(card, (x_position, y_position))
                
            except Exception as e:
                print(f"Ошибка при обработке карты {card_file}: {e}")
        
        # Конвертируем в палитру с меньшим количеством цветов для Telegram
        frame = frame.convert('P', palette=Image.Palette.ADAPTIVE, colors=64)
        frames.append(frame)
    
    # Сохраняем GIF с параметрами оптимизированными для Telegram
    try:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,  # Быстрая анимация для Telegram
            loop=loop,
            optimize=True,
            disposal=2  # Важно для правильного отображения в Telegram
        )
        print(f"GIF для Telegram создан: {output_path}")
        print(f"Параметры: {num_frames} кадров, пул из {num_cards_pool} карт")
        print(f"Размер кадра: {frame_width}x{frame_height}")
        print(f"Размер карт: {card_width}x{card_height}")
        print(f"Длительность кадра: {duration}ms")
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Размер файла: {file_size:.2f} МБ")
        
        if file_size < 8:
            print("✓ Файл подходит для отправки как GIF в Telegram")
        else:
            print("⚠ Файл слишком большой для GIF в Telegram")
    except Exception as e:
        print(f"Ошибка при создании GIF: {e}")

def create_three_cards_gif(cards_dir, output_path, num_cards_pool=36, num_frames=30, duration=200, loop=0):
    """
    Создает GIF с 3 картами на каждом кадре, случайно выбирая из пула карт
    
    Args:
        cards_dir (str): Путь к папке с картами
        output_path (str): Путь для сохранения GIF
        num_cards_pool (int): Размер пула карт для случайного выбора
        num_frames (int): Количество кадров в GIF
        duration (int): Длительность каждого кадра в миллисекундах
        loop (int): Количество повторений (0 = бесконечно)
    """
    # Получаем все доступные карты
    card_files = glob.glob(os.path.join(cards_dir, "*.jpg"))
    
    # Исключаем обложки из выборки
    card_files = [f for f in card_files if 'Cover' not in os.path.basename(f)]
    
    if len(card_files) < num_cards_pool:
        print(f"Недостаточно карт: найдено {len(card_files)}, требуется {num_cards_pool}")
        return
    
    # Выбираем пул карт для использования
    card_pool = random.sample(card_files, num_cards_pool)
    
    # Параметры композиции
    frame_width = 320
    frame_height = 180
    card_height = 160  # Высота карты с учетом отступов
    card_width = int(card_height * 0.6)  # Соотношение сторон карт 0.6
    padding_top = (frame_height - card_height) // 2  # Центрируем по вертикали
    
    # Рассчитываем горизонтальные отступы
    total_cards_width = card_width * 3
    remaining_width = frame_width - total_cards_width
    padding_between = remaining_width // 4  # 4 промежутка: слева, между картами (2), справа
    
    frames = []
    
    for frame_num in range(num_frames):
        # Создаем пустой кадр с темным фоном
        frame = Image.new('RGB', (frame_width, frame_height), color=(20, 20, 20))
        
        # Случайно выбираем 3 карты из пула
        selected_cards = random.sample(card_pool, 3)
        
        # Размещаем карты на кадре
        for i, card_file in enumerate(selected_cards):
            try:
                # Загружаем и изменяем размер карты
                card = Image.open(card_file)
                card = card.resize((card_width, card_height), Image.Resampling.LANCZOS)
                
                # Вычисляем позицию карты
                x_position = padding_between + i * (card_width + padding_between)
                y_position = padding_top
                
                # Вставляем карту в кадр
                frame.paste(card, (x_position, y_position))
                
            except Exception as e:
                print(f"Ошибка при обработке карты {card_file}: {e}")
        
        # Конвертируем в палитру для оптимизации размера
        frame = frame.convert('P', palette=Image.Palette.ADAPTIVE, colors=128)
        frames.append(frame)
        
        if frame_num % 5 == 0:  # Показываем прогресс каждые 5 кадров
            print(f"Создан кадр {frame_num + 1}/{num_frames}")
    
    # Сохраняем GIF
    try:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
            optimize=True
        )
        print(f"GIF успешно создан: {output_path}")
        print(f"Параметры: {num_frames} кадров, пул из {num_cards_pool} карт")
        print(f"Размер кадра: {frame_width}x{frame_height}")
        print(f"Размер карт: {card_width}x{card_height}")
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)
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
    cards_directory = os.path.join(base_dir, "720px")  # Используем правильную папку с картами
    gif_directory = os.path.join(base_dir, "gif")
    os.makedirs(gif_directory, exist_ok=True)
    
    # Создаем GIF оптимизированный для Telegram
    create_telegram_optimized_gif(
        cards_dir=cards_directory,
        output_path=os.path.join(gif_directory, "telegram_tarot.gif"),
        num_cards_pool=12,
        num_frames=10,  # Меньше кадров для Telegram
        duration=100,  # Быстрая анимация (100ms на кадр)
        loop=0
    ) 