import os
import requests
from flask import Flask

# Your confirmed Server ID URL
PUBLIC_SERVER_URL = "https://freemcserver.net/server/2077426"
SERVER_ID = "2077426"

app = Flask('')

@app.route('/')
def home():
    print("\n--- UptimeRobot Ping Received! Running Renewal Loop ---")
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://freemcserver.net',
        'Referer': PUBLIC_SERVER_URL
    }
    
    # Strategy 1: Let's hit the renewal API directly using your ID token
    try:
        renew_url = f"https://freemcserver.net/api/public/server/{SERVER_ID}/renew"
        print(f"Attempting direct renewal at: {renew_url}")
        
        renew_resp = session.post(renew_url, headers=headers, json={}, timeout=10)
        print(f"API Response Code: {renew_resp.status_code}")
        
        if renew_resp.status_code == 200:
            return f"Success! Sent renewal command for SlayingSmp (ID: {SERVER_ID}). Check your server panel!"
        else:
            # Strategy 2: If direct API fails, try touching the main page first to grab session cookies
            print("Direct API failed, trying with session cookies...")
            session.get(PUBLIC_SERVER_URL, headers=headers, timeout=10)
            renew_resp2 = session.post(renew_url, headers=headers, json={}, timeout=10)
            
            if renew_resp2.status_code == 200:
                return f"Success after cookie refresh! SlayingSmp (ID: {SERVER_ID}) renewed."
            else:
                return f"Server page loaded, but API rejected the request with code {renew_resp2.status_code}. The server might already be at the 4-hour max limit!"

    except Exception as e:
        print(f"❌ Network Error: {e}")
        return f"Automation ran but encountered an error: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
