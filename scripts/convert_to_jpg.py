#!/usr/bin/env python3
"""
Универсальный скрипт для конвертации всех изображений в папке в формат JPG
Поддерживает любые колоды и настраиваемые параметры
"""

import os
import glob
import argparse
from PIL import Image
from pathlib import Path

def convert_to_jpg(directory_path, quality=95, keep_originals=False):
    """
    Конвертирует все изображения в указанной папке в формат JPG
    
    Args:
        directory_path (str): Путь к папке с изображениями
    """
    # Поддерживаемые форматы изображений
    supported_formats = ['*.png', '*.PNG', '*.gif', '*.GIF', '*.bmp', '*.BMP', 
                        '*.tiff', '*.TIFF', '*.tif', '*.TIF', '*.webp', '*.WEBP']
    
    # Счетчики для статистики
    converted_count = 0
    deleted_count = 0
    already_jpg_count = 0
    error_count = 0
    
    # Получаем список всех файлов изображений
    all_image_files = []
    for pattern in supported_formats:
        all_image_files.extend(glob.glob(os.path.join(directory_path, pattern)))
    
    if not all_image_files:
        print(f"Не найдено изображений для конвертации в папке: {directory_path}")
        # Проверяем JPG файлы
        jpg_files = glob.glob(os.path.join(directory_path, "*.jpg")) + \
                   glob.glob(os.path.join(directory_path, "*.JPG")) + \
                   glob.glob(os.path.join(directory_path, "*.jpeg")) + \
                   glob.glob(os.path.join(directory_path, "*.JPEG"))
        if jpg_files:
            print(f"В папке уже есть {len(jpg_files)} JPG файлов")
        return
    
    print(f"Найдено {len(all_image_files)} файлов для конвертации")
    print("-" * 50)
    
    for image_path in all_image_files:
        try:
            # Получаем имя файла без расширения
            file_name = Path(image_path).stem
            output_path = os.path.join(directory_path, f"{file_name}.jpg")
            
            # Проверяем, существует ли уже JPG версия
            if os.path.exists(output_path):
                print(f"⚠️  JPG версия уже существует: {file_name}.jpg")
                # Удаляем исходный файл если не указано сохранять оригиналы
                if not keep_originals:
                    os.remove(image_path)
                    print(f"   Удален исходный файл: {os.path.basename(image_path)}")
                    deleted_count += 1
                continue
            
            # Открываем изображение
            with Image.open(image_path) as img:
                # Конвертируем в RGB если изображение в другом режиме (RGBA, P, и т.д.)
                if img.mode not in ('RGB', 'L'):
                    # Если есть альфа-канал, создаем белый фон
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        # Создаем белый фон
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        # Накладываем изображение на белый фон
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    else:
                        img = img.convert('RGB')
                
                # Сохраняем как JPG с указанным качеством
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                print(f"✅ Конвертировано: {os.path.basename(image_path)} → {file_name}.jpg")
                converted_count += 1
                
                # Удаляем исходный файл если не указано сохранять оригиналы
                if not keep_originals:
                    os.remove(image_path)
                    print(f"   Удален исходный файл: {os.path.basename(image_path)}")
                    deleted_count += 1
                
        except Exception as e:
            print(f"❌ Ошибка при обработке {os.path.basename(image_path)}: {e}")
            error_count += 1
    
    # Подсчитываем существующие JPG файлы
    jpg_files = glob.glob(os.path.join(directory_path, "*.jpg")) + \
               glob.glob(os.path.join(directory_path, "*.JPG"))
    already_jpg_count = len(jpg_files) - converted_count
    
    # Выводим статистику
    print("\n" + "=" * 50)
    print("СТАТИСТИКА:")
    print(f"✅ Конвертировано файлов: {converted_count}")
    if not keep_originals and deleted_count > 0:
        print(f"🗑️  Удалено исходных файлов: {deleted_count}")
    if already_jpg_count > 0:
        print(f"📁 Уже были в JPG формате: {already_jpg_count}")
    if error_count > 0:
        print(f"❌ Ошибок при конвертации: {error_count}")
    print(f"📊 Всего JPG файлов в папке: {len(jpg_files)}")
    print("=" * 50)

def main():
    """Основная функция с поддержкой аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Конвертация всех изображений в JPG формат',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Конвертировать все изображения в папке soimoi
  python convert_to_jpg.py --dir tarot/soimoi/full
  
  # Конвертировать с указанием качества
  python convert_to_jpg.py -d tarot/new_deck/images --quality 90
  
  # Конвертировать без удаления оригиналов
  python convert_to_jpg.py -d tarot/backup --keep-originals
        """
    )
    
    parser.add_argument('-d', '--dir', '--directory', 
                        default="tarot/soimoi/full",
                        help='Папка с изображениями для конвертации (по умолчанию: tarot/soimoi/full)')
    parser.add_argument('-q', '--quality', type=int, default=95,
                        help='Качество JPG (1-100, по умолчанию: 95)')
    parser.add_argument('--keep-originals', action='store_true',
                        help='Сохранить оригинальные файлы (не удалять после конвертации)')
    
    args = parser.parse_args()
    
    # Проверяем существование папки
    if not os.path.exists(args.dir):
        print(f"❌ Папка не найдена: {args.dir}")
        return
    
    print(f"🎯 Начинаем конвертацию файлов в папке: {args.dir}")
    print(f"📊 Качество JPG: {args.quality}%")
    if args.keep_originals:
        print("📁 Оригинальные файлы будут сохранены")
    print("=" * 50)
    
    # Выполняем конвертацию
    convert_to_jpg(args.dir, args.quality, args.keep_originals)
    
    print("\n✨ Обработка завершена!")

if __name__ == "__main__":
    main()