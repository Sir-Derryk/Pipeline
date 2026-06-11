import os
import sys
import argparse
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.links.add(value)

def check_external_link(url):
    """Проверяет внешнюю ссылку через HEAD/GET запрос"""
    try:
        req = urllib.request.Request(
            url, 
            method="HEAD",
            headers={'User-Agent': 'Mozilla/5.0 (UDE Link Checker)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status in [200, 301, 302], f"HTTP {response.status}"
    except urllib.error.HTTPError as e:
        # Некоторые сервера блокируют HEAD-запросы, пробуем GET
        try:
            req.method = "GET"
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200, f"HTTP {response.status}"
        except urllib.error.HTTPError as e_get:
            return False, f"HTTP Error {e_get.code}"
        except Exception:
            return False, f"HTTP Error {e.code}"
    except Exception as e:
        return False, f"Connection error: {e}"

def check_local_links(local_dir):
    """Локально извлекает и проверяет ссылки из всех собранных HTML-файлов"""
    html_files = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"Scanning {len(html_files)} HTML files on disk...")
    all_ok = True

    for file_path in html_files:
        rel_file_path = os.path.relpath(file_path, local_dir)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            extractor = LinkExtractor()
            extractor.feed(html_content)
            
            for link in extractor.links:
                # Пропускаем якоря внутри страницы и пустые ссылки
                if link.startswith("#") or not link.strip():
                    continue

                parsed = urlparse(link)
                # 1. Проверка внешних ссылок
                if parsed.scheme in ["http", "https"]:
                    print(f"[Checking Link] {link} in {rel_file_path}")
                    ok, msg = check_external_link(link)
                    if not ok:
                        print(f"  ❌ BROKEN EXTERNAL: {link} ({msg})")
                        all_ok = False
                
                # 2. Проверка внутренних ссылок
                else:
                    # Убираем якорь из внутренней ссылки
                    clean_link = parsed.path
                    if not clean_link:
                        continue
                    
                    # Проверяем локальный файл
                    if clean_link.startswith("/"):
                        # Абсолютный роут относительно корня дистрибутива
                        target_path = os.path.join(local_dir, clean_link.lstrip("/"))
                    else:
                        # Относительный путь от текущего файла
                        target_path = os.path.join(os.path.dirname(file_path), clean_link)

                    # Проверяем как директорию с index.html, так и flat-файл
                    is_valid = False
                    possible_paths = [
                        target_path,
                        os.path.join(target_path, "index.html"),
                        f"{target_path.rstrip('/')}.html"
                    ]
                    for path in possible_paths:
                        if os.path.exists(path):
                            is_valid = True
                            break

                    if not is_valid:
                        print(f"  ❌ BROKEN INTERNAL: {link} in {rel_file_path}")
                        all_ok = False

        except Exception as e:
            print(f"[Error] Failed to parse {rel_file_path}: {e}")
            all_ok = False

    return all_ok

def main():
    parser = argparse.ArgumentParser(description="UDE Portal Link Checker")
    parser.add_argument("--local-dir", required=True, help="Path to local compiled dist directory")
    
    args = parser.parse_args()
    if not os.path.exists(args.local_dir):
        print(f"[Error] Local directory {args.local_dir} does not exist.")
        sys.exit(1)

    success = check_local_links(args.local_dir)
    if success:
        print("\n[SUCCESS] No broken links found!")
        sys.exit(0)
    else:
        print("\n[ERROR] Broken links found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
