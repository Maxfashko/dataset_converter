from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
"""
Создание xml файла разметки по стандарту Pascal VOC2007
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

    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.self.rootrettyxml(indent="  ")

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

        size = SubElement(self.root, "size")
        width = SubElement(size, "width")
        width.text = " "
        height = SubElement(size, "height")
        height.text = " "
        depth = SubElement(size, "depth")
        depth.text = " "

        segmented = SubElement(self.root, "segmented")
        segmented.text = "0"

    def set_filename_root(self, name):
        for s in self.root:
            if s.tag == "filename":
                s.text = name
                break

    def set_size_root(self, size):
        d = {"width":size[1], "height":size[0], "depth":size[2]}

        for elem in self.root:
            if elem.tag == "size":
                child = elem.getchildren()
                for val in child:
                    try:
                        if d[val.tag]:
                            val.text=str(d[val.tag])
                    except KeyError as e:
                        print(e)
                break

    def add_sub_object(self, name, bbox, truncated="0", difficult="0", input_root=None):
        if not input_root:
            obj = SubElement(self.root, "object")
        else:
            obj = SubElement(input_root, "object")

        name_ = SubElement(obj, "name")
        name_.text = name
        truncated_ = SubElement(obj, "truncated")
        truncated_.text = truncated
        difficult_ = SubElement(obj, "difficult")
        difficult_.text = difficult

        bndbox = SubElement(obj, "bndbox")
        xmin = SubElement(bndbox, "xmin")
        xmin.text = str(bbox.x1)

        ymin = SubElement(bndbox, "ymin")
        ymin.text = str(bbox.y1)

        xmax = SubElement(bndbox, "xmax")
        xmax.text = str(bbox.x2)

        ymax = SubElement(bndbox, "ymax")
        ymax.text = str(bbox.y2)
