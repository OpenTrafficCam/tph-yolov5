
from pathlib import Path
import json
from otvision_config import CONFIG
import os
import copy

def _print_overall_performance_stats(duration, det_fps):
    print("All Chunks done in {0:0.2f} s ({1:0.2f} fps)".format(duration, det_fps))

def _get_det_config(weights, conf, iou, size, chunksize, normalized):
    return {
        "detector": "YOLOv5",
        "weights": weights,
        "conf": conf,
        "iou": iou,
        "size": size,
        "chunksize": chunksize,
        "normalized": normalized,
    }

def _get_vidconfig(file, width, height, fps, frames):
    return {
        "file": str(Path(file).stem),
        "filetype": str(Path(file).suffix),
        "width": width,
        "height": height,
        "fps": fps,
        "frames": frames,
    }

def _convert_detections(yolo_detections, names, vid_config, det_config):
    data = {}
    for no, yolo_detection in enumerate(yolo_detections):
        # TODO: #81 Detections: Nested dict instead of dict of lists of dicts
        detection = []
        for yolo_bbox in yolo_detection:
            bbox = {
                "class": names[int(yolo_bbox[5])],
                "conf": yolo_bbox[4],
                "x": yolo_bbox[0],
                "y": yolo_bbox[1],
                "w": yolo_bbox[2],
                "h": yolo_bbox[3],
            }
            detection.append(bbox)
        data[str(no + 1)] = {"classified": detection}
    return {"vid_config": vid_config, "det_config": det_config, "data": data}

def save_detections(
    detections, infile, overwrite=CONFIG["DETECT"]["YOLO"]["OVERWRITE"]
): 
    filepath = os.path.dirname(infile) + "/" + os.path.splitext(os.path.basename(infile))[0] + CONFIG["FILETYPES"]["DETECT"]
    exists = os.path.isfile(filepath)
    if overwrite or not exists:
        infile_path = Path(infile)
        outfile = str(infile_path.with_suffix(CONFIG["FILETYPES"]["DETECT"]))
        with open(outfile, "w") as f:
            json.dump(detections, f, indent=4)
        if exists:
            print("Detections file (" + os.path.basename(filepath) + ") overwritten") 
        else:
            print("Detections as " + os.path.basename(filepath) + " saved")
    else:
        print(os.path.basename(infile)+" already exists, was not overwritten")