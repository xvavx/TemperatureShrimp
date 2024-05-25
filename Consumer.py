from bs4 import BeautifulSoup
import logging
from pprint import PrettyPrinter

class Consumer:
    def __init__(self, queue):
        self.queue = queue
        self.printer = PrettyPrinter(indent=2)

    def run(self):
        while True:
            url, markup = self.queue.get()
            if url is None:
                break
            self.extract_and_print_hyperlinks(url, markup)
            self.queue.task_done()

    def extract_and_print_hyperlinks(self, url, markup):
        soup = BeautifulSoup(markup, 'html.parser')
        hyperlinks = [a['href'] for a in soup.find_all('a', href=True)]
        logging.info(f"Hyperlinks from {url}:")
        print("-" * 50)# Print a separator line
        self.printer.pprint(hyperlinks[:15])  # Print first 15 hyperlinks
