# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clone_geometry_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CloneGeometryDialogBase(object):
    def setupUi(self, CloneGeometryDialogBase):
        CloneGeometryDialogBase.setObjectName("CloneGeometryDialogBase")
        CloneGeometryDialogBase.resize(370, 279)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CloneGeometryDialogBase.sizePolicy().hasHeightForWidth())
        CloneGeometryDialogBase.setSizePolicy(sizePolicy)
        CloneGeometryDialogBase.setMinimumSize(QtCore.QSize(0, 0))
        CloneGeometryDialogBase.setMaximumSize(QtCore.QSize(570, 320))
        CloneGeometryDialogBase.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(CloneGeometryDialogBase)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(CloneGeometryDialogBase)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(CloneGeometryDialogBase)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(CloneGeometryDialogBase)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(CloneGeometryDialogBase)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(CloneGeometryDialogBase)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.groupBox = QtWidgets.QGroupBox(CloneGeometryDialogBase)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.radioToMemory = QtWidgets.QRadioButton(self.groupBox)
        self.radioToMemory.setChecked(True)
        self.radioToMemory.setObjectName("radioToMemory")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.radioToMemory)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setStatusTip("")
        self.lineEdit_2.setWhatsThis("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.checkBoxAtrib = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxAtrib.setChecked(True)
        self.checkBoxAtrib.setObjectName("checkBoxAtrib")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBoxAtrib)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_mask = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_mask.setObjectName("checkBox_mask")
        self.horizontalLayout_2.addWidget(self.checkBox_mask)
        self.maskColor = QgsColorButton(self.groupBox)
        self.maskColor.setObjectName("maskColor")
        self.horizontalLayout_2.addWidget(self.maskColor)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.line_2 = QtWidgets.QFrame(self.groupBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioToLayer = QtWidgets.QRadioButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioToLayer.sizePolicy().hasHeightForWidth())
        self.radioToLayer.setSizePolicy(sizePolicy)
        self.radioToLayer.setObjectName("radioToLayer")
        self.horizontalLayout_3.addWidget(self.radioToLayer)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_about = QtWidgets.QPushButton(CloneGeometryDialogBase)
        self.pushButton_about.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButton_about.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/_PrintTools/comp_print/icons/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_about.setIcon(icon)
        self.pushButton_about.setObjectName("pushButton_about")
        self.horizontalLayout_4.addWidget(self.pushButton_about)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.button_box = QtWidgets.QDialogButtonBox(CloneGeometryDialogBase)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout_4.addWidget(self.button_box)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.label_8 = QtWidgets.QLabel(CloneGeometryDialogBase)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)

        self.retranslateUi(CloneGeometryDialogBase)
        self.button_box.accepted.connect(CloneGeometryDialogBase.accept)
        self.button_box.rejected.connect(CloneGeometryDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(CloneGeometryDialogBase)

    def retranslateUi(self, CloneGeometryDialogBase):
        _translate = QtCore.QCoreApplication.translate
        CloneGeometryDialogBase.setWindowTitle(_translate("CloneGeometryDialogBase", "Клонирование геометрии"))
        self.label.setText(_translate("CloneGeometryDialogBase", "Слой-источник:"))
        self.label_2.setText(_translate("CloneGeometryDialogBase", "Количество выделенных объектов: "))
        self.label_3.setText(_translate("CloneGeometryDialogBase", "-"))
        self.groupBox.setTitle(_translate("CloneGeometryDialogBase", "Сохранить геометрию в..."))
        self.radioToMemory.setText(_translate("CloneGeometryDialogBase", "Во временный слой"))
        self.lineEdit_2.setPlaceholderText(_translate("CloneGeometryDialogBase", "Название (при необходимости)"))
        self.checkBoxAtrib.setText(_translate("CloneGeometryDialogBase", "Копировать атрибуты"))
        self.checkBox_mask.setText(_translate("CloneGeometryDialogBase", "Только обводка"))
        self.radioToLayer.setText(_translate("CloneGeometryDialogBase", "В существующий слой"))
        self.pushButton_about.setToolTip(_translate("CloneGeometryDialogBase", "О программе..."))
        self.label_8.setText(_translate("CloneGeometryDialogBase", "<html><head/><body><p><span style=\" color:#828282;\">МКУ ЦИКТ - ГО &quot;Город Калининград&quot;</span></p></body></html>"))

from qgscolorbutton import QgsColorButton
