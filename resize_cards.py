import os
from PIL import Image
import glob

def resize_cards():
    """
    Сжимает все изображения карт до 720px в ширину с оптимальным качеством
    """
    source_dir = "tarot/rider-waite/full"
    target_dir = "tarot/rider-waite/720px"
    
    # Создаем папку если её нет
    os.makedirs(target_dir, exist_ok=True)
    
    # Получаем список всех изображений
    image_files = glob.glob(os.path.join(source_dir, "*.jpg")) + glob.glob(os.path.join(source_dir, "*.png"))
    
    print(f"Найдено {len(image_files)} изображений для обработки")
    
    for image_path in image_files:
        filename = os.path.basename(image_path)
        output_path = os.path.join(target_dir, filename)
        
        try:
            # Открываем изображение
            with Image.open(image_path) as img:
                # Получаем размеры
                width, height = img.size
                
                # Вычисляем новую высоту для ширины 720px
                new_width = 720
                new_height = int((height * new_width) / width)
                
                # Изменяем размер с высоким качеством
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Сохраняем с оптимальным качеством
                if filename.lower().endswith('.jpg'):
                    resized_img.save(output_path, 'JPEG', quality=85, optimize=True)
                elif filename.lower().endswith('.png'):
                    resized_img.save(output_path, 'PNG', optimize=True)
                
                print(f"✓ {filename}: {width}x{height} → {new_width}x{new_height}")
                
        except Exception as e:
            print(f"✗ Ошибка при обработке {filename}: {e}")
    
    print(f"\nОбработка завершена! Изображения сохранены в {target_dir}")

if __name__ == "__main__":
    resize_cards() 