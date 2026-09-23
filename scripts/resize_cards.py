#!/usr/bin/env python3
"""
Универсальный скрипт для изменения размера карт таро
Поддерживает любые колоды и настраиваемые размеры
"""

import os
import argparse
from PIL import Image
from pathlib import Path
import glob

def resize_cards(source_dir, output_dir, target_width=None, target_height=None, 
                 quality=95, preserve_aspect=True):
    """
    Изменяет размер всех изображений в указанной папке
    
    Args:
        source_dir (str): Исходная папка с картами
        output_dir (str): Папка для сохранения измененных карт
        target_width (int): Целевая ширина
        target_height (int): Целевая высота
        quality (int): Качество JPEG (1-100)
        preserve_aspect (bool): Сохранять соотношение сторон
    """
    # Создаем выходную директорию если не существует
    os.makedirs(output_dir, exist_ok=True)
    
    # Поддерживаемые форматы
    supported_formats = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    
    # Собираем все файлы изображений
    image_files = []
    for pattern in supported_formats:
        image_files.extend(glob.glob(os.path.join(source_dir, pattern)))
    
    if not image_files:
        print(f"❌ Не найдено изображений в папке: {source_dir}")
        return
    
    print(f"📁 Найдено {len(image_files)} изображений для обработки")
    print(f"📏 Целевой размер: {target_width or 'авто'}x{target_height or 'авто'}")
    print("-" * 50)
    
    processed = 0
    errors = 0
    
    for image_path in image_files:
        try:
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_dir, filename)
            
            # Открываем изображение
            with Image.open(image_path) as img:
                original_width, original_height = img.size
                
                # Вычисляем новые размеры
                if preserve_aspect:
                    # Если указан только один размер, вычисляем второй
                    if target_width and not target_height:
                        aspect_ratio = original_height / original_width
                        new_width = target_width
                        new_height = int(target_width * aspect_ratio)
                    elif target_height and not target_width:
                        aspect_ratio = original_width / original_height
                        new_width = int(target_height * aspect_ratio)
                        new_height = target_height
                    elif target_width and target_height:
                        # Масштабируем чтобы вписать в заданные размеры
                        aspect_ratio = original_width / original_height
                        target_aspect = target_width / target_height
                        
                        if aspect_ratio > target_aspect:
                            new_width = target_width
                            new_height = int(target_width / aspect_ratio)
                        else:
                            new_height = target_height
                            new_width = int(target_height * aspect_ratio)
                    else:
                        # Если размеры не указаны, сохраняем оригинальные
                        new_width = original_width
                        new_height = original_height
                else:
                    # Без сохранения пропорций
                    new_width = target_width or original_width
                    new_height = target_height or original_height
                
                # Изменяем размер
                resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Конвертируем в RGB если нужно (для JPEG)
                if resized.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', resized.size, (255, 255, 255))
                    if resized.mode == 'RGBA':
                        rgb_img.paste(resized, mask=resized.split()[-1])
                    else:
                        rgb_img.paste(resized)
                    resized = rgb_img
                
                # Сохраняем с указанным качеством
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    resized.save(output_path, 'JPEG', quality=quality, optimize=True)
                else:
                    resized.save(output_path)
                
                print(f"✅ {filename}: {original_width}x{original_height} → {new_width}x{new_height}")
                processed += 1
                
        except Exception as e:
            print(f"❌ Ошибка при обработке {filename}: {e}")
            errors += 1
    
    # Статистика
    print("\n" + "=" * 50)
    print("📊 СТАТИСТИКА:")
    print(f"✅ Обработано: {processed} файлов")
    if errors > 0:
        print(f"❌ Ошибок: {errors}")
    print(f"📁 Результаты сохранены в: {output_dir}")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description='Изменение размера карт таро с сохранением пропорций',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Изменить размер всех карт Rider-Waite до ширины 720px
  python resize_cards.py --source tarot/rider-waite/full --output tarot/rider-waite/720px --width 720
  
  # Изменить размер карт Soimoi до 400x600 без сохранения пропорций
  python resize_cards.py -s tarot/soimoi/full -o tarot/soimoi/resized -w 400 -H 600 --no-preserve-aspect
  
  # Создать миниатюры высотой 200px с качеством 85%
  python resize_cards.py -s tarot/rider-waite/full -o tarot/rider-waite/thumbs --height 200 -q 85
        """
    )
    
    parser.add_argument('-s', '--source', required=True,
                        help='Исходная папка с картами')
    parser.add_argument('-o', '--output', required=True,
                        help='Папка для сохранения результатов')
    parser.add_argument('-w', '--width', type=int,
                        help='Целевая ширина в пикселях')
    parser.add_argument('-H', '--height', type=int,
                        help='Целевая высота в пикселях')
    parser.add_argument('-q', '--quality', type=int, default=95,
                        help='Качество JPEG (1-100, по умолчанию: 95)')
    parser.add_argument('--no-preserve-aspect', action='store_true',
                        help='Не сохранять соотношение сторон')
    
    args = parser.parse_args()
    
    # Проверка аргументов
    if not os.path.exists(args.source):
        print(f"❌ Исходная папка не найдена: {args.source}")
        return
    
    if not args.width and not args.height:
        print("⚠️  Не указаны целевые размеры. Используйте --width и/или --height")
        return
    
    # Запуск обработки
    resize_cards(
        source_dir=args.source,
        output_dir=args.output,
        target_width=args.width,
        target_height=args.height,
        quality=args.quality,
        preserve_aspect=not args.no_preserve_aspect
    )

if __name__ == "__main__":
    main()