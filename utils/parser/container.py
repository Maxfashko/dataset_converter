
class BBox(object):
    """docstring for BBox"""
    def __init__(self, **kwargs):
        super(BBox, self).__init__()
        self.x1 = kwargs['x1']
        self.x2 = kwargs['x2']
        self.y1 = kwargs['y1']
        self.y2 = kwargs['y2']


class Container(object):
    """docstring for Container"""
    def __init__(self, **kwargs):
        super(Container, self).__init__()
        self.bbox = kwargs['bbox']
        self.label = kwargs['label']


class Containers(object):
    """docstring for Containers"""
    def __init__(self, **kwargs):
        super(Containers, self).__init__()
        self._containers = {}

    def add(self, name, val):
        if type(self._containers.get(name)) == list:
            self._containers[name].append(val)
        else:
            self._containers[name] = []
            self._containers[name].append(val)

    def get_classes(self):
        s = set()
        for fn, containers in self._containers.items():
            for container in containers:
                s.add(str(container.label))
        return {val:idx+1 for idx, val in enumerate(s)}

    def containers():
        doc = "The containers property."
        def fget(self):
            for key, val in self._containers.items():
                yield key, val
        def fdel(self):
            del self._containers
        return locals()
    containers = property(**containers())
