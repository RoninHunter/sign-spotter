#-*-coding:utf-8-*-

import os
import pathlib
import shutil
from xml.etree.ElementTree import dump
import json
import pprint

import argparse


from formatDarkFiles.py import VOC, YOLO


parser = argparse.ArgumentParser(description='label Converting example.')
parser.add_argument('--datasets',               type=str, help='type of datasets')
parser.add_argument('--img_path',               type=str, help='directory of image folder')
parser.add_argument('--label',                  type=str, help='directory of label folder or label file path')
parser.add_argument('--convert_output_path',    type=str, help='directory of label folder')
parser.add_argument('--img_type',               type=str, help='type of image')
parser.add_argument('--manipast_path',          type=str, help='directory of manipast file', default="./")
parser.add_argument('--cls_list_file',          type=str, help='directory of *.names file', default="./")

args = parser.parse_args()


def main(config):



    if config["datasets"] == "VOC":

        voc = VOC()

        yolo = YOLO(config["cls_list"])

        flag, data = voc.parse(config["label"])

        if flag == True:

            flag, data = yolo.generate(data)
            if flag == True:
                flag, data = yolo.save(data, config["output_path"], config["img_path"] ,
                                       config["img_type"], config["manipast_path"])

                if flag == False:
                    print("Saving Result : {}, msg : {}".format(flag, data))

            else:
                print("YOLO Generating Result : {}, msg : {}".format(flag, data))


        else:
            print("VOC Parsing Result : {}, msg : {}".format(flag, data))

    else:
        print("Unkwon Datasets")

if __name__ == '__main__':


    config ={
        "datasets":         args.datasets,
        "img_path":         args.img_path,
        "label":            args.label,
        "img_type":         args.img_type,
        "manipast_path":    args.manipast_path,
        "output_path":      args.convert_output_path,
        "cls_list":         args.cls_list_file,
    }



    main(config)

    # Example command usage below
    # python3 example.py --datasets VOC --img_path <image_path> --label <label path or annotation file> --convert_output_path <output path> --img_type [".jpg" / ".png"] --manipast_path <output manipast file path> --cls_list_file <*.names file path>
