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
from PyQt5.QtCore import QObject, QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QDialogButtonBox, QColorDialog, QAction
from qgis.core import  Qgis, QgsFeature, QgsGeometry, QgsMapLayer, QgsSpatialIndex, QgsFeatureRequest, QgsVectorLayer, QgsField, QgsProject, QgsSimpleLineSymbolLayer, QgsSimpleMarkerSymbolLayer, QgsWkbTypes, QgsRenderContext
# Initialize Qt resources from file resources.py
from .resources_rc import *
# Import the code for the dialog
from .clone_geometry_dialog import CloneGeometryDialog
import os.path
import locale


class CloneGeometry:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
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

        # Create the dialog (after translation) and keep reference
        # self.mColor = "#0055ff"
        self.mColor = QColor(0,85,255,255) #дефолтный цвет

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


        # TODO: We are going to let the user set this up in a future iteration

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
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
                    if layer.geometryType() == self.iface.mapCanvas().currentLayer().geometryType():
                        layerlist.append( layer.name() )
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
        if self.dlg.checkBox_mask.isChecked():
            self.mColor = self.dlg.maskColor.color()
            if layer.geometryType()==QgsWkbTypes.PolygonGeometry  or layer.geometryType()==QgsWkbTypes.LineGeometry :
                properties = {'color': self.mColor.name(), 'outline_width': '0.6'}
                symbol_layer = QgsSimpleLineSymbolLayer.create(properties)
                layer.renderer().symbols(QgsRenderContext())[0].changeSymbolLayer(0, symbol_layer)
            elif layer.geometryType()==QgsWkbTypes.PointGeometry :
                properties = {'size': '2', 'color': self.mColor.name(), 'outline_color': self.mColor.name(), 'outline_width': '0.6'}
                symbol_layer = QgsSimpleMarkerSymbolLayer.create(properties)
                layer.renderer().symbols(QgsRenderContext())[0].changeSymbolLayer(0, symbol_layer)
        else:
            if layer.geometryType()==QgsWkbTypes.PolygonGeometry :
                layer.renderer().symbols(QgsRenderContext())[0].symbolLayer(0).setStrokeWidth(0.4)
                layer.renderer().symbols(QgsRenderContext())[0].symbolLayer(0).setBrushStyle(Qt.Dense4Pattern) 
                layer.setFeatureBlendMode(13)
        self.iface.layerTreeView().refreshLayerSymbology(layer.id())
        
    def cloneGeometry(self):

        curlayer = self.iface.mapCanvas().currentLayer()
        
        tomemory = False
        if self.dlg.radioToMemory.isChecked():  #MEMORY LAYER
            tomemory = True
            if curlayer.geometryType()==QgsWkbTypes.PolygonGeometry :
                geo = "MultiPolygon"
            elif curlayer.geometryType()==QgsWkbTypes.LineGeometry :
                geo = "MultiLineString"
            elif curlayer.geometryType()==QgsWkbTypes.PointGeometry :
                geo = "Point"
            
            LayerB = QgsVectorLayer(geo, self.dlg.lineEdit_2.text(), "memory")
            QgsProject.instance().addMapLayer(LayerB, False)
            root = QgsProject.instance().layerTreeRoot()
            
            self.setStyleLayer(LayerB)
            
            if self.dlg.checkBoxAtrib.isChecked():
                curlayer_fields = curlayer.dataProvider().fields()
                curlayer_attribute_list = curlayer.dataProvider().fields().toList()
                LayerB_attribute_list = []
                LayerBpr = LayerB.dataProvider()
                
                for attrib in curlayer_attribute_list:
                    if LayerB.fields().lookupField(attrib.name())==-1:
                        LayerB_attribute_list.append(QgsField(attrib.name(),attrib.type()))
                LayerBpr.addAttributes(LayerB_attribute_list)
                LayerB.updateFields()

            for feat in curlayer.selectedFeatures():
                LayerB.dataProvider().addFeatures([feat])
                
            root.insertLayer(0, LayerB)
            self.iface.messageBar().clearWidgets()
            self.iface.setActiveLayer(LayerB)
            curlayer.selectByIds([])
        else:                                                   #EXISTS LAYER

            myName = self.dlg.comboBox.currentText()
            LayerB = self.getVectorLayerByName(myName)
     
     #-----
            self.iface.setActiveLayer(curlayer)
            self.iface.actionCopyFeatures().trigger()
            self.iface.setActiveLayer(LayerB)
            
            if LayerB.isEditable() == False:
                LayerB.startEditing()
            self.iface.actionPasteFeatures().trigger()
            
            if LayerB.selectedFeatureCount() ==1:
                if LayerB.isEditable() == False:
                    LayerB.startEditing()
                selb = LayerB.selectedFeatures()
                self.iface.openFeatureForm(LayerB, selb[0], False, False)
            
            if LayerB.isEditable():
                pass
            else:
                self.iface.messageBar().pushMessage(u"Не выполнено ", u"Возможно, не достаточно прав на редактирование слоя", duration=7, level=2)
        
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
            # show the dialog
            self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:

            pass
