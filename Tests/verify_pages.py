import os
import sys
import argparse
import urllib.request
import urllib.error
from html.parser import HTMLParser

# A simple parser to extract text content from HTML
class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []

    def handle_data(self, data):
        self.text_content.append(data)

    def get_text(self):
        return " ".join(self.text_content)

def extract_signature_from_md(md_path):
    """Extracts the first '#' heading as the page signature"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    # Return the clean heading text without the '#' character
                    return line[2:].strip()
    except Exception as e:
        print(f"[Warning] Failed to read {md_path}: {e}")
    return None

def get_expected_pages(user_docs_root):
    """Scans sources and returns a dictionary of {route: signature}"""
    expected = {}

    # Add the main page
    index_md = os.path.join(user_docs_root, "index.md")
    if os.path.exists(index_md):
        expected["/"] = "Universal Document Engine"

    # Traverse guide files (VitePress)
    docs_dir = os.path.join(user_docs_root, "docs")
    if os.path.exists(docs_dir):
        for root, _, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, docs_dir).replace("\\", "/")
                    route_name = rel_path[:-3]  # strip .md extension
                    route = f"/docs/{route_name}"
                    sig = extract_signature_from_md(full_path)
                    if sig:
                        expected[route] = sig

    # Traverse API Reference files (Hugo)
    api_dir = os.path.join(user_docs_root, "hugo-site", "content", "api")
    if os.path.exists(api_dir):
        # Add the main API page
        expected["/api"] = "UDE API Index"
        for root, _, files in os.walk(api_dir):
            for file in files:
                if file.endswith(".md") and file != "_index.md":
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, api_dir).replace("\\", "/")
                    route_name = rel_path[:-3]  # strip .md extension
                    route = f"/api/{route_name}".lower()
                    sig = extract_signature_from_md(full_path)
                    if sig:
                        expected[route] = sig

    return expected

def verify_local(local_dir, route, signature):
    """Local file check on disk"""
    # In VitePress/Docusaurus, routes are compiled to index.html in nested directories
    if route == "/":
        file_path = os.path.join(local_dir, "index.html")
    else:
        # Remove the leading slash for correct path joining
        clean_route = route.lstrip("/")
        file_path = os.path.join(local_dir, clean_route, "index.html")
        # Also check the alternative flat file option (e.g., docs/getting-started.html)
        if not os.path.exists(file_path):
            file_path = os.path.join(local_dir, f"{clean_route}.html")

    if not os.path.exists(file_path):
        return False, f"Missing compiled file: {file_path}"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            parser = HTMLTextExtractor()
            parser.feed(html_content)
            plain_text = parser.get_text()
            if signature.lower() in plain_text.lower():
                return True, "Verified"
            return False, f"Signature '{signature}' not found in text"
    except Exception as e:
        return False, f"Error reading file: {e}"

def verify_remote(base_url, route, signature):
    """Remote page check via HTTP"""
    url = base_url.rstrip("/") + route
    # For VitePress, routes usually end with a slash
    if route != "/":
        url += "/"
        
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (UDE Portal Test Runner)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8')
            parser = HTMLTextExtractor()
            parser.feed(html_content)
            plain_text = parser.get_text()
            if signature.lower() in plain_text.lower():
                return True, "Verified"
            return False, f"Signature '{signature}' not found in HTTP response"
    except urllib.error.HTTPError as e:
        return False, f"HTTP Error {e.code}: {e.reason}"
    except Exception as e:
        return False, f"Connection error: {e}"

def main():
    parser = argparse.ArgumentParser(description="UDE Portal Page and Signature Verifier")
    parser.add_argument("--local-dir", help="Path to local compiled dist directory (e.g. user-docs/.vitepress/dist)")
    parser.add_argument("--remote-url", help="Base URL of deployed portal (e.g. https://Sir-Derryk.github.io/ude-user-docs)")
    parser.add_argument("--user-docs", default="./user-docs", help="Path to user-docs sources")
    
    args = parser.parse_args()
    if not args.local_dir and not args.remote_url:
        print("[Error] Please specify either --local-dir or --remote-url")
        sys.exit(1)

    expected_pages = get_expected_pages(args.user_docs)
    if not expected_pages:
        print("[Error] No source pages found to verify.")
        sys.exit(1)

    print(f"Loaded {len(expected_pages)} expected pages from source MD files.")
    
    failed = 0
    for route, signature in expected_pages.items():
        if args.local_dir:
            success, msg = verify_local(args.local_dir, route, signature)
            mode = "LOCAL"
        else:
            success, msg = verify_remote(args.remote_url, route, signature)
            mode = "REMOTE"

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"[{mode}] {status} | Route: {route:<30} | {msg}")
        if not success:
            failed += 1

    if failed > 0:
        print(f"\n[ERROR] Verification failed. {failed} page(s) failed checks.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All pages verified successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
