from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment

"""
Creating an xml labelme Markup File
"""


class XmlParser:
    def __init__(self):
        self.root = None
        self.create_root()

    def write_root(self, path, input_root=None):
        if not input_root:
            data = ElementTree.tostring(self.root, 'utf-8')
        else:
            data = ElementTree.tostring(input_root, 'utf-8')

        with open(path, "wb") as file:
            file.write(data)

    def create_root(self):
        self.root = Element('annotation')

        comment = Comment('Generated for PyMOTW')
        folder = SubElement(self.root, "folder")
        folder.text = " "
        filename = SubElement(self.root, "filename")
        filename.text = " "

        source = SubElement(self.root, "source")
        source.text = " "

        owner = SubElement(self.root, "owner")
        owner.text = " "

        imagesize = SubElement(self.root, "imagesize")
        nrows = SubElement(imagesize, "nrows")
        nrows.text = " "
        ncols = SubElement(imagesize, "ncols")
        ncols.text = " "
        depth = SubElement(imagesize, "depth")
        depth.text = " "

        segmented = SubElement(self.root, "segmented")
        segmented.text = "0"

    def set_filename_root(self, name):
        for s in self.root:
            if s.tag == "filename":
                s.text = name
                break

    def set_size_root(self, width, height, depth):
        d = {"ncols":width, "nrows":height, "depth":depth}

        for elem in self.root:
            if elem.tag == "imagesize":
                child = elem.getchildren()
                for val in child:
                    try:
                        if d[val.tag]:
                            val.text=str(d[val.tag])
                    except KeyError as e:
                        print(e)
                break

    def add_sub_object(self, name, bbox, _type='bounding_box', deleted="0", verified="0", input_root=None):
        if not input_root:
            obj = SubElement(self.root, "object")
        else:
            obj = SubElement(input_root, "object")

        name_ = SubElement(obj, "name")
        name_.text = name
        deleted_ = SubElement(obj, "deleted")
        deleted_.text = deleted
        verified_ = SubElement(obj, "verified")
        verified_.text = verified

        type_ = SubElement(obj, "type")
        type_.text = _type

        polygon = SubElement(obj, "polygon")
        username = SubElement(polygon, "username")
        username.text = 'admin'

        def make_point(elem, crd):
            pt = SubElement(elem, "pt")
            x = SubElement(pt, "x")
            y = SubElement(pt, "y")
            x.text = str(crd[0])
            y.text = str(crd[1])

        x1, y1, x2, y2 = bbox.x1, bbox.y1, bbox.x2, bbox.y2
        [make_point(polygon, crd) for crd in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]]
