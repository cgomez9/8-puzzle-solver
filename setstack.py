from orderedset import OrderedSet
import queue

class SetStack(queue.Queue):
    def _init(self, maxsize):
        self.queue = OrderedSet()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop(True)

    def hasElement(self,element):
        return element in self.queue
