# To parse XML
import xmltodict
import codecs
import os.path

from my_python.my_label import Labeled_Image, Labeled_Object

'''
VOC_Labeled_Image
'''


class VOC_Labeled_Image(Labeled_Image):
    # constructor
    def __init__(self, filepath, width, height, objects):
        super().__init__(filepath, width, height, objects)
        self.filepath = filepath
        self.folder = os.path.basename(os.path.dirname(filepath))
        self.filename = os.path.basename(filepath)
        self.width = width
        self.height = height
        self.database = "Unknown"
        self.depth = 3
        self.segmented = 0
    '''
    get_label_str
    '''

    def get_label_str(self):
        label_dict = {"annotation": {
            "folder": self.folder,
            "filename": self.filename,
            "path": self.filepath,
            "source":
            {
                "database": self.database
            },
                "size": {
                    "width": self.width,
                    "height": self.height,
                    "depth": self.depth
            },
            "segmented": 0,
                "object": []
        }}
        # get objects information as dictionary.
        # and append them to ["object"] list.
        for obj in self.objects:
            obj_dict = obj.get_info_as_output_fmt()
            label_dict["annotation"]["object"].append(obj_dict)

        return xmltodict.unparse(label_dict, pretty=True)


'''
VOC_Object
'''


class VOC_Labeled_Object(Labeled_Object):
    # constructor
    def __init__(self, class_id, class_name, x, y, width, height, truncated, difficult):
        super().__init__(class_id, class_name, x, y, width, height)
        self.truncated = truncated
        self.difficult = difficult
        self.pose = "Unspecified"

    def get_info_as_output_fmt(self):
        # on voc format, pixcel number starts (1,1).
        obj_dict = {
            "name": self.class_name,
            "pose": self.pose,
            "truncated": self.truncated,
            "difficult": self.difficult,
            "bndbox": {
                "xmin": (self.x + 1),
                "ymin": (self.y + 1),
                "xmax": (self.x + self.width),
                "ymax": (self.y + self.height)
            }
        }
        # additional attributes
        if self.confidence >= 0:
            obj_dict["confidence"] = self.confidence
        if self.iou >= 0:
            obj_dict["iou"] = self.iou
        if self.object_id >= 0:
            obj_dict["object_id"] = self.object_id

        return obj_dict


'''
load_voc_labeled_image
'''


def load_voc_labeled_image(xml_file_path):

    if os.path.isfile(xml_file_path) == False:
        return None

    xml_file = codecs.open(xml_file_path, 'r', 'utf-8')
    xml_text = xml_file.read()
    xml_file.close()
    xml_data = xmltodict.parse(xml_text)

    annotation = xml_data["annotation"]
    filepath = annotation["path"]
    img_width = int(annotation["size"]["width"])
    img_height = int(annotation["size"]["height"])

    objects = []
    if "object" in annotation:
        objects = annotation["object"]
        is_list = isinstance(objects, list)
        if is_list is False:
            # if there is an object only, create a dummy list
            objects = [objects]

    voc_objects = []
    for obj in objects:
        class_id = -1
        class_name = obj["name"]
        bndbox = obj["bndbox"]
        x = int(bndbox["xmin"]) - 1
        y = int(bndbox["ymin"]) - 1
        width = int(bndbox["xmax"]) - x
        height = int(bndbox["ymax"]) - y

        if width < 1:
            continue
        if height < 1:
            continue

        truncated = int(obj["truncated"])
        difficult = int(obj["difficult"])

        voc_object = VOC_Labeled_Object(
            class_id, class_name, x, y, width, height, truncated, difficult)

        if "confidence" in obj:
            confidence = float(obj["confidence"])
            voc_object.confidence = confidence
        elif "score" in obj:
            confidence = float(obj["score"])
            voc_object.confidence = confidence
        if "iou" in obj:
            iou = float(obj["iou"])
            voc_object.iou = iou

        voc_objects.append(voc_object)

    voc_labeled_image = VOC_Labeled_Image(
        filepath, img_width, img_height, voc_objects)

    return voc_labeled_image
