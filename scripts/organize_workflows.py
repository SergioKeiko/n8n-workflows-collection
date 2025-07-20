#!/usr/bin/env python3
"""
N8N Workflow Organizer - Simple Version
Простая версия для быстрого запуска на macOS
Created by: Sergey
"""

import os
import json
import shutil
from pathlib import Path
from collections import defaultdict

def organize_workflows():
    """Организует workflows по категориям"""
    print("🚀 Запуск организации N8N workflows...")
    print("=" * 50)
    
    # Категории и ключевые слова для классификации
    categories = {
        "ai-automation": [
            "openai", "chatgpt", "claude", "ai", "gpt", "llm", "langchain", 
            "chatbot", "bot", "artificial", "intelligence", "machine", "learning"
        ],
        "crm-sales": [
            "hubspot", "salesforce", "pipedrive", "crm", "lead", "sales", 
            "deal", "contact", "customer", "prospect", "zoho", "bitrix"
        ],
        "email-marketing": [
            "mailchimp", "activecampaign", "sendgrid", "email", "newsletter", 
            "campaign", "brevo", "klaviyo", "getresponse", "convertkit", "mail"
        ],
        "social-media": [
            "facebook", "twitter", "instagram", "linkedin", "tiktok", 
            "youtube", "telegram", "whatsapp", "discord", "slack", "social"
        ],
        "data-processing": [
            "sheets", "excel", "csv", "airtable", "notion", "database", 
            "mysql", "postgres", "mongodb", "redis", "transform", "data"
        ],
        "integrations": [
            "webhook", "api", "rest", "graphql", "zapier", "make", 
            "http", "integration", "connect", "sync"
        ],
        "monitoring": [
            "monitor", "alert", "notification", "ping", "uptime", 
            "error", "log", "tracking", "report", "status"
        ],
        "ecommerce": [
            "shopify", "woocommerce", "stripe", "paypal", "payment", 
            "order", "product", "inventory", "ecommerce", "store", "shop"
        ],
        "productivity": [
            "task", "todo", "calendar", "scheduler", "timer", "reminder", 
            "project", "trello", "asana", "monday", "workflow", "time"
        ],
        "restaurant-business": [
            "restaurant", "food", "delivery", "menu", "order", "kitchen", 
            "reservation", "cafe", "horeca", "pos", "table", "cook"
        ]
    }
    
    source_dir = Path("workflows")
    target_dir = Path("organized_workflows")
    
    if not source_dir.exists():
        print("❌ Папка workflows не найдена!")
        return False
    
    json_files = list(source_dir.glob("*.json"))
    
    if not json_files:
        print("❌ JSON файлы не найдены в папке workflows/")
        return False
    
    print(f"📁 Найдено {len(json_files)} JSON файлов для организации")
    print("🔄 Начинаем обработку...")
    print()
    
    stats = defaultdict(int)
    processed_count = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            analysis_text = ""
            analysis_text += json_file.name.lower() + " "
            
            if 'name' in workflow_data:
                analysis_text += workflow_data['name'].lower() + " "
            
            if 'nodes' in workflow_data:
                for node in workflow_data['nodes']:
                    if 'type' in node:
                        analysis_text += node['type'].lower() + " "
                    if 'parameters' in node:
                        analysis_text += str(node['parameters']).lower() + " "
            
            category_scores = defaultdict(int)
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in analysis_text:
                        category_scores[category] += 1
            
            if category_scores:
                category = max(category_scores, key=category_scores.get)
            else:
                category = "uncategorized"
            
            target_category_dir = target_dir / category
            target_file = target_category_dir / json_file.name
            
            target_category_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(json_file, target_file)
            stats[category] += 1
            processed_count += 1
            
            if processed_count % 200 == 0:
                print(f"📊 Обработано: {processed_count}/{len(json_files)}")
            
        except Exception as e:
            print(f"❌ Ошибка обработки {json_file.name}: {e}")
            try:
                target_category_dir = target_dir / "uncategorized"
                target_category_dir.mkdir(parents=True, exist_ok=True)
                target_file = target_category_dir / json_file.name
                shutil.copy2(json_file, target_file)
                stats["uncategorized"] += 1
            except:
                pass
    
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТЫ ОРГАНИЗАЦИИ")
    print("="*60)
    
    total = sum(stats.values())
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    emojis = {
        "ai-automation": "🤖", "crm-sales": "💼", "email-marketing": "📧",
        "social-media": "📱", "data-processing": "📊", "integrations": "🔗",
        "monitoring": "📈", "ecommerce": "🛒", "productivity": "⚡",
        "restaurant-business": "🍕", "my-workflows": "💎", "uncategorized": "📁"
    }
    
    for category, count in sorted_stats:
        percentage = (count / total) * 100 if total > 0 else 0
        emoji = emojis.get(category, "📄")
        print(f"{emoji} {category:22} {count:4} файлов ({percentage:.1f}%)")
    
    print(f"\n🎯 Всего обработано: {total} файлов")
    print(f"✅ Организация завершена успешно!")
    
    create_readme(stats, emojis)
    return True

def create_readme(stats, emojis):
    readme_content = f"""# 🚀 My N8N Workflows Collection

> **Автор:** Sergey - Marketing Automation & No-Code Specialist  
> **Upwork:** [https://www.upwork.com/fl/~017d2e8eb206e2c1ac](https://www.upwork.com/fl/~017d2e8eb206e2c1ac)

## 📊 Статистика коллекции

**Всего workflows:** {sum(stats.values())}

### По категориям:

"""
    
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    for category, count in sorted_stats:
        emoji = emojis.get(category, "📄")
        readme_content += f"- {emoji} **{category}**: {count} workflows\n"
    
    readme_content += """

## 🔧 Использование

1. Перейдите в нужную категорию в папке `organized_workflows/`
2. Выберите подходящий workflow (JSON файл)
3. Импортируйте в n8n через меню Import workflow
4. Настройте credentials и параметры

## 🎯 Для ресторанного бизнеса

Специальная категория `restaurant-business/` содержит workflows для:
- Автоматизация заказов
- Управление доставкой  
- Обратная связь клиентов
- Управление запасами
- Интеграция с POS системами

---

*Автоматически организовано*
"""
    
    readme_path = Path("organized_workflows/README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📝 Создан файл: {readme_path}")

if __name__ == "__main__":
    success = organize_workflows()
    
    if success:
        print("\n🌟 Готово! Проверьте папку organized_workflows/")
        print("\n💡 Следующие шаги:")
        print("   1. Откройте папку organized_workflows/")
        print("   2. Выберите нужную категорию")
        print("   3. Импортируйте workflow в n8n")
        print("   4. Добавляйте свои workflows в my-workflows/")
    else:
        print("\n❌ Организация завершена с ошибками")
