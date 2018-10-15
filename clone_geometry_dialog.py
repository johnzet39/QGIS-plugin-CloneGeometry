# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CloneGeometryDialog
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

import os

from PyQt5 import QtGui, uic, QtWidgets
from .clone_geometry_dialog_base import Ui_CloneGeometryDialogBase



class CloneGeometryDialog(QtWidgets.QDialog, Ui_CloneGeometryDialogBase):
    def __init__(self):
        """Constructor."""
        super(CloneGeometryDialog, self).__init__()
        self.setupUi(self)
