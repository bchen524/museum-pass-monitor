# Seattle Library Museum Pass Monitor

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, parse_qs


def check_aquarium_passes():
    """Visit the Seattle Library aquarium pass page and check for weekend availability"""
    url = "https://spl.libcal.com/passes/Aquarium"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"Successfully fetched page")
        print(f"Status code: {response.status_code}")
        print("-" * 80)
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links containing "Aquarium/book"
        available_links = soup.find_all('a', href=lambda href: href and 'Aquarium/book' in href)
        
        if not available_links:
            print("No available passes found.")
            return []
        
        print(f"Found {len(available_links)} available slot(s)\n")
        
        weekend_slots = []
        
        for link in available_links:
            href = link.get('href')
            
            # Parse the URL to extract the date parameter
            parsed = urlparse(href)
            params = parse_qs(parsed.query)
            
            if 'date' in params:
                date_str = params['date'][0]  # e.g., "2026-01-12"
                
                # Parse the date
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                
                # Check if it's a weekend (Saturday=5, Sunday=6)
                is_weekend = date_obj.weekday() in [5, 6]
                
                slot_info = {
                    'date': date_str,
                    'day': day_name,
                    'is_weekend': is_weekend,
                    'link': f"https://spl.libcal.com{href}"
                }
                
                if is_weekend:
                    weekend_slots.append(slot_info)
                    print(f"✓ WEEKEND AVAILABLE: {day_name}, {date_str}")
                    print(f"  Book here: {slot_info['link']}\n")
                else:
                    print(f"  Available (weekday): {day_name}, {date_str}")
        
        print("-" * 80)
        if weekend_slots:
            print(f"\n🎉 Found {len(weekend_slots)} weekend slot(s) available!")
            print("\nWeekend dates with availability:")
            for slot in weekend_slots:
                print(f"  • {slot['day']}, {slot['date']}")
        else:
            print("\n❌ No weekend slots available at this time.")
        
        return weekend_slots
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return []


if __name__ == "__main__":
    check_aquarium_passes()

