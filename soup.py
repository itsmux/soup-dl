import sys
import os
import argparse
import xml.etree.ElementTree as ET
import Queue
import threading
import urllib


USAGE = u"Usage: python soup.py yourfile.rss"
DATA_FOLDER = "data"


class SoupDownloader(threading.Thread):
    """SoupDownloader class

    """
    def __init__(self, queue):
        """

        """
        super(SoupDownloader, self).__init__()
        self.queue = queue

    def run(self):
        """

        """
        while True:

            url = self.queue.get()
            print u"Downloading %s" % url

            # Filename and path
            file_name = os.path.basename(url)
            path = os.path.join(DATA_FOLDER, file_name)

            # Download file
            if not os.path.isfile(path):
                urllib.urlretrieve(url, path)

            self.queue.task_done()


class SoupParser(object):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        """
        self.queue = kwargs.pop('queue')

    def parse_item(self, item):
        """

        """
        enclosure = item.find('enclosure')
        if enclosure is not None and enclosure.get('type') == 'image/jpeg':
            url = enclosure.get('url')
            self.queue.put(url)

    def parse(self, xml):
        tree = ET.parse(xml)
        root = tree.getroot()
        channel = root.find('channel')
        items = channel.findall('item')
        for item in items:
            self.parse_item(item)


class Soup(object):
    """Soup class.

    """
    def __init__(self, *args, **kwargs):
        self.rss = kwargs.pop('rss')
        self.parser = kwargs.pop('parser')

    def prepare_folder(self):
        """Checks for existence of DATA_FOLDER or creates it.

        """
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

    def process(self):
        """Process the soup.io RSS file and download all images.

        """
        self.prepare_folder()
        self.parser.parse(self.rss)


def main(args):
    """

    """
    # Parse args and get the RSS filename
    try:
        rss = args[1]
    except IndexError:
        print USAGE
        return

    # Init the dl queue
    queue = Queue.Queue()

    # Spawn a pool of threads and pass them queue instance
    for i in range(10):
        thread = SoupDownloader(queue)
        thread.setDaemon(True)
        thread.start()

    # Add a parser and init Soup
    parser = SoupParser(queue=queue)
    soup = Soup(rss=rss, parser=parser)
    soup.process()

    # Wait for the queue to finish
    queue.join()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
