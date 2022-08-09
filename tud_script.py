from re import A

from matplotlib import projections
import detect
from utils.general import check_requirements
check_requirements(exclude=('tensorboard', 'thop'))
source = r"C:\Users\Kollascheck\Desktop\Test Cut und OTC\test_tph-yolov5\kleine Videodatei"
tu_dict ={
    "weights" : r"\\vs-grp08.zih.tu-dresden.de\otc_live\models\YoloV5\drone\tph-yolov5\yolov5l-xs-1.pt",
    "source" : source,
    "save_txt" : False, # single txt file for every image
    "save_conf" : True,
    "project" : source,
    "name" : None, #subfolder ;None --> no extra folder 
    # "export_of_tph-yolov5l-xs-1"
    "device" : "",
    "nosave" : True, # video with bboxes
    "normalize_output" : False, # odet xywh output
    "exist_ok": True
}

detect.run(**tu_dict)