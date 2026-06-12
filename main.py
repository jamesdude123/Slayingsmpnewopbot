import os
import re
import time
import requests
from flask import Flask
from threading import Thread

# 1. Paste your FreeMCServer Public Page URL here
PUBLIC_SERVER_URL"https://freemcserver.net/server/2077426"

app = Flask('')

@app.route('/')
def home():
    return "SlayingSmp Renewal Bot is Online!"

def run_web_server():
    # Runs a small web server so UptimeRobot has something to ping
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def renew_minecraft_server():
    while True:
        try:
            print("Fetching public server page...")
            session = requests.Session()
            # Adding a fake browser header to prevent blocks
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            response = session.get(PUBLIC_SERVER_URL, headers=headers)
            
            if response.status_code == 200:
                # Search the page HTML for the server's internal ID
                server_id_match = re.search(r'data-server-id="([^"]+)"', response.text)
                
                if server_id_match:
                    server_id = server_id_match.group(1)
                    print(f"Found Server ID: {server_id}. Sending renewal ping...")
                    
                    # Target FreeMcServer's public background renewal endpoint
                    renew_url = f"https://freemcserver.net/api/public/server/{server_id}/renew"
                    renew_resp = session.post(renew_url, headers=headers)
                    
                    if renew_resp.status_code == 200:
                        print("Success! SlayingSmp has been renewed for 4 hours.")
                    else:
                        print(f"Failed to renew. API Status: {renew_resp.status_code}")
                else:
                    print("Could not locate the Server ID on your public page. Check your URL!")
            else:
                print(f"Failed to load page. Status: {response.status_code}")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            
        # The script checks and renews every 3 hours (10800 seconds)
        print("Sleeping for 3 hours...")
        time.sleep(10800)

if __name__ == "__main__":
    # Start the web server thread for UptimeRobot
    t = Thread(target=run_web_server)
    t.start()
    # Start the auto-renewal background loop
    renew_minecraft_server()
