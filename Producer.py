import requests
import logging

class Producer:
    def __init__(self, urlQueue, markupQueue):
        self.urlQueue = urlQueue
        self.markupQueue = markupQueue

    def run(self):
        while True:
            url = self.urlQueue.get()
            if url is None:
                self.urlQueue.task_done()
                break
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    self.markupQueue.put((url, response.text))
                else:
                    logging.error(f"Failed to fetch {url} with status code {response.status_code}")
            except requests.RequestException as e:
                logging.error(f"Error fetching {url}: {e}")
            finally:
                self.urlQueue.task_done()
