from re import A

from matplotlib import projections
import detect
from utils.general import check_requirements
check_requirements(exclude=('tensorboard', 'thop'))

weights = r"\\vs-grp08.zih.tu-dresden.de\otc_live\models\YoloV5\drone\tph-yolov5\yolov5l-xs-1.pt"
source = r"C:\Users\Kollascheck\Desktop\Test Cut und OTC\test_tph-yolov5"
save_txt = True
save_conf = True
project = source
subfolder = "tph-yolov5l-xs-1"
detect.run(weights=weights, source=source, project=source, name=subfolder, save_txt=True, save_conf=True)