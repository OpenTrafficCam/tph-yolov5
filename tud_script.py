from re import A

from matplotlib import projections
import detect

detect.check_requirements(exclude=('tensorboard', 'thop'))

weights = r"yolov5l-xs-1.pt"
source = r"D:\Testvideos\TKV\Testauswertung\raw"
save_txt = True
save_conf = True
project = source
subfolder = "tph-yolov5l-xs-1"
detect.run(weights=weights, source=source, project=source, name=subfolder, save_txt=True, save_conf=True)