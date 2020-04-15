#-*-coding:utf-8-*-

import sys
import os
import csv
import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, ElementTree
import json

from xml.etree.ElementTree import dump


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s|%s| %s%% (%s/%s)  %s' % (prefix, bar, percent, iteration, total, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print("\n")

class VOC:
    """
    Handler Class for VOC PASCAL Format
    """

    def xml_indent(self, elem, level=0):
        i = "\n" + level * "\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.xml_indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def generate(self, data):
        try:

            xml_list = {}

            progress_length = len(data)
            progress_cnt = 0
            printProgressBar(0, progress_length, prefix='\nVOC Generate:'.ljust(15), suffix='Complete', length=40)

            for key in data:
                element = data[key]

                xml_annotation = Element("annotation")

                xml_size = Element("size")
                xml_width = Element("width")
                xml_width.text = element["size"]["width"]
                xml_size.append(xml_width)

                xml_height = Element("height")
                xml_height.text = element["size"]["height"]
                xml_size.append(xml_height)

                xml_depth = Element("depth")
                xml_depth.text = element["size"]["depth"]
                xml_size.append(xml_depth)

                xml_annotation.append(xml_size)

                xml_segmented = Element("segmented")
                xml_segmented.text = "0"

                xml_annotation.append(xml_segmented)

                if int(element["objects"]["num_obj"]) < 1:
                    return False, "number of Object less than 1"

                for i in range(0, int(element["objects"]["num_obj"])):

                    xml_object = Element("object")
                    obj_name = Element("name")
                    obj_name.text = element["objects"][str(i)]["name"]
                    xml_object.append(obj_name)

                    obj_pose = Element("pose")
                    obj_pose.text = "Unspecified"
                    xml_object.append(obj_pose)

                    obj_truncated = Element("truncated")
                    obj_truncated.text = "0"
                    xml_object.append(obj_truncated)

                    obj_difficult = Element("difficult")
                    obj_difficult.text = "0"
                    xml_object.append(obj_difficult)

                    xml_bndbox = Element("bndbox")

                    obj_xmin = Element("xmin")
                    obj_xmin.text = element["objects"][str(i)]["bndbox"]["xmin"]
                    xml_bndbox.append(obj_xmin)

                    obj_ymin = Element("ymin")
                    obj_ymin.text = element["objects"][str(i)]["bndbox"]["ymin"]
                    xml_bndbox.append(obj_ymin)

                    obj_xmax = Element("xmax")
                    obj_xmax.text = element["objects"][str(i)]["bndbox"]["xmax"]
                    xml_bndbox.append(obj_xmax)

                    obj_ymax = Element("ymax")
                    obj_ymax.text = element["objects"][str(i)]["bndbox"]["ymax"]
                    xml_bndbox.append(obj_ymax)
                    xml_object.append(xml_bndbox)

                    xml_annotation.append(xml_object)

                self.xml_indent(xml_annotation)

                xml_list[key.split(".")[0]] = xml_annotation

                printProgressBar(progress_cnt + 1, progress_length, prefix='VOC Generate:'.ljust(15), suffix='Complete', length=40)
                progress_cnt += 1

            return True, xml_list

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            msg = "ERROR : {}, moreInfo : {}\t{}\t{}".format(e, exc_type, fname, exc_tb.tb_lineno)

            return False, msg

    @staticmethod
    def save(xml_list, path):

        try:
            path = os.path.abspath(path)

            progress_length = len(xml_list)
            progress_cnt = 0
            printProgressBar(0, progress_length, prefix='\nVOC Save:'.ljust(10), suffix='Complete', length=40)

            for key in xml_list:
                xml = xml_list[key]
                filepath = os.path.join(path, "".join([key, ".xml"]))
                ElementTree(xml).write(filepath)

                printProgressBar(progress_cnt + 1, progress_length, prefix='VOC Save:'.ljust(15), suffix='Complete', length=40)
                progress_cnt += 1

            return True, None

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            msg = "ERROR : {}, moreInfo : {}\t{}\t{}".format(e, exc_type, fname, exc_tb.tb_lineno)

            return False, msg

    @staticmethod
    def parse(path):
        try:

            (dir_path, dir_names, filenames) = next(os.walk(os.path.abspath(path)))

            data = {}
            progress_length = len(filenames)
            progress_cnt = 0
            printProgressBar(0, progress_length, prefix='\nVOC Parsing:'.ljust(15), suffix='Complete', length=40)
            for filename in filenames:

                # print(dir_path)
                # print(dir_path)
                # print(filename)
                # print(filename)
                # print(filename)

               
                # xml = open(dir_path, filename, "r")

                xml = open(os.path.join(dir_path, filename), "r")
                
                
                tree = Et.parse(xml)
                root = tree.getroot()

                xml_size = root.find("size")
                size = {
                    "width": xml_size.find("width").text,
                    "height": xml_size.find("height").text,
                    "depth": xml_size.find("depth").text

                }

                objects = root.findall("object")
                if len(objects) == 0:
                    return False, "number object zero"

                obj = {
                    "num_obj": len(objects)
                }
    
                obj_index = 0
                for _object in objects:

                    tmp = {
                        "name": _object.find("name").text
                    }

                    xml_bndbox = _object.find("bndbox")
                    bndbox = {
                        "xmin": float(xml_bndbox.find("xmin").text),
                        "ymin": float(xml_bndbox.find("ymin").text),
                        "xmax": float(xml_bndbox.find("xmax").text),
                        "ymax": float(xml_bndbox.find("ymax").text)
                    }
                    tmp["bndbox"] = bndbox
                    obj[str(obj_index)] = tmp

                    obj_index += 1

                annotation = {
                    "size": size,
                    "objects": obj
                }

                filenameFIX = root.find("filename").text.split(".")[0] + "_" + root.find("filename").text.split(".")[1]

                data[filenameFIX] = annotation


                printProgressBar(progress_cnt + 1, progress_length, prefix='VOC Parsing:'.ljust(15), suffix='Complete', length=40)
                progress_cnt += 1

            return True, data

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            msg = "ERROR : {}, moreInfo : {}\t{}\t{}".format(e, exc_type, fname, exc_tb.tb_lineno)

            return False, msg



        try:

            progress_length = len(data)
            progress_cnt = 0
            printProgressBar(0, progress_length, prefix='\nYOLO Saving:'.ljust(15), suffix='Complete', length=40)

            with open(os.path.abspath(os.path.join(manipast_path, "manifast.txt")), "w") as manipast_file:

                for key in data:
                    manipast_file.write(os.path.abspath(os.path.join(img_path, "".join([key, img_type, "\n"]))))

                    with open(os.path.abspath(os.path.join(save_path, "".join([key, ".txt"]))), "w") as output_txt_file:
                        output_txt_file.write(data[key])


                    printProgressBar(progress_cnt + 1, progress_length, prefix='YOLO Saving:'.ljust(15),
                                     suffix='Complete',
                                     length=40)
                    progress_cnt += 1

            return True, None

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            msg = "ERROR : {}, moreInfo : {}\t{}\t{}".format(e, exc_type, fname, exc_tb.tb_lineno)

            return False, msg


class YOLO:
    """ 
    Handler Class for UDACITY Format
    """

    def __init__(self, cls_list_path):
        print(cls_list_path)

        with open(cls_list_path, 'r') as file:
            l = file.read().splitlines()

        self.cls_list = l


    def coordinateCvt2YOLO(self,size, box):
        dw = 1. / size[0]
        dh = 1. / size[1]

        # (xmin + xmax / 2)
        x = (box[0] + box[1]) / 2.0
        # (ymin + ymax / 2)
        y = (box[2] + box[3]) / 2.0

        # (xmax - xmin) = w
        w = box[1] - box[0]
        # (ymax - ymin) = h
        h = box[3] - box[2]

        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (round(x,3), round(y,3), round(w,3), round(h,3))

    def parse(self, label_path, img_path, img_type=".png"):
        try:

            (dir_path, dir_names, filenames) = next(os.walk(os.path.abspath(label_path)))

            data = {}

            progress_length = len(filenames)
            progress_cnt = 0
            printProgressBar(0, progress_length, prefix='\nYOLO Parsing:'.ljust(15), suffix='Complete', length=40)

            for filename in filenames:

                txt = open(os.path.join(dir_path, filename), "r")

                filename = filename.split(".")[0]

                img = Image.open(os.path.join(img_path, "".join([filename, img_type])))
                img_width = str(img.size[0])
                img_height = str(img.size[1])
                img_depth = 3

                size = {
                    "width": img_width,
                    "height": img_height,
                    "depth": img_depth
                }

                obj = {}
                obj_cnt = 0

                for line in txt:
                    elements = line.split(" ")
                    name_id = elements[0]

                    xminAddxmax = float(elements[1]) * (2.0 * float(img_width))
                    yminAddymax = float(elements[2]) * (2.0 * float(img_height))

                    w = float(elements[3]) * float(img_width)
                    h = float(elements[4]) * float(img_height)

                    xmin = (xminAddxmax - w) / 2
                    ymin = (yminAddymax - h) / 2
                    xmax = xmin + w
                    ymax = ymin + h

                    bndbox = {
                        "xmin": float(xmin),
                        "ymin": float(ymin),
                        "xmax": float(xmax),
                        "ymax": float(ymax)
                    }


                    obj_info = {
                        "name": name_id,
                        "bndbox": bndbox
                    }

                    obj[str(obj_cnt)] =obj_info
                    obj_cnt += 1

                obj["num_obj"] =  obj_cnt

                data[filename] = {
                    "size": size,
                    "objects": obj
                }

                printProgressBar(progress_cnt + 1, progress_length, prefix='YOLO Parsing:'.ljust(15), suffix='Complete',
                                 length=40)
                progress_cnt += 1

            return True, data

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            msg = "ERROR : {}, moreInfo : {}\t{}\t{}".format(e, exc_type, fname, exc_tb.tb_lineno)

            return False, msg

    def generate(self, data):

        try:

            progress_length =len(data)
            progress_cnt = 0
            printProgressBar(0, progress_length, prefix='\nYOLO Generating:'.ljust(15), suffix='Complete', length=40)

            result = {}

            for key in data:
                img_width = int(data[key]["size"]["width"])
                img_height = int(data[key]["size"]["height"])

                contents = ""

                for idx in range(0, int(data[key]["objects"]["num_obj"])):

                    xmin = data[key]["objects"][str(idx)]["bndbox"]["xmin"]
                    ymin = data[key]["objects"][str(idx)]["bndbox"]["ymin"]
                    xmax = data[key]["objects"][str(idx)]["bndbox"]["xmax"]
                    ymax = data[key]["objects"][str(idx)]["bndbox"]["ymax"]

                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = self.coordinateCvt2YOLO((img_width, img_height), b)

                    cls_id = self.cls_list.index(data[key]["objects"][str(idx)]["name"])

                    bndbox = "".join(["".join([str(e), " "]) for e in bb])
                    contents = "".join([contents, str(cls_id), " ", bndbox[:-1], "\n"])

                result[key] = contents

                printProgressBar(progress_cnt + 1, progress_length, prefix='YOLO Generating:'.ljust(15),
                                 suffix='Complete',
                                 length=40)
                progress_cnt += 1

            return True, result

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            msg = "ERROR : {}, moreInfo : {}\t{}\t{}".format(e, exc_type, fname, exc_tb.tb_lineno)

            return False, msg

    def save(self, data, save_path, img_path, img_type, manipast_path):

        try:

            progress_length = len(data)
            progress_cnt = 0
            printProgressBar(0, progress_length, prefix='\nYOLO Saving:'.ljust(15), suffix='Complete', length=40)

            with open(os.path.abspath(os.path.join(manipast_path, "manifast.txt")), "w") as manipast_file:

                for key in data:
                    manipast_file.write(os.path.abspath(os.path.join(img_path, "".join([key, img_type, "\n"]))))

                    with open(os.path.abspath(os.path.join(save_path, "".join([key, ".txt"]))), "w") as output_txt_file:
                        output_txt_file.write(data[key])


                    printProgressBar(progress_cnt + 1, progress_length, prefix='YOLO Saving:'.ljust(15),
                                     suffix='Complete',
                                     length=40)
                    progress_cnt += 1

            return True, None

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            msg = "ERROR : {}, moreInfo : {}\t{}\t{}".format(e, exc_type, fname, exc_tb.tb_lineno)

            return False, msg