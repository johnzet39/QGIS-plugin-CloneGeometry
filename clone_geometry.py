# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CloneGeometry
                                 A QGIS plugin
 Клонирование геометрии в другой слой
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
from PyQt4.QtCore import SIGNAL, QObject, QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QColor,QAction, QIcon, QDialogButtonBox, QColorDialog
from qgis.core import  QGis, QgsFeature, QgsGeometry, QgsMapLayerRegistry, QgsMapLayer, QgsSpatialIndex, QgsFeatureRequest, QgsVectorLayer, QgsField, QgsProject, QgsSimpleLineSymbolLayerV2, QgsSimpleMarkerSymbolLayerV2
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from clone_geometry_dialog import CloneGeometryDialog
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
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

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
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        '''
        icon_path = ':/plugins/CloneGeometry/icon.png'
        self.add_action(
            icon_path,
            text=u'Клонировать границы в другой слой...',
            callback=self.run,
            parent=self.iface.mainWindow())
        '''
        self.clone_action = QAction(
            QIcon(':/plugins/CloneGeometry/icon.png'),
            u"Клонировать границы в другой слой...", self.iface.mainWindow())
            
        QObject.connect(self.clone_action, SIGNAL("triggered()"), self.run)
        self.iface.digitizeToolBar().addAction(self.clone_action)
        self.iface.addPluginToVectorMenu(u"&Clone geometry", self.clone_action)
        QObject.connect(self.iface, SIGNAL('currentLayerChanged(QgsMapLayer *)'), self.check_buttons_state)
        QObject.connect(self.iface.mapCanvas(), SIGNAL('selectionChanged(QgsMapLayer *)'), self.check_buttons_state)
        
        self.check_buttons_state(None)
 

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        '''
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Clone geometry'),
                action)
            self.iface.removeToolBarIcon(action)
            self.iface.unregisterMainWindowAction(action)
            self.iface.digitizeToolBar().removeAction(action)
        # remove the toolbar
        '''
        self.iface.unregisterMainWindowAction(self.clone_action)
        self.iface.removePluginVectorMenu(u"&Clone geometry", self.clone_action)
        self.iface.digitizeToolBar().removeAction(self.clone_action)
        QObject.disconnect(self.iface, SIGNAL('currentLayerChanged(QgsMapLayer *)'), self.check_buttons_state)
        QObject.disconnect(self.iface.mapCanvas(), SIGNAL('selectionChanged(QgsMapLayer *)'), self.check_buttons_state)
       
    # def color_picker(self):

    #     self.mColor = QColorDialog.getColor().name()
    #     self.dlg.maskColor.setStyleSheet("QWidget { background-color: %s}" % self.mColor)

    def colorState(self):
        if self.dlg.checkBox_mask.isChecked():
            self.dlg.maskColor.setEnabled(True)
            # self.dlg.maskColor.setStyleSheet("QWidget { background-color: %s}" % self.mColor)
        else:
            self.dlg.maskColor.setEnabled(False)
            # self.dlg.maskColor.setStyleSheet("")


    def check_buttons_state(self, layer=None):
        layer = self.iface.activeLayer()
        if not isinstance(layer, QgsVectorLayer):
            self.clone_action.setDisabled(True)
            return
        sel_feat_count = layer.selectedFeatureCount()
        if sel_feat_count < 1:
            self.clone_action.setDisabled(True)
            return
        if sel_feat_count > 0:
            self.clone_action.setEnabled(True)
            return
        self.clone_action.setEnabled(True)  # copy button can be pressed!

    def checktolayer( self ):
        self.buttonOk.setEnabled(True)

        if self.dlg.radioToMemory.isChecked():
            self.dlg.comboBox.setEnabled(False)
            self.dlg.checkBoxAtrib.setEnabled(True)
        elif self.dlg.radioToLayer.isChecked():
            self.dlg.comboBox.setEnabled(True)
            self.dlg.checkBoxAtrib.setEnabled(False)
            if self.dlg.comboBox.currentIndex() == -1:
                self.buttonOk.setEnabled(False)

    def populateLayers( self ):
        myListB = []
        self.dlg.comboBox.clear()
        myListB = self.getLayerNames()
        self.dlg.comboBox.addItems( myListB )

    def getLayerNames( self ):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        layerlist = []
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                if not layer.isReadOnly():
                    if layer.geometryType() == self.iface.mapCanvas().currentLayer().geometryType():
                    #if layer.geometryType() == QGis.Polygon:
                        layerlist.append( layer.name() )
        return sorted( layerlist, cmp=locale.strcoll )

    def getVectorLayerByName( self, myName ):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None
                    
    def countVectorLayerByName(self, myName):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        cnt = 0
        maxcnt = 1
        for name, layer in layermap.iteritems():
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
            print self.mColor
            if layer.geometryType()==QGis.Polygon or layer.geometryType()==QGis.Line:
                properties = {'color': self.mColor.name(), 'outline_width': '0.6'}
                symbol_layer = QgsSimpleLineSymbolLayerV2.create(properties)
                layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)
            elif layer.geometryType()==QGis.Point:
                properties = {'size': '4', 'color': self.mColor.name(), 'outline_color': self.mColor.name(), 'outline_width': '0.6'}
                symbol_layer = QgsSimpleMarkerSymbolLayerV2.create(properties)
                layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)
        else:
            if layer.geometryType()==QGis.Polygon:
                layer.rendererV2().symbols()[0].symbolLayer(0).setBorderWidth(0.4)
                layer.rendererV2().symbols()[0].symbolLayer(0).setBrushStyle(Qt.Dense4Pattern) 
                layer.setFeatureBlendMode(13)
            
        
    def cloneGeometry(self):
        MLayer = self.iface.mapCanvas().currentLayer()
        
        tomemory = False
        if self.dlg.radioToMemory.isChecked():  #MEMORY LAYER
            tomemory = True
            if MLayer.geometryType()==QGis.Polygon:
                geo = "MultiPolygon"
            elif MLayer.geometryType()==QGis.Line:
                geo = "MultiLineString"
            elif MLayer.geometryType()==QGis.Point:
                geo = "Point"
            
            LayerB = QgsVectorLayer(geo, self.dlg.lineEdit_2.text(), "memory")
            QgsMapLayerRegistry.instance().addMapLayer(LayerB, False)
            root = QgsProject.instance().layerTreeRoot()
            
            self.setStyleLayer(LayerB)
            
            if self.dlg.checkBoxAtrib.isChecked():
                MLayer_fields = MLayer.dataProvider().fields()
                MLayer_attribute_list = MLayer.dataProvider().fields().toList()
                LayerB_attribute_list = []
                LayerBpr = LayerB.dataProvider()
                
                for attrib in MLayer_attribute_list:
                    if LayerB.fieldNameIndex(attrib.name())==-1:
                        LayerB_attribute_list.append(QgsField(attrib.name(),attrib.type()))
                LayerBpr.addAttributes(LayerB_attribute_list)
                LayerB.updateFields()

            for feat in MLayer.selectedFeatures():
                LayerB.dataProvider().addFeatures([feat])
                
            root.insertLayer(0, LayerB)
            self.iface.messageBar().clearWidgets()
            self.iface.setActiveLayer(LayerB)
            MLayer.setSelectedFeatures([])
        else:                                                   #EXISTS LAYER

            myName = self.dlg.comboBox.currentText()
            LayerB = self.getVectorLayerByName(myName)
     
     #-----
            self.iface.setActiveLayer(MLayer)
            self.iface.actionCopyFeatures().trigger()
            self.iface.setActiveLayer(LayerB)
            
            if LayerB.isEditable() == False:
                LayerB.startEditing()
            self.iface.actionPasteFeatures().trigger()
            
            #LayerB.commitChanges()
            # if LayerB.selectedFeatureCount() ==1 and LayerB.providerType() <> u'memory':
            if LayerB.selectedFeatureCount() ==1:
                if LayerB.isEditable() == False:
                    LayerB.startEditing()
                selb = LayerB.selectedFeatures()
                self.iface.openFeatureForm(LayerB, selb[0], False, False)
            
            if LayerB.isEditable():
                pass
                # self.iface.messageBar().pushMessage(u"Склонирована геометрия из слоя '"+MLayer.name()+u"' в слой '"+LayerB.name()+"'", duration=7, level=3)
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
            MLayer = self.iface.mapCanvas().currentLayer()
            self.dlg.lineEdit.setText(MLayer.name())
            
            LayerBNamePrefix = u"_Клонирование из "+MLayer.name()
            cntName = self.countVectorLayerByName(LayerBNamePrefix)
            if cntName > 0:
                self.dlg.lineEdit_2.setText(LayerBNamePrefix+' '+str(cntName))
            else:
                self.dlg.lineEdit_2.setText(LayerBNamePrefix)
            
            self.dlg.label_3.setText(str(MLayer.selectedFeatureCount()))
            # show the dialog
            self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            #self.cloneGeometry
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
