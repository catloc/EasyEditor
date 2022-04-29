from os import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter

app = QApplication ([])
main_window = QWidget()
main_window.resize(700, 500)
main_window.setWindowTitle('Easy Editor')
ib_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

row = QHBoxLayout()
row2 = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
 
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

row2.addWidget(btn_left)
row2.addWidget(btn_right)
row2.addWidget(btn_mirror)
row2.addWidget(btn_sharp)
row2.addWidget(btn_bw)

col2.addWidget(ib_image)
col2.addLayout(row2)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
main_window.setLayout(row)

main_window.show()

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = path.join(dir, filename)
        self.image = Image.open(image_path)


    def showImage(self, path):
        ib_image.hide()
        pixmapimage = QPixmap(path)
        w, h = ib_image.width(), ib_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        ib_image.setPixmap(pixmapimage)
        ib_image.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        pathk = path.join(self.dir, self.save_dir)
        if not(path.exists(pathk) or path.isdir(pathk)):
            mkdir(pathk)
        image_path = path.join(pathk, self.filename)
        self.image.save(image_path)

    def do_flip(self):
        self.image =  self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image =  self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image =  self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.image =  self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharp)

app.exec_()