import sys
import glob
import os.path
import codecs
import copy
import argparse
from tqdm import tqdm

import my_util as myutl
from my_voc import VOC_Labeled_Object, load_voc_labeled_image
from my_label import Labeled_Object

'''
 parse_args()
'''
def parse_args():
    parser = argparse.ArgumentParser(description='replace_voc_class.py')
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
        '-setting',
        dest='setting',
        help='setting json file path',
        default=None,
        type=str
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    in_folder_path = args.input
    if in_folder_path is None or os.path.isdir(in_folder_path) is False:
        print("error: input folder doesn't exist.")
        sys.exit(1)
    setting = args.setting
    if setting is None or os.path.isfile(setting) is False:
        print("error: setting file doesn't exist.")
        sys.exit(1)
    out_folder_path = args.output
    if out_folder_path is None or in_folder_path == out_folder_path:
        print("error: input and output folder should be different with each other.")
        sys.exit(1)
    return parser.parse_args()

'''
replace_class_info(voc_labeled_image, setting)
'''
def replace_class_info(voc_labeled_image, setting):
    cat_name_pair_list = setting["class_names"]
    objects            = voc_labeled_image.objects
    new_objects        = []
    #loop for objects
    for org_object in objects:
        cat_name = org_object.class_name
        new_cat_name = None
        #loop for class_name
        for cat_name_pair in cat_name_pair_list:
            old_cat_name = cat_name_pair[0]
            if cat_name == old_cat_name:
                new_cat_name = cat_name_pair[1]
                break
        if new_cat_name is None:
            #cat_name was unmatched with any old_cat_names
            print("warning: unmatched class " + cat_name)
            print(voc_labeled_image.filename)
            continue
        #difficult fl
        new_difficult_fl = int(cat_name_pair[2])
        if new_difficult_fl == -1:
            #delete object
            continue
        #get object info from original one
        new_x         = org_object.x
        new_y         = org_object.y
        new_width     = org_object.width
        new_height    = org_object.height
        new_truncated = org_object.truncated
        #create new object      
        new_object = VOC_Labeled_Object(0, new_cat_name, new_x, new_y, new_width, new_height, new_truncated, new_difficult_fl)
        if hasattr(org_object, "confidence"):
            new_object.confidence = org_object.confidence            
        #append
        new_objects.append(new_object)

    voc_labeled_image.objects = new_objects
            
    return voc_labeled_image
    

'''
main(args)
'''
def main(args):
    in_folder_path    = args.input
    out_folder_path   = args.output
    setting_file_path = args.setting
    #create output folder if it doesn't exist.
    if os.path.isdir(out_folder_path) is False:
        os.makedirs(out_folder_path)
    #parse json data
    setting = myutl.load_json(setting_file_path)

    #get input xml file path list
    xml_file_path_list = glob.glob(in_folder_path + "/*.xml")
    for xml_file_path in tqdm(xml_file_path_list):
        #print(xml_file_path)
        #load xml file as a voc labeled image
        #print(xml_file_path)
        voc_labeled_image = load_voc_labeled_image(xml_file_path)
        #replace class information
        new_labeled_image = replace_class_info(voc_labeled_image, setting)
        if new_labeled_image is None:
            print("warning: new labeled image is None")
            print(xml_file_path)
            continue
        #output new voc label
        new_xml_str   = new_labeled_image.get_label_str()
        new_file_name = os.path.basename(xml_file_path)
        new_file_path = out_folder_path + "/" + new_file_name
        new_file      = codecs.open(new_file_path, 'w', 'utf-8')
        new_file.write(new_xml_str)
        new_file.close()
    
if __name__ == '__main__':
    args = parse_args()
    main(args)
