# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CloneGeometry
                                 A QGIS plugin
 Clone features to memory or other vector layer.
                              -------------------
        begin                : 2015-08-05
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Zlatanov Evgeniy
        email                : johnzet@yandex.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QObject, QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant, QSize
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QDialogButtonBox, QColorDialog, QAction, QDialog
from qgis.core import  (
                        edit,
                        Qgis,
                        QgsFeature,
                        QgsGeometry,
                        QgsMapLayer,
                        QgsSpatialIndex,
                        QgsFeatureRequest,
                        QgsVectorLayer,
                        QgsField,
                        QgsProject,
                        QgsSimpleLineSymbolLayer,
                        QgsSimpleMarkerSymbolLayer,
                        QgsWkbTypes,
                        QgsRenderContext,
                        QgsVectorLayerUtils
                        )
# Initialize Qt resources from file resources.py
from .resources_rc import *
# Import the code for the dialog
from .clone_geometry_dialog import CloneGeometryDialog
import os.path
import locale

from PyQt5 import QtCore, QtGui
from .about_ui import Ui_Dialog as AboutDialog

class AbtDialog(QDialog):
    def __init__(self):

        super(AbtDialog, self).__init__()
        self.about_ui = AboutDialog()
        self.about_ui.setupUi(self)

        self.plugin_dir = os.path.dirname(__file__)

        self.about_ui.label_6.setPixmap(QtGui.QPixmap(':/plugins/CloneGeometry/icon.png').scaled(QSize(64, 64)))
        self.about_ui.label_6.setScaledContents(False)
        self.about_ui.label_version.setText('2020.0507')
        self.about_ui.label_4.setText('Златанов Евгений')
        self.about_ui.label.setText('CloneFeatures')
        self.about_ui.textBrowser.setText('2015-2020. Клонирование объектов в существующий слой или новый временный слой. ')


