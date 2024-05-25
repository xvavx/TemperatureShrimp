import requests

class Producer:
    def __init__(self, url, queue):
        self.url = url
        self.queue = queue

    def run(self):
        try:
            awnser = requests.get(self.url)
            if awnser.status_code == 200:
                self.queue.put((self.url, awnser.text))
            else:
                print(f"Failed to fetch {self.url} with status code {awnser.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching {self.url}: {e}")
