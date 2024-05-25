import threading
import time
import os
from Producer import Producer
from Consumer import Consumer
from QueueManager import MarkupQueue

# Print the current working directory
# print("Current working directory:", os.getcwd())

def read_urls_from_file(fileName):
    fileDir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(fileDir, fileName)

    # Read URLs from the file
    with open(filePath, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def main():
    fileName = 'urls.txt'
    urls = read_urls_from_file(fileName)

    # Create producer threads
    producerThreads = []
    for url in urls:
        producer = Producer(url, MarkupQueue)
        thread = threading.Thread(target=producer.run)
        producerThreads.append(thread)
        thread.start()

    # Create consumer thread
    consumer = Consumer(MarkupQueue)
    consumerThread = threading.Thread(target=consumer.run)
    consumerThread.start()

    # Wait for all producer threads to finish
    for thread in producerThreads:
        thread.join()

    # Stop consumer thread
    MarkupQueue.put((None, None))
    consumerThread.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds") # Output time


