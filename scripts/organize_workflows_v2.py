#!/usr/bin/env python3
import os
import json
import shutil
from pathlib import Path
from collections import defaultdict

def organize_workflows():
    print("🚀 Запуск организации с популярными категориями...")
    print("=" * 50)
    
    # Популярные категории для фриланса
    categories = {
        "ai-automation": ["openai", "chatgpt", "ai", "gpt", "bot", "chatbot"],
        "lead-generation": ["lead", "prospect", "linkedin", "scraping", "generation"],
        "social-media-automation": ["facebook", "twitter", "instagram", "social"],
        "email-marketing": ["mailchimp", "activecampaign", "email", "newsletter"],
        "crm-sales": ["hubspot", "salesforce", "crm", "sales", "deal"],
        "data-processing": ["sheets", "excel", "csv", "airtable", "data"],
        "e-commerce": ["shopify", "woocommerce", "stripe", "ecommerce", "shop"],
        "customer-support": ["support", "ticket", "telegram", "whatsapp"],
        "project-management": ["trello", "asana", "monday", "task", "project"],
        "marketing-automation": ["marketing", "campaign", "funnel", "analytics"],
        "integrations-api": ["webhook", "api", "integration", "zapier", "make"],
        "business-intelligence": ["analytics", "dashboard", "report", "metrics"]
    }
    
    source_dir = Path("workflows")
    target_dir = Path("organized_workflows")
    
    # Очищаем и создаем новую структуру
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir()
    
    for category in categories.keys():
        (target_dir / category).mkdir()
    (target_dir / "uncategorized").mkdir()
    (target_dir / "my-workflows").mkdir()
    
    json_files = list(source_dir.glob("*.json"))
    print(f"📁 Найдено {len(json_files)} workflows")
    
    stats = defaultdict(int)
    
    for i, json_file in enumerate(json_files):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            text = json_file.name.lower() + " "
            if 'name' in data:
                text += data['name'].lower() + " "
            
            category_scores = defaultdict(int)
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in text:
                        category_scores[category] += 1
            
            category = max(category_scores, key=category_scores.get) if category_scores else "uncategorized"
            
            target_file = target_dir / category / json_file.name
            shutil.copy2(json_file, target_file)
            stats[category] += 1
            
            if (i + 1) % 200 == 0:
                print(f"📊 Обработано: {i + 1}/{len(json_files)}")
                
        except Exception as e:
            target_file = target_dir / "uncategorized" / json_file.name
            shutil.copy2(json_file, target_file)
            stats["uncategorized"] += 1
    
    # Выводим результаты
    print("\n" + "="*50)
    print("📊 РЕЗУЛЬТАТЫ")
    print("="*50)
    
    emojis = {
        "ai-automation": "🤖", "lead-generation": "🎯", 
        "social-media-automation": "📱", "email-marketing": "📧",
        "crm-sales": "💼", "data-processing": "📊",
        "e-commerce": "🛒", "customer-support": "🎧",
        "project-management": "📋", "marketing-automation": "📈",
        "integrations-api": "🔗", "business-intelligence": "📉",
        "uncategorized": "📁"
    }
    
    total = sum(stats.values())
    for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        emoji = emojis.get(category, "📄")
        percent = (count/total)*100 if total > 0 else 0
        print(f"{emoji} {category:25} {count:4} workflows ({percent:.1f}%)")
    
    print(f"\n🎯 Всего: {total} workflows")
    return True

if __name__ == "__main__":
    organize_workflows()
