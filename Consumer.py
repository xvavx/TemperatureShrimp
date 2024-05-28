from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s') # Removes the default logging message

class Consumer:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        while True:
            url, markup = self.queue.get()
            if url is None:
                break
            self.extractLogHyperlinks(url, markup)
            self.queue.task_done()

    def extractLogHyperlinks(self, url, markup):
        soup = BeautifulSoup(markup, 'html.parser')
        hyperlinks = [a['href'] for a in soup.find_all('a', href=True)]
        formatted_hyperlinks = "\n".join(hyperlinks[:15])  # Format first 15 hyperlinks
        logging.info(f"\n----------------------------------------------\n\n"
                     f"Hyperlinks from {url}:\n\n{formatted_hyperlinks}")
