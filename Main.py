import threading
import time
import os
from Producer import Producer
from Consumer import Consumer
from QueueManager import UrlQueue, MarkupQueue

def readUrlsFromFile(fileName):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(fileDir, fileName)

    with open(filePath, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def main():
    fileName = 'urls.txt'
    urls = readUrlsFromFile(fileName)

    for url in urls:
        UrlQueue.put(url)

    numProducers = 5  # Amount of producer threads
    producer_threads = []
    for _ in range(numProducers):
        producer = Producer(UrlQueue, MarkupQueue)
        thread = threading.Thread(target=producer.run)
        producer_threads.append(thread)
        thread.start()

    consumer = Consumer(MarkupQueue)
    consumer_thread = threading.Thread(target=consumer.run)
    consumer_thread.start()

    # Waits for all URLs to be processed
    UrlQueue.join()

    # Stops threads
    for _ in range(numProducers):
        UrlQueue.put(None)
    for thread in producer_threads:
        thread.join()

    # Wait for the consumer to finish
    MarkupQueue.put((None, None))
    consumer_thread.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
