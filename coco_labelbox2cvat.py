""" 
Conversion of instance segmentation masks in LabelBox COCO 1.0 pickle format to CVAT COCO 1.0 json 
"""
__author__ = "Filip Drapejkowski"
__version__ = "1.0.0"

import argparse
import pickle
import json
from collections import defaultdict


def main(args):
    print("Reading from ", args.input_path)
    with open(args.input_path, "rb") as f:
        annotation_id = 0
        data_pkl = pickle.load(f)
        data = data_pkl['test']
        data.extend(data_pkl['train'])
        cvat_data=defaultdict(list)

        for i, _ in enumerate(data):
            data[i].pop('lablebox_metadata')
            data[i].pop('file_name')
            image = {
                "coco_url": "",
                "date_captured": 0,
                "file_name": data[i].pop("image_id") + ".jpg",
                "flickr_url": "",
                "id": i,
                "license": 0,
            }
            # ratios are not using data[i]["width or height"] due to wrong/inconsitent values.
            # areas are not computed, bbox are not rescaled, proper width/height are not saved because CVAT 
            # saves proper values during Dump annotations / Export Dataset operations
            width_ratio = 1.0 if "inputframesvideo" not in image["file_name"] else 1920/1279
            height_ratio = 1.0 if "inputframesvideo" not in image["file_name"] else 1080/604
            if args.verbose > 0:
                print(width_ratio, end=" ")
                print(height_ratio, end=" ")
            data[i]["annotations"] = data[i]["annotations"]
            for a, annotation in enumerate(data[i]["annotations"]):
                annotation.pop("bbox_mode")
                annotation["image_id"] = i
                annotation["iscrowd"] = 0
                annotation["category_id"]+=1 # indexing from 1, unfortunatelly
                annotation["attributes"] = { "occluded": False }
                annotation["area"] = 0.0
                annotation["id"] = annotation_id
                annotation["segmentation"] = [[val * width_ratio if i % 2 == 0 else val * height_ratio for i, val in enumerate(annotation["segmentation"][0])]]
                annotation_id +=1 
                cvat_data["annotations"].append(annotation)
            cvat_data["images"].append(image)
        cvat_data["categories"] = [
            {"id": 1, "name": "class_0", "supercategory": ""}, 
            {"id": 2, "name": "class_1", "supercategory": ""}
        ]

        with open(args.output_path, "w") as f_json:
            print("Saving to ", args.output_path)
            json.dump(cvat_data, f_json, indent=4, sort_keys=True)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Conversion of instance segmentation masks in LabelBox COCO 1.0 pickle format to CVAT COCO 1.0 json")
    parser.add_argument("--input_path", help="Pickle file in LabelBox format to be converted.", default="labelbox_coco.pkl")
    parser.add_argument("--output_path", help="Json file in CVAT format to be saved.", default="cvat_coco.json")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)

    args = parser.parse_args()
    main(args)