###
'''Created by: Piyush Kumar'''
'''Last Modified Date:- 23-Nov-2020'''
###

#####################Object Detection Code##################################

import numpy as np
import os
import tensorflow as tf
from PIL import Image
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import pathlib

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

def load_model(model_name):
  base_url = 'http://download.tensorflow.org/models/object_detection/'
  model_file = model_name + '.tar.gz'
  model_dir = tf.keras.utils.get_file(
    fname=model_name, 
    origin=base_url + model_file,
    untar=True)

  model_dir = pathlib.Path(model_dir)/"saved_model"

  model = tf.saved_model.load(str(model_dir))
  model = model.signatures['serving_default']

  return model

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = '/home/piyush/models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

def run_inference_for_single_image(model, image):
  image = np.asarray(image)
  # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
  input_tensor = tf.convert_to_tensor(image)
  # The model expects a batch of images, so add an axis with `tf.newaxis`.
  input_tensor = input_tensor[tf.newaxis,...]

  # Run inference
  output_dict = model(input_tensor)

  # All outputs are batches tensors.
  # Convert to numpy arrays, and take index [0] to remove the batch dimension.
  # We're only interested in the first num_detections.
  num_detections = int(output_dict.pop('num_detections'))
  output_dict = {key:value[0, :num_detections].numpy() 
                 for key,value in output_dict.items()}
  output_dict['num_detections'] = num_detections

  # detection_classes should be ints.
  output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
  # Handle models with masks:
  if 'detection_masks' in output_dict:
    # Reframe the the bbox mask to the image size.
    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
              output_dict['detection_masks'], output_dict['detection_boxes'],
               image.shape[0], image.shape[1])      
    detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                       tf.uint8)
    output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    
  return output_dict

def show_inference(model, image_path, thres, file_name):
  # the array based representation of the image will be used later in order to prepare the
  # result image with boxes and labels on it.
  
  image_np = np.array(Image.open(image_path))
  # Actual detection.
  output_dict = run_inference_for_single_image(model, image_np)
  # Visualization of the results of a detection.
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks_reframed', None),
      use_normalized_coordinates=True,
      min_score_thresh=thres,
      line_thickness=4)

  im = Image.fromarray(image_np)
  im.save('/home/piyush/Detected_image/detected.jpg')
  print('file saved')

############################################################################

######################GUI Code##############################################
  
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os
import time
from PIL import Image
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import threading


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("border-color: rgb(243, 243, 243);")
        #MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        #MainWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        #MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.warning_label = QtWidgets.QLabel(self.centralwidget)
        self.warning_label.setGeometry(QtCore.QRect(150, 30, 411, 21))
        self.warning_label.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"font: italic 11pt \"Padauk\";\n"
"color: rgb(239, 41, 41);")
        self.warning_label.setText("")
        self.warning_label.setObjectName("warning_label")
        
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(230, 500, 261, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.select_folder = QtWidgets.QPushButton(self.centralwidget)
        self.select_folder.setGeometry(QtCore.QRect(10, 100, 121, 61))
        self.select_folder.setObjectName("open_folder")
        self.previous_image = QtWidgets.QPushButton(self.centralwidget)
        self.previous_image.setGeometry(QtCore.QRect(10, 300, 121, 61))
        self.previous_image.setObjectName("previous_image")
        self.save_annotation = QtWidgets.QPushButton(self.centralwidget)
        self.save_annotation.setGeometry(QtCore.QRect(10, 410, 121, 61))
        self.save_annotation.setObjectName("save_annotation")
        self.detect = QtWidgets.QPushButton(self.centralwidget)
        self.detect.setGeometry(QtCore.QRect(590, 250, 101, 61))
        self.detect.setObjectName("detect")
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(590, 350, 101, 61))
        self.reset.setObjectName("reset")
        self.expand = QtWidgets.QPushButton(self.centralwidget)
        self.expand.setGeometry(QtCore.QRect(492, 462, 80, 25))
        self.expand.setObjectName("expand")
        self.open_image = QtWidgets.QLabel(self.centralwidget)
        self.open_image.setGeometry(QtCore.QRect(150, 110, 421, 351))
        self.open_image.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.open_image.setText("")
        self.open_image.setObjectName("open_image")
        self.next_image = QtWidgets.QPushButton(self.centralwidget)
        self.next_image.setGeometry(QtCore.QRect(10, 200, 121, 61))
        self.next_image.setObjectName("next_image")
        self.select_model_label = QtWidgets.QLabel(self.centralwidget)
        self.select_model_label.setGeometry(QtCore.QRect(590, 30, 91, 31))
        self.select_model_label.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"border-color: rgb(46, 52, 54);")
        self.select_model_label.setObjectName("select_model_label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(590, 70, 161, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frcnn = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.frcnn.setObjectName("frcnn")
        self.verticalLayout.addWidget(self.frcnn)
        '''self.mobilenet = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.mobilenet.setObjectName("mobilenet")
        self.verticalLayout.addWidget(self.mobilenet)'''
        self.ssd = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ssd.setObjectName("ssd")
        self.verticalLayout.addWidget(self.ssd)
        self.detection_threshold_label = QtWidgets.QLabel(self.centralwidget)
        self.detection_threshold_label.setGeometry(QtCore.QRect(590, 190, 141, 31))
        self.detection_threshold_label.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.detection_threshold_label.setObjectName("detection_threshold_label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(740, 190, 51, 31))
        self.textEdit.setObjectName("textEdit")
        '''self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(590, 270, 181, 191))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.person = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.person.setObjectName("person")
        self.verticalLayout_2.addWidget(self.person)
        self.cat = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.cat.setObjectName("cat")
        self.verticalLayout_2.addWidget(self.cat)
        self.dog = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.dog.setObjectName("dog")
        self.verticalLayout_2.addWidget(self.dog)
        self.Bottle = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.Bottle.setObjectName("Bottle")
        self.verticalLayout_2.addWidget(self.Bottle)
        self.chair = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.chair.setObjectName("chair")
        self.verticalLayout_2.addWidget(self.chair)
        self.label_filter_label = QtWidgets.QLabel(self.centralwidget)
        self.label_filter_label.setGeometry(QtCore.QRect(590, 236, 91, 31))
        self.label_filter_label.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.label_filter_label.setObjectName("label_filter_label")'''
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.path = ""
        self.files = []
        self.counter = 0
        self.flag = False
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        
        self.select_folder.setText(_translate("MainWindow", "Select Folder"))
        self.select_folder.clicked.connect(self.open_folder_handler)
        
        self.previous_image.setText(_translate("MainWindow", "Previous Image"))
        self.previous_image.clicked.connect(self.previous_image_handler)
        
        self.save_annotation.setText(_translate("MainWindow", "Save Annotation"))
        
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.reset.setEnabled(False)
        self.reset.clicked.connect(self.reset_handler)
        
        self.expand.setText(_translate("MainWindow", "Expand"))
        self.expand.setEnabled(False)
        self.expand.clicked.connect(self.expand_handler)
        
        self.detect.setText(_translate("MainWindow", "Detect"))
        self.detect.clicked.connect(self.detect_handler)
        
        self.next_image.setText(_translate("MainWindow", "Next Image"))
        self.next_image.clicked.connect(self.next_image_handler)
        
        self.select_model_label.setText(_translate("MainWindow", "Select Model"))
        
        self.frcnn.setText(_translate("MainWindow", "FRCNN"))
        self.frcnn.clicked.connect(self.frcnn_click_handler)
        
        '''self.mobilenet.setText(_translate("MainWindow", "Mobilenet"))
        self.mobilenet.setChecked(True)
        self.mobilenet.clicked.connect(self.mobilenet_click_handler)'''
        
        self.ssd.setText(_translate("MainWindow", "SSD"))
        self.ssd.setChecked(True)
        self.ssd.clicked.connect(self.ssd_click_handler)
        
        self.detection_threshold_label.setText(_translate("MainWindow", "Detection Threshold"))
        
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.7</p></body></html>"))
        '''self.person.setText(_translate("MainWindow", "Person"))
        self.cat.setText(_translate("MainWindow", "Cat"))
        self.dog.setText(_translate("MainWindow", "Dog"))
        self.Bottle.setText(_translate("MainWindow", "Bottle"))
        self.chair.setText(_translate("MainWindow", "Chair"))
        self.label_filter_label.setText(_translate("MainWindow", "Label Filter"))'''
        
        
    def show_image(self):
        Image.open(self.path+'/'+self.files[self.counter]).resize((421,351)).save('size.jpg')
        self.im = QPixmap('size.jpg')
        self.open_image.setPixmap(self.im)
    
    def run_progressBar(self):
        count = 0
        turn = 0
        start = time.perf_counter()
        while(self.flag==True):
            if(turn==0):
                self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.progressBar.setValue(count)
                count+=0.25
                if(count>100):
                    turn = 1
            elif(turn==1):
                self.progressBar.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.progressBar.setValue(count)
                count-=0.25
                if(count==0):
                    turn=0
            
            time.sleep(0.005)
        finish = time.perf_counter()
        return(finish-start)
        
    def open_folder_handler(self):
        self.open_dialog_box()
    
    def open_dialog_box(self):
        self.counter=0
        filename = QFileDialog.getOpenFileName()
        self.path = filename[0]
        location = self.path.rfind('/')
        self.path = self.path[0:location]
        self.files = [i for i in os.listdir(self.path) if i.endswith('.jpg')]
        self.show_image()
        
    def next_image_handler(self):
        self.counter+=1
        if(self.counter>=len(self.files)):
            self.counter = len(self.files)-1
        self.show_image()
    
    def reset_handler(self):
        self.show_image()
        self.reset.setEnabled(False)
        
    def previous_image_handler(self):
        self.counter-=1
        if(self.counter<0):
            self.counter=0
        self.show_image()
    
    def detect_handler(self):
        self.detect_thread()
    
    def detect_thread(self):
        #self.thread = QThread()
        #self.thread.started.connect(self.detecting_object)
        #self.thread.start()
        #th = threading.Thread(target = self.detecting_object)
        #th.start()
        #self.run_progressBar()
        self.flag=True
        import concurrent.futures as cf
        with cf.ThreadPoolExecutor() as executer:
            p1 = executer.submit(self.detecting_object)
            p2 = executer.submit(self.run_progressBar)
            print(p1.result())
            print(p2.result())
        
        
    def detecting_object(self):
        print(self)
        self.warning_label.setText(".................Please Wait.................Please Wait.................Please Wait.................")
        #self.flag = True
        #self.progress = QtWidgets.QProgressDialog('Detecting Please Wait!!','Cancel',0,100)
        #self.progress.show()
        #self.progress.show()
        #threading.Thread(Process(target = self.run_progressBar).start())
        thres = float(self.textEdit.toPlainText())
        model_name = ''
        if(self.frcnn.isChecked()):
            model_name = 'faster_rcnn_inception_v2_coco_2018_01_28'
        elif(self.ssd.isChecked()):
            model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
        else:
            self.warning_label.setText("Please select a model")
        
        if(model_name!=''):thres = float(self.textEdit.toPlainText())
        model_name = ''
        if(self.frcnn.isChecked()):
            model_name = 'faster_rcnn_inception_v2_coco_2018_01_28'
        elif(self.ssd.isChecked()):
            model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
        else:
            self.warning_label.setText("Please select a model")
        
        if(model_name!=''):
            detection_model = load_model(model_name)
            image_path = self.path+'/'+self.files[self.counter]
            show_inference(detection_model,image_path,thres,self.files[self.counter])
            Image.open('/home/piyush/Detected_image/detected.jpg').resize((421,351)).save('size.jpg')
            self.im = QPixmap('size.jpg')
            self.open_image.setPixmap(self.im)
        self.flag = False
        self.progressBar.setValue(0)
        self.warning_label.setText("")
        self.reset.setEnabled(True)
        self.expand.setEnabled(True)
        return 'done'
        #self.progress.hide()
            
    def expand_handler(self):
        filepath = '/home/piyush/Detected_image/detected.jpg'
        import subprocess, os, platform
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
        self.expand.setEnabled(False)
    
    def frcnn_click_handler(self):
        if(self.frcnn.isChecked()):
            #self.mobilenet.setChecked(False)
            self.warning_label.setText("")
            self.ssd.setChecked(False)
        
    '''def mobilenet_click_handler(self):self.MainWindow
        if(self.mobilenet.isChecked()):
            self.frcnn.setChecked(False)
            self.ssd.setChecked(False)'''
        
    def ssd_click_handler(self):
        if(self.ssd.isChecked()):
            #self.mobilenet.setChecked(False)
            self.warning_label.setText("")
            self.frcnn.setChecked(False)
            
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Form)
    Form.show()
    P = Process(target = sys.exit, args = (app.exec_()))
    P.start()
    P.join()
    #sys.exit(app.exec_())
