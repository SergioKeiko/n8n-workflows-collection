#!/usr/bin/env python3
"""
Очищает API токены и секреты из всех workflows
"""

import os
import json
import re
from pathlib import Path

def clean_secrets_in_json(file_path):
    """Очищает секреты в JSON файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Паттерны для поиска API токенов
        secret_patterns = [
            r'apify_api_[a-zA-Z0-9]+',
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI
            r'xapp-[a-zA-Z0-9]+',   # X/Twitter
            r'AAAA[a-zA-Z0-9_%]+',  # Twitter Bearer
            r'ghp_[a-zA-Z0-9]{36}', # GitHub
            r'[a-zA-Z0-9]{32,}',    # Generic long tokens
        ]
        
        data_str = json.dumps(data)
        original_str = data_str
        changes_made = False
        
        # Заменяем найденные токены
        for pattern in secret_patterns:
            matches = re.findall(pattern, data_str)
            for match in matches:
                if len(match) > 16:  # Только длинные строки
                    data_str = data_str.replace(match, "YOUR_API_TOKEN_HERE")
                    changes_made = True
        
        if changes_made:
            # Парсим обновленный JSON
            cleaned_data = json.loads(data_str)
            
            # Сохраняем очищенный файл
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
            
            return True
        
        return False
        
    except Exception as e:
        print(f"Ошибка обработки {file_path}: {e}")
        return False

def main():
    """Главная функция"""
    print("🔒 Очистка API токенов из workflows...")
    print("=" * 50)
    
    organized_dir = Path("organized_workflows")
    cleaned_count = 0
    total_files = 0
    
    # Обрабатываем все JSON файлы
    for json_file in organized_dir.rglob("*.json"):
        total_files += 1
        if clean_secrets_in_json(json_file):
            cleaned_count += 1
            print(f"🧹 Очищен: {json_file.name}")
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ОЧИСТКИ")
    print("=" * 50)
    print(f"📁 Всего файлов: {total_files}")
    print(f"🧹 Очищено файлов: {cleaned_count}")
    print(f"✅ Файлов без секретов: {total_files - cleaned_count}")
    
    if cleaned_count > 0:
        print(f"\n🎯 Готово! {cleaned_count} файлов очищены от API токенов.")
        print("💡 Все токены заменены на 'YOUR_API_TOKEN_HERE'")
    else:
        print("\n✅ API токены не найдены!")

if __name__ == "__main__":
    main()
