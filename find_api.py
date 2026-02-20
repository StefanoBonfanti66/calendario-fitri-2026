import requests
from bs4 import BeautifulSoup

def find_api():
    base_url = "https://www.myfitri.it"
    r = requests.get(f"{base_url}/calendario")
    soup = BeautifulSoup(r.text, 'html.parser')
    scripts = [s['src'] for s in soup.find_all('script') if s.has_attr('src')]
    
    for s in scripts:
        script_url = base_url + s
        print(f"Checking {script_url}...")
        r2 = requests.get(script_url)
        if 'api' in r2.text.lower() or 'calendario' in r2.text.lower():
            print(f"Found in {s}")
            # Try to find something like /api/.../
            import re
            matches = re.findall(r'/[a-zA-Z0-9_-]+/api/[^\s"\']+', r2.text)
            for m in matches:
                print(f"Possible API: {m}")
            # Also search for calendario
            matches = re.findall(r'/[^\s"\']*calendario[^\s"\']*', r2.text)
            for m in matches:
                print(f"Possible Calendario related: {m}")

if __name__ == "__main__":
    find_api()
