"""VOC Size Filter"""
import os.path
import glob
from my_python.my_voc import load_voc_labeled_image


def main():
    """main function"""
    # input VOC path
    xml_area_path = r"D:\VSI\VsiZenrinSignTrackingFinal\input\2_DNN_Detection_Result_Files_Ground-Truth_20200319\nagoya_test"
    # output VOC path
    output_path = r"D:\VSI\VsiZenrinSignTrackingFinal\input\2_DNN_Detection_Result_Files_Ground-Truth_20200319_1800\nagoya_test"
    # set the minimum size of boxes
    size = 1800

    # get sub folders
    xml_dir_list = os.listdir(xml_area_path)

    # Loop each sub folder
    for xml_dir in xml_dir_list:
        # make a new folder to output folder with the same name as input
        os.makedirs(os.path.join(output_path, xml_dir))
        # get XML file list in the sub folder
        xml_file_list = glob.glob(os.path.join(
            xml_area_path, xml_dir, "*.xml"))
        # Loop each XML file and output XML file using xml_filter function
        for xml_file in xml_file_list:
            xml_filter(xml_file, os.path.join(output_path, xml_dir), size)


def xml_filter(xml_file_path, output_dir_path, size):
    """output XML files with boxes over the size from input XML files"""
    # load box labels
    label = load_voc_labeled_image(xml_file_path)

    # size filter
    dst_objects = []
    for obj in label.objects:
        area = obj.width * obj.height
        if area < size:
            continue
        dst_objects.append(obj)
    label.objects = dst_objects

    # output
    output_file_path = os.path.join(
        output_dir_path, os.path.basename(xml_file_path))
    with open(output_file_path, mode="w") as f:
        f.write(label.get_label_str())


if __name__ == "__main__":
    main()
