import unittest
from unittest.mock import patch
from Consumer import Consumer
from QueueManager import MarkupQueue

class TestConsumer(unittest.TestCase):

    @patch('Consumer.PrettyPrinter.pprint') # Checks pprint without importing it
    def test_consumer(self, mocked_printer_pprint):
        # Create a Consumer instance
        consumer = Consumer(MarkupQueue)

        # Read URLs from urls.txt and put them into the queue
        with open('urls.txt', 'r') as file:
            urls = file.readlines()
            for url in urls:
                MarkupQueue.put((url.strip(), '<a href="https://www.example.org">Example</a>')) # couldn' get this to work without a link

        # Stops the Queue
        MarkupQueue.put((None, None))

        consumer.run()

        hyperlinks_called_with = mocked_printer_pprint.call_args[0][0]

        print("\nTest: Consumer properly extracts and prints hyperlinks")
        print("-" * 50)
        print("Expected hyperlinks:")
        for url in urls:
            print("  -", url.strip())
        print("\nActual hyperlinks:")
        for link in hyperlinks_called_with:
            print("  -", link)

if __name__ == "__main__":
    unittest.main()
