#!/usr/bin/env python3
"""
Менеджер колод таро - утилита для работы с конфигурацией колод
Позволяет легко управлять различными колодами и их настройками
"""

import json
import os
import argparse
from pathlib import Path

class DeckManager:
    def __init__(self, config_path="decks_config.json"):
        """Инициализация менеджера колод"""
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Загрузка конфигурации из файла"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"⚠️  Конфигурационный файл не найден: {self.config_path}")
            return {"decks": {}, "default_settings": {}}
    
    def save_config(self):
        """Сохранение конфигурации в файл"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"✅ Конфигурация сохранена в {self.config_path}")
    
    def list_decks(self):
        """Список всех доступных колод"""
        if not self.config.get('decks'):
            print("Нет зарегистрированных колод")
            return
        
        print("\n📚 Доступные колоды:")
        print("-" * 50)
        for deck_id, deck_info in self.config['decks'].items():
            print(f"ID: {deck_id}")
            print(f"  Название: {deck_info['name']}")
            print(f"  Описание: {deck_info['description']}")
            print(f"  Путь: {deck_info['source_dir']}")
            print(f"  Количество карт: {deck_info['card_count']}")
            print()
    
    def get_deck(self, deck_id):
        """Получение информации о конкретной колоде"""
        return self.config.get('decks', {}).get(deck_id)
    
    def add_deck(self, deck_id, name, source_dir, description="", card_count=78):
        """Добавление новой колоды"""
        if deck_id in self.config.get('decks', {}):
            print(f"⚠️  Колода {deck_id} уже существует")
            return False
        
        # Создаем структуру папок для новой колоды
        base_dir = source_dir
        
        deck_info = {
            "name": name,
            "description": description,
            "source_dir": base_dir,
            "full_size_dir": os.path.join(base_dir, "full"),
            "resized_dirs": {
                "720px": os.path.join(base_dir, "720px"),
                "360px": os.path.join(base_dir, "360px"),
                "thumbs": os.path.join(base_dir, "thumbs")
            },
            "gif_dir": os.path.join(base_dir, "gif"),
            "card_count": card_count,
            "card_format": "jpg",
            "naming_pattern": "*",
            "has_cover": False
        }
        
        if 'decks' not in self.config:
            self.config['decks'] = {}
        
        self.config['decks'][deck_id] = deck_info
        self.save_config()
        
        print(f"✅ Колода '{name}' добавлена с ID: {deck_id}")
        
        # Создаем необходимые папки
        for dir_path in [deck_info['full_size_dir'], deck_info['gif_dir']] + list(deck_info['resized_dirs'].values()):
            os.makedirs(dir_path, exist_ok=True)
            print(f"  📁 Создана папка: {dir_path}")
        
        return True
    
    def remove_deck(self, deck_id):
        """Удаление колоды из конфигурации (не удаляет файлы)"""
        if deck_id not in self.config.get('decks', {}):
            print(f"⚠️  Колода {deck_id} не найдена")
            return False
        
        deck_name = self.config['decks'][deck_id]['name']
        del self.config['decks'][deck_id]
        self.save_config()
        
        print(f"✅ Колода '{deck_name}' удалена из конфигурации")
        print("   (Файлы колоды не были удалены)")
        return True
    
    def update_deck(self, deck_id, **kwargs):
        """Обновление информации о колоде"""
        if deck_id not in self.config.get('decks', {}):
            print(f"⚠️  Колода {deck_id} не найдена")
            return False
        
        for key, value in kwargs.items():
            if key in self.config['decks'][deck_id]:
                self.config['decks'][deck_id][key] = value
        
        self.save_config()
        print(f"✅ Колода {deck_id} обновлена")
        return True
    
    def get_default_settings(self, setting_type=None):
        """Получение настроек по умолчанию"""
        if setting_type:
            return self.config.get('default_settings', {}).get(setting_type)
        return self.config.get('default_settings', {})
    
    def create_processing_script(self, deck_id, operation):
        """Создание скрипта для обработки колоды"""
        deck = self.get_deck(deck_id)
        if not deck:
            print(f"⚠️  Колода {deck_id} не найдена")
            return
        
        scripts = []
        
        if operation == 'resize':
            # Генерируем команды для изменения размера
            for size_name, size_dir in deck['resized_dirs'].items():
                settings = self.get_default_settings('resize')['standard_sizes'].get(size_name, {})
                cmd = f"python scripts/resize_cards.py -s {deck['full_size_dir']} -o {size_dir}"
                
                if settings.get('width'):
                    cmd += f" -w {settings['width']}"
                if settings.get('height'):
                    cmd += f" -H {settings['height']}"
                
                scripts.append(cmd)
        
        elif operation == 'gif':
            # Генерируем команды для создания GIF
            gif_settings = self.get_default_settings('gif')
            
            for gif_type in ['single', 'three', 'celtic', 'telegram']:
                settings = gif_settings.get(gif_type.replace('_', ''), {})
                cmd = f"python scripts/create_tarot_gif.py -s {deck['resized_dirs'].get('720px', deck['full_size_dir'])} -o {deck['gif_dir']} -t {gif_type}"
                
                if gif_type == 'single' and settings:
                    cmd += f" --pool {settings.get('pool_size', 12)} --frames {settings.get('frames', 12)}"
                elif gif_type == 'three' and settings:
                    cmd += f" --pool {settings.get('pool_size', 12)} --frames {settings.get('frames', 12)}"
                
                scripts.append(cmd)
        
        elif operation == 'convert':
            # Команда для конвертации в JPG
            cmd = f"python scripts/convert_to_jpg.py -d {deck['full_size_dir']}"
            scripts.append(cmd)
        
        if scripts:
            print(f"\n📝 Скрипты для обработки колоды '{deck['name']}':")
            print("-" * 50)
            for script in scripts:
                print(script)
            print("-" * 50)
            print("\n💡 Вы можете выполнить эти команды для обработки колоды")
        else:
            print(f"⚠️  Неизвестная операция: {operation}")

def main():
    parser = argparse.ArgumentParser(
        description='Менеджер колод таро',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Показать все колоды
  python deck_manager.py --list
  
  # Добавить новую колоду
  python deck_manager.py --add new_deck --name "Новая колода" --source tarot/new_deck
  
  # Получить информацию о колоде
  python deck_manager.py --info rider-waite
  
  # Создать скрипты для обработки колоды
  python deck_manager.py --deck soimoi --scripts resize
  python deck_manager.py --deck soimoi --scripts gif
  
  # Удалить колоду из конфигурации
  python deck_manager.py --remove old_deck
        """
    )
    
    parser.add_argument('--list', action='store_true',
                        help='Показать список всех колод')
    parser.add_argument('--add', metavar='DECK_ID',
                        help='Добавить новую колоду')
    parser.add_argument('--name',
                        help='Название колоды (для --add)')
    parser.add_argument('--source',
                        help='Путь к папке с колодой (для --add)')
    parser.add_argument('--description',
                        help='Описание колоды (для --add)')
    parser.add_argument('--remove', metavar='DECK_ID',
                        help='Удалить колоду из конфигурации')
    parser.add_argument('--info', metavar='DECK_ID',
                        help='Показать информацию о колоде')
    parser.add_argument('--deck', metavar='DECK_ID',
                        help='ID колоды для операций')
    parser.add_argument('--scripts', choices=['resize', 'gif', 'convert'],
                        help='Создать скрипты для обработки колоды')
    parser.add_argument('--config',
                        default='decks_config.json',
                        help='Путь к файлу конфигурации')
    
    args = parser.parse_args()
    
    # Создаем менеджер колод
    manager = DeckManager(args.config)
    
    # Выполняем операции
    if args.list:
        manager.list_decks()
    
    elif args.add:
        if not args.name or not args.source:
            print("❌ Для добавления колоды требуются --name и --source")
            return
        
        manager.add_deck(
            deck_id=args.add,
            name=args.name,
            source_dir=args.source,
            description=args.description or ""
        )
    
    elif args.remove:
        manager.remove_deck(args.remove)
    
    elif args.info:
        deck = manager.get_deck(args.info)
        if deck:
            print(f"\n📚 Информация о колоде '{args.info}':")
            print("-" * 50)
            for key, value in deck.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for k, v in value.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"{key}: {value}")
        else:
            print(f"❌ Колода {args.info} не найдена")
    
    elif args.deck and args.scripts:
        manager.create_processing_script(args.deck, args.scripts)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()