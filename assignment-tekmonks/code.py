from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import re
import json

HOST = "localhost"
PORT = 8000

def fetch_latest_stories():
    url = "https://time.com"
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")

   
    stories = re.findall(r'<a href="(/[\d]+/[^"]+)".?>(.?)</a>', html)

    results = []
    added_titles = set()

    for href, title in stories:
        # Clean title (remove HTML tags, newlines, etc.)
        clean_title = re.sub(r"<.*?>", "", title).strip()
        if clean_title and clean_title not in added_titles:
            results.append({
                "title": clean_title,
                "link": f"https://time.com{href}"
            })
            added_titles.add(clean_title)
        if len(results) == 6:
            break

    return results


class TimeStoriesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/getTimeStories":
            stories = fetch_latest_stories()
            response = json.dumps(stories, indent=4)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found.")


if __name__ == "__main__":
    print(f"Server running on http://{HOST}:{PORT}/getTimeStories")
    server = HTTPServer((HOST, PORT), TimeStoriesHandler)
    server.serve_forever()