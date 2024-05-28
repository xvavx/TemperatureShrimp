import unittest
from unittest.mock import patch
from Consumer import Consumer
from QueueManager import MarkupQueue

class TestConsumer(unittest.TestCase):

    @patch('Consumer.logging.info')
    def test_consumer(self, mockedLogInfo):
        consumer = Consumer(MarkupQueue)

        # Read URLs from urls.txt and put them into the queue
        with open('urls.txt', 'r') as file:
            urls = file.readlines()
            for url in urls:
                MarkupQueue.put((url.strip(), '<a href="https://www.wikipedia.org">Example</a>'))

        MarkupQueue.put((None, None))
        consumer.run()

        hyperlinksCalled = [call[0][0] for call in mockedLogInfo.call_args_list]

        print("\nTest: Consumer properly extracts and logs hyperlinks")
        print("-" * 50)
        print("Expected hyperlinks:")
        for url in urls:
            print(f"  - {url.strip()}")
        print("\nActual hyperlinks:")
        for link in hyperlinksCalled:
            print(f" {link}")

if __name__ == "__main__":
    unittest.main()
