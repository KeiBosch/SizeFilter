import sys
import glob
import os.path
import json
import codecs
import shutil
import xmltodict
import argparse
from tqdm import tqdm

import my_util as utl
from my_voc import VOC_Labeled_Image, VOC_Labeled_Object, load_voc_labeled_image

def parse_args():
    parser = argparse.ArgumentParser(description='json2voc')
    parser.add_argument(
        '-in',
        dest='input',
        help='input folder path',
        default=None,
        type=str
    )
    parser.add_argument(
        '-out',
        dest='output',
        help='output folder path',
        default=None,
        type=str
    )
    parser.add_argument(
        '-name',
        dest='name',
        help='dataset name',
        default=None,
        type=str
    )
    parser.add_argument(
        '-json_class',
        dest='json_class',
        help='json class list file path',
        default=None,
        type=str
    )
    parser.add_argument(
        '-img_do',
        dest='img_do',
        help='None(default), cp, mv',
        default=None,
        type=str
    )
    parser.add_argument(
        '-name_tag',
        dest='name_tag',
        help='if you want to append string to name of annotation data, set it as name_tag',
        default="",
        type=str
    )
    parser.add_argument(
        '-default_class_name',
        dest='default_class_name',
        help='(Optional) all objects class name is replaced with the name you set',
        default=None,
        type=str
    )
    parser.add_argument(
        '-ann_img_ext',
        dest='ann_img_ext',
        help='(Optional) if you want to replace extention of image in output json file, set the extention name.',
        default=None,
        type=str
    )
    parser.add_argument(
        '-add_no_object_images',
        dest='add_no_object_images',
        help='(Optional) if you want to append images which do not have any objects, set this flag.',
        action='store_true',
        default=False
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

'''
get_init_coco_label
'''
def get_init_coco_label():
    init_coco_label = {
        "type":"instances",
        "images":[],
        "annotations":[],
        "categories":[]
    }
    return init_coco_label

'''
load_voc_label
'''
def load_voc_label(xml_file_path):
    xml_file  = codecs.open(xml_file_path, 'r', 'utf-8')
    xml_text  = xml_file.read()
    xml_file.close()
    voc_label = xmltodict.parse(xml_text)
    return voc_label

'''
get_class_id
'''
def get_class_id(coco_label, class_name):
    cat_infos = coco_label["categories"]
    cat_ids = [cat_info["id"] for cat_info in cat_infos if cat_info["name"] == class_name]
    if len(cat_ids) == 0:
        return -1
    cat_id  = cat_ids[0]
    return cat_id

'''
append_voc_label_to_coco
'''
def append_voc_label_to_coco(coco_label, voc_labeled_image, default_name, ann_img_ext=None):
    
    xml_file_name      = os.path.basename(voc_labeled_image.xml_file_path)
    xml_file_stem, ext = os.path.splitext(xml_file_name)
    
    #image information
    image_id        = len(coco_label["images"]) + 1
    #image_file_name = voc_labeled_image.filename
    image_file_name = xml_file_stem + ".jpg"
    image_width     = voc_labeled_image.width
    image_height    = voc_labeled_image.height
    
    if ann_img_ext is not None:
        file_stem, ext  = os.path.splitext(image_file_name)
        image_file_name = file_stem + ann_img_ext
    
    image = {
        "id":image_id,
        "file_name":image_file_name,
        "width":image_width,
        "height":image_height,
    }
    #append a image object
    coco_label["images"].append(image)
    
    #object information
    voc_objects = voc_labeled_image.objects
    for voc_object in voc_objects:
        class_name = voc_object.class_name
        if default_name is not None:
            class_name = default_name
        class_id   = get_class_id(coco_label, class_name)
        if class_id == -1:
            continue

        object_id       = len(coco_label["annotations"]) + 1 
        x               = voc_object.x
        y               = voc_object.y
        width           = voc_object.width
        height          = voc_object.height
        xmax            = x + width
        ymax            = y + height
        segmentation    = []
        segmentation.append([x,y, x,ymax, xmax,ymax, xmax,y])
        area            = width * height
        bbox            = [x, y, width, height]
        iscrowd         = 0
        ignore          = voc_object.difficult
        
        coco_object = {
            "id":object_id,
            "category_id":class_id,
            "image_id":image_id,
            "segmentation":segmentation,
            "area":area,
            "bbox":bbox,
            "iscrowd":iscrowd,
            "ignore":ignore
        }
        
        #append an annotation object
        coco_label["annotations"].append(coco_object)

    return True

'''
main
'''
def main(args):
    input_folder_path = args.input
    if os.path.isdir(input_folder_path) is False:
        print("error : input folder is not exist.")
        print(input_folder_path)
        sys.exit(1)
    dataset_name = args.name
    if dataset_name is None:
        print("error: dataset_name is required.")
        sys.exit(1)
    output_folder_path = args.output + "/" + dataset_name
    if os.path.isdir(output_folder_path) is False:
        os.makedirs(output_folder_path)
    
    #get initial coco label object
    coco_label = get_init_coco_label()
    
    #get json class list
    json_class_data  = utl.load_json(args.json_class)
    coco_label["categories"] = json_class_data["categories"]
    
    add_no_object_images = args.add_no_object_images
    
    #get voc xml file list
    xml_file_path_list = glob.glob(input_folder_path + "/*.xml")
    for xml_file_path in xml_file_path_list:
        #print(xml_file_path)
        voc_labeled_image = load_voc_labeled_image(xml_file_path)
        if voc_labeled_image is None:
            continue
        if len(voc_labeled_image.objects) == 0:
            #print("warning : xml file does not have any bboxes.")
            #print(xml_file_path)
            if add_no_object_images is False:
                continue
            
        voc_labeled_image.xml_file_path = xml_file_path
        append_voc_label_to_coco(coco_label, voc_labeled_image, args.default_class_name, args.ann_img_ext)
    
    if len(coco_label["annotations"]) == 0:
        print("error : no object appended.")
        print(dataset_name)
        sys.exit(1)
    
    #output an annotation json file
    ann_file_path = output_folder_path + "/" + dataset_name + args.name_tag + ".json"
    ann_file = codecs.open(ann_file_path, 'w', 'utf-8')
    json.dump(coco_label, ann_file)
    ann_file.close()
    
    img_do = args.img_do
    if img_do is not None:
        img_folder_path = output_folder_path + "/" + dataset_name
        if os.path.isdir(img_folder_path) is False:
            os.makedirs(img_folder_path)
        jpg_file_list = glob.glob(input_folder_path + "/*.jpg")
        for jpg_file_path in jpg_file_list:
            if os.path.isfile(jpg_file_path) is False:
                continue
            jpg_file_name   = os.path.basename(jpg_file_path)
            output_jpg_path = img_folder_path + "/" + jpg_file_name
            if img_do == "cp":
                if os.path.isfile(output_jpg_path) is True:
                    continue
                shutil.copy(jpg_file_path, img_folder_path)
            elif img_do == "mv":
                if os.path.isfile(output_jpg_path) is True:
                    os.remove(output_jpg_path)
                shutil.move(jpg_file_path, img_folder_path)
    
if __name__ == '__main__':
    args = parse_args()
    main(args)
    