class CloneGeometry:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CloneGeometry_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.colorValues = [
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#000000",
            "#800000", "#008000", "#000080", "#808000", "#800080", "#008080", "#808080",
            "#C00000", "#00C000", "#0000C0", "#C0C000", "#C000C0", "#00C0C0", "#C0C0C0",
            "#400000", "#004000", "#000040", "#404000", "#400040", "#004040", "#404040",
            "#200000", "#002000", "#000020", "#202000", "#200020", "#002020", "#202020",
            "#600000", "#006000", "#000060", "#606000", "#600060", "#006060", "#606060",
            "#A00000", "#00A000", "#0000A0", "#A0A000", "#A000A0", "#00A0A0", "#A0A0A0",
            "#E00000", "#00E000", "#0000E0", "#E0E000", "#E000E0", "#00E0E0", "#E0E0E0"
        ]
        self.colorIndex = 0
        self.mColor = QColor(0,85,255,255) #default color border

        self.dlg = CloneGeometryDialog()
        # self.dlg.maskColor.clicked.connect(self.color_picker)
        self.dlg.checkBox_mask.clicked.connect(self.colorState)
        self.buttonOk = self.dlg.button_box.button( QDialogButtonBox.Ok )
        self.dlg.radioToMemory.clicked.connect(self.checktolayer)
        self.dlg.radioToLayer.clicked.connect(self.checktolayer)
        self.dlg.comboBox.currentIndexChanged.connect(self.checktolayer)
        self.buttonOk.clicked.connect(self.cloneGeometry)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Clone geometry')

        # about button
        self.ui_about = AbtDialog()
        self.dlg.pushButton_about.setIcon(QIcon(':/plugins/CloneGeometry/about.png'))
        self.dlg.pushButton_about.clicked.connect(self.show_about)


    # about button
    def show_about(self):
        self.ui_about.setWindowFlags(self.ui_about.windowFlags() | Qt.WindowStaysOnTopHint | Qt.WindowMinMaxButtonsHint)
        self.ui_about.show()
        # TODO: We are going to let the user set this up in a future iteration


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CloneGeometry', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.iface.digitizeToolBar().addAction(action)
        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action


    def initGui(self):

        self.clone_action = QAction(
            QIcon(':/plugins/CloneGeometry/icon.png'),
            u"Клонировать границы в другой слой...", self.iface.mainWindow())
            
        self.clone_action.triggered.connect(self.run)
        self.iface.digitizeToolBar().addAction(self.clone_action)
        self.iface.addPluginToVectorMenu(u"&Клонирование геометрии", self.clone_action)
        self.iface.mapCanvas().currentLayerChanged.connect(self.check_buttons_state)
        
        self.check_buttons_state(None)
        self.colorState()
 

    def unload(self):

        self.iface.unregisterMainWindowAction(self.clone_action)
        self.iface.removePluginVectorMenu(u"&Клонирование геометрии", self.clone_action)
        self.iface.digitizeToolBar().removeAction(self.clone_action)
        self.iface.mapCanvas().currentLayerChanged.disconnect(self.check_buttons_state)

        self.dlg.checkBox_mask.clicked.disconnect(self.colorState)
        self.dlg.radioToMemory.clicked.disconnect(self.checktolayer)
        self.dlg.radioToLayer.clicked.disconnect(self.checktolayer)
        self.dlg.comboBox.currentIndexChanged.disconnect(self.checktolayer)
        self.buttonOk.clicked.disconnect(self.cloneGeometry)


    def colorState(self):
        if self.dlg.checkBox_mask.isChecked() and self.dlg.checkBox_mask.isEnabled():
            self.dlg.maskColor.setEnabled(True)
        else:
            self.dlg.maskColor.setEnabled(False)


    def check_buttons_state(self, layer=None):
        layer = self.iface.activeLayer()
        if not isinstance( layer, QgsVectorLayer):
            self.clone_action.setDisabled(True)
            return
        if layer is not None:
            layer.selectionChanged.connect(self.on_current_layer_selection_changed)
            self.on_current_layer_selection_changed()

        
    def on_current_layer_selection_changed(self):

        layer = self.iface.activeLayer()
        if layer is not None:
            sel_feat_count =  layer.selectedFeatureCount()
            if sel_feat_count < 1:
                self.clone_action.setDisabled(True)
                return
            if sel_feat_count > 0:
                self.clone_action.setEnabled(True)
                return
            self.clone_action.setEnabled(True)


    def checktolayer( self ):
        self.buttonOk.setEnabled(True)

        if self.dlg.radioToMemory.isChecked():
            self.dlg.checkBoxAtrib.setEnabled(True)
            self.dlg.checkBox_mask.setEnabled(True)
            self.colorState()
            # self.dlg.maskColor.setEnabled(True)
            self.dlg.lineEdit_2.setEnabled(True)
            self.dlg.comboBox.setEnabled(False)
        elif self.dlg.radioToLayer.isChecked():
            self.dlg.checkBoxAtrib.setEnabled(False)
            self.dlg.checkBox_mask.setEnabled(False)
            self.colorState()
            # self.dlg.maskColor.setEnabled(False)
            self.dlg.lineEdit_2.setEnabled(False)
            self.dlg.comboBox.setEnabled(True)
            if self.dlg.comboBox.currentIndex() == -1:
                self.buttonOk.setEnabled(False)

    def populateLayers( self ):
        myListB = []
        self.dlg.comboBox.clear()
        myListB = self.getLayerNames()
        self.dlg.comboBox.addItems( myListB )

    def getLayerNames( self ):
        layermap = QgsProject.instance().mapLayers()
        layerlist = []
        for name, layer in layermap.items():
            if layer.type() == QgsMapLayer.VectorLayer:
                if not layer.readOnly():
                    if layer.providerType() not in ('oracle'):
                        if layer.geometryType() == self.iface.mapCanvas().currentLayer().geometryType():
                            layerlist.append( layer.name())
        return sorted( layerlist)

    def getVectorLayerByName( self, myName ):
        layermap = QgsProject.instance().mapLayers()
        for name, layer in layermap.items():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None
                    
    def countVectorLayerByName(self, myName):
        layermap = QgsProject.instance().mapLayers()
        cnt = 0
        maxcnt = 1
        for name, layer in layermap.items():
            if layer.type() == QgsMapLayer.VectorLayer and (layer.name()[:-2] == myName or layer.name()[:-3] == myName or layer.name() == myName):
                if layer.isValid():
                    cnt = cnt + 1
                    try:
                        curcnt = int(layer.name()[len(myName):].strip())
                        if curcnt > maxcnt:
                            maxcnt = curcnt
                    except:
                        continue
        if cnt > 0:
            cnt = maxcnt+1
        return cnt

    def setStyleLayer( self, layer ):
        if self.dlg.checkBox_mask.isChecked(): # only border
            if layer.geometryType()==QgsWkbTypes.PolygonGeometry  or layer.geometryType()==QgsWkbTypes.LineGeometry :
                properties = {'color': self.mColor.name(), 'outline_width': '0.6'}
                symbol_layer = QgsSimpleLineSymbolLayer.create(properties)
                layer.renderer().symbols(QgsRenderContext())[0].changeSymbolLayer(0, symbol_layer)
            elif layer.geometryType()==QgsWkbTypes.PointGeometry :
                properties = {'size': '2', 'color': self.mColor.name(), 'outline_color': self.mColor.name(), 'outline_width': '0.6'}
                symbol_layer = QgsSimpleMarkerSymbolLayer.create(properties)
                layer.renderer().symbols(QgsRenderContext())[0].changeSymbolLayer(0, symbol_layer)
        else:
            if self.colorIndex > (len(self.colorValues) - 1):
                self.colorIndex = 0
            color = QColor(self.colorValues[self.colorIndex])
            self.colorIndex += 1
            if layer.geometryType()==QgsWkbTypes.PolygonGeometry :
                layer.renderer().symbols(QgsRenderContext())[0].symbolLayer(0).setStrokeWidth(0.4)
                layer.renderer().symbols(QgsRenderContext())[0].symbolLayer(0).setBrushStyle(Qt.Dense4Pattern)
                layer.renderer().symbols(QgsRenderContext())[0].symbolLayer(0).setFillColor(color)
                layer.setFeatureBlendMode(13)
        self.iface.layerTreeView().refreshLayerSymbology(layer.id())


    def cloneToMemory(self):
        curlayer = self.iface.mapCanvas().currentLayer()
        selectedFeatCount = curlayer.selectedFeatureCount()
        geo = QgsWkbTypes.displayString(curlayer.wkbType()) # wkbType string name of geometry
        
        targetLayer = QgsVectorLayer(geo, self.dlg.lineEdit_2.text(), "memory")
        targetLayer.setCrs(curlayer.sourceCrs())
        QgsProject.instance().addMapLayer(targetLayer, False)
        root = QgsProject.instance().layerTreeRoot()
        
        self.setStyleLayer(targetLayer)
        
        if self.dlg.checkBoxAtrib.isChecked(): #copy attributes
            curlayer_attribute_list = curlayer.fields().toList()
            targetLayer_attribute_list = []
            targetLayerpr = targetLayer.dataProvider()
            
            for attrib in curlayer_attribute_list:
                if targetLayer.fields().lookupField(attrib.name())==-1:
                    targetLayer_attribute_list.append(QgsField(attrib.name(),attrib.type()))
            with edit(targetLayer):
                for attr in targetLayer_attribute_list:
                    if attr.type() == 1: # иначе игнорируется поле с типом 1 (bool)
                        attr = QgsField(attr.name(), QVariant.String) # конвертируем bool в string
                    res_add = targetLayer.addAttribute(attr)   
                    if not res_add:
                        print(u'Не создано поле {}'.format(attr.name())) 
            targetLayer.updateFields()

        # for feat in curlayer.selectedFeatures(): # not work more
        #     targetLayer.dataProvider().addFeatures([feat]) # not work more

        # ИЗ МОДУЛЯ Apend Features To layer -----------------------------------------------
        # В старом варианте в QGIS3 при добавлении объектов с отличающимся набором аттрибутов
        # происходила задержка с выводом сообщений в логи. Что затягивало процесс.
        mapping = dict()
        for target_idx in targetLayer.fields().allAttributesList():
            target_field = targetLayer.fields().field(target_idx)
            source_idx = curlayer.fields().indexOf(target_field.name())
            if source_idx != -1:
                mapping[target_idx] = source_idx

        features = curlayer.selectedFeatures()
        destType = targetLayer.geometryType()
        destIsMulti = QgsWkbTypes.isMultiType(targetLayer.wkbType())
        new_features = []

        for current, in_feature in enumerate(features):
            attrs = {target_idx: in_feature[source_idx] for target_idx, source_idx in mapping.items()}
            geom = QgsGeometry()
            if in_feature.hasGeometry() and targetLayer.isSpatial():
                # Convert geometry to match destination layer
                # Adapted from QGIS qgisapp.cpp, pasteFromClipboard()
                geom = in_feature.geometry()
                if destType != QgsWkbTypes.UnknownGeometry:
                    newGeometry = geom.convertToType(destType, destIsMulti)
                    if newGeometry.isNull():
                        continue
                    geom = newGeometry
                # Avoid intersection if enabled in digitize settings
                geom.avoidIntersections(QgsProject.instance().avoidIntersectionsLayers())

            new_feature = QgsVectorLayerUtils().createFeature(targetLayer, geom, attrs)
            new_features.append(new_feature)

        with edit(targetLayer):
            res = targetLayer.addFeatures(new_features)
        # ИЗ МОДУЛЯ Apend Features To layer -----------------------------------------------end

        root.insertLayer(0, targetLayer)
        self.iface.messageBar().clearWidgets()
        self.iface.setActiveLayer(targetLayer)
        curlayer.selectByIds([])

        if res:
            self.iface.messageBar().pushMessage(u"Выполнено", u"Склонировано {0}/{1} объектов".format(len(new_features), selectedFeatCount), duration=5, level=0)


    def cloneToExists(self):

        curlayer = self.iface.mapCanvas().currentLayer()
        targetName = self.dlg.comboBox.currentText()
        targetLayer = self.getVectorLayerByName(targetName)
        
        self.iface.setActiveLayer(curlayer)
        self.iface.actionCopyFeatures().trigger()
        self.iface.setActiveLayer(targetLayer)

        if targetLayer.isEditable() == False:
            targetLayer.startEditing()
        self.iface.actionPasteFeatures().trigger()
        
        if targetLayer.selectedFeatureCount() ==1:
            if targetLayer.isEditable() == False:
                targetLayer.startEditing()
            selb = targetLayer.selectedFeatures()
            self.iface.openFeatureForm(targetLayer, selb[0], False, False) 

        if not targetLayer.isEditable():
            self.iface.messageBar().pushMessage(u"Не выполнено ", u"Возможно, не достаточно прав на редактирование слоя", duration=7, level=2)

        
    def cloneGeometry(self):

        tomemory = False
        if self.dlg.radioToMemory.isChecked():  #MEMORY LAYER
            self.cloneToMemory()
        else:                                   #EXISTS LAYER
            self.cloneToExists()
        

    def run(self):
        """Run method that performs all the real work"""
        
        if self.iface.mapCanvas().currentLayer() == None:
            self.iface.messageBar().pushMessage(u"Не выбран активный слой", u"Выберите слой, объекты которого необходимо клонировать", duration=5, level=2)
            return
        elif self.iface.mapCanvas().currentLayer().selectedFeatureCount() <= 0:
            self.iface.messageBar().pushMessage(u"Не выбраны объекты в активном слое", u"Выберите объекты, которые необходимо клонировать", duration=5, level=2)
            return
        else:
            self.dlg.radioToMemory.setChecked(True)
            self.dlg.checkBoxAtrib.setChecked(True)
            self.dlg.maskColor.setColor(self.mColor)
            self.populateLayers()
            self.checktolayer()
            self.colorState()
            self.dlg.comboBox.setCurrentIndex(-1)

            curlayer = self.iface.mapCanvas().currentLayer()
            self.dlg.lineEdit.setText(curlayer.name())
            
            LayerBNamePrefix = u"_Клонирование из "+curlayer.name()
            cntName = self.countVectorLayerByName(LayerBNamePrefix)
            if cntName > 0:
                self.dlg.lineEdit_2.setText(LayerBNamePrefix+' '+str(cntName))
            else:
                self.dlg.lineEdit_2.setText(LayerBNamePrefix)
            self.dlg.label_3.setText(str(curlayer.selectedFeatureCount()))

            self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass
