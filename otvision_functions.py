
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

# def _convert_detections_chunks(yolo_detections, names, det_config):
#     result = []
#     for no, yolo_detection in enumerate(yolo_detections):
#         data = {}
#         detection = []
#         for yolo_bbox in yolo_detection:
#             bbox = {
#                 "class": names[int(yolo_bbox[5])],
#                 "conf": yolo_bbox[4],
#                 "x": yolo_bbox[0],
#                 "y": yolo_bbox[1],
#                 "w": yolo_bbox[2],
#                 "h": yolo_bbox[3],
#             }
#             detection.append(bbox)
#         data[str(no + 1)] = {"classified": detection}
#         result.append({"det_config": det_config, "data": data})

#     return result

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
    infile_list = os.listdir(os.path.split(infile)[0])
    for i, t in enumerate(copy.deepcopy(infile_list)):
        infile_list[i] = os.path.split(infile)[0] + r"/" + t

    existing_files = get_files(infile_list, CONFIG["FILETYPES"]["DETECT"])
    if overwrite or not existing_files:
        print(existing_files)
        infile_path = Path(infile)
        outfile = str(infile_path.with_suffix(CONFIG["FILETYPES"]["DETECT"]))
        with open(outfile, "w") as f:
            json.dump(detections, f, indent=4)
        if existing_files:
            print("Detections file overwritten")
        else:
            print("Detections file saved")
    else:
        print("Detections file already exists, was not overwritten")

def get_files(paths, filetypes=None, replace_filetype=False, search_subdirs=True):
    """
    Generates a list of files ending with filename based on filenames or the
    (recursive) content of folders.

    Args:
        paths ([str or list of str or Path or list of Path]): where to find
        the files.
        filetype ([str]): ending of files to find. Preceding "_" prevents adding a '.'
            If no filetype is given, filetypes of file paths given are used and
            directories are ignored. Defaults to None.
        replace_filetype ([bool]): Wheter or not to replace the filetype in file paths
            with the filetype given. Currently only applied when one filetype was given.
            Defaults to False.
        search_subdirs ([bool]): Wheter or not to search subdirs of dirs given as paths.
            Defaults to True.

    Returns:
        [list]: [list of filenames as str]
    """
    files = set()

    # Check, if paths is a str or a list
    if type(paths) is str or isinstance(paths, Path):
        paths = [paths]
    elif type(paths) is not list and not isinstance(paths, Path):
        raise TypeError("Paths needs to be a str, a list of str, or Path object")
    
    # Check if filetypes is str or a list and transform it
    if filetypes:
        if type(filetypes) is not list:
            filetypes = [filetypes]

        for idx, filetype in enumerate(filetypes):
            if type(filetype) is not str:
                raise TypeError("Filetype needs to be a str or a list of str")

            if not filetype.startswith("_"):
                if not filetype.startswith("."):
                    filetype = "." + filetype
                filetypes[idx] = filetype.lower()
    # add all files to a single list _files_
    for path in paths:
        path = Path(path)
        # If path is a real file add it to return list
        if path.is_file():
            # Replace filetype in path if replace_filetype is given as argument
            # and path has suffix and only one filetype was given and new path exists
            if filetypes and replace_filetype and len(filetypes) == 1 and path.suffix:
                path_with_filetype_replaced = path.with_suffix(filetypes[0])
                if path_with_filetype_replaced.is_file():
                    path = path.with_suffix(filetypes[0])
            # Add path to list of returned paths if filetype meets requirements
            file = str(path)
            print(file)
            print(filetypes)
            if filetypes:
                for filetype in filetypes:
                    print(path.suffix.lower())
                    if path.suffix.lower() == filetype:
                        files.add(str(path))
            else:
                files.add(str(path))
        # If path is a real file add it to return list
        elif path.is_dir():
            for filetype in filetypes:
                for file in path.glob("**/*" if search_subdirs else "*"):
                    if file.is_file and file.suffix.lower() == filetype:
                        files.add(str(file))
        else:
            raise TypeError(
                "Paths needs to be a path as a pathlib.Path() or a str or a list of str"
            )

    return sorted(list(files))