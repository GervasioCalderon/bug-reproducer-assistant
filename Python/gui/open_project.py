# This file is part of Bug-reproducer Assistant
# The tool has been designed and developed by Gervasio Andres Calderon Fernandez, of Core Security Technologies
# 
# Copyright (c) 2011, Core Security Technologies
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Window to open/remove a project.
'''
from PyQt4.QtCore import pyqtSignature, QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *
from ui_openProject import Ui_openProjectDialog
import os
import config
import project

class OpenProjectWindow(QDialog, Ui_openProjectDialog):
    '''
    PyQt dialog to open or remove a project.
    '''
    ##
    # @param self The OpenProjectWindow to construct.
    # @param parent Optional parent window.
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.createActions()
        self.loadControls()

    ##
    # @param self The OpenProjectWindow.
    def createActions(self):
        '''
        Create PyQt actions.
        '''
        self.connect(self.removeProjectButton, SIGNAL("clicked()"), self, SLOT("removeProject()"))
        self.connect(self.projectsListWidget, SIGNAL("currentRowChanged(int)"),self, SLOT("projectSelectionChanged()"))

    ##
    # @param self The OpenProjectWindow.
    def loadControls(self):
        '''
        Initial load of this window's controls.
        '''
        self.removeProjectButton.setEnabled(False)
        self.confirmationButtonBox.button(QDialogButtonBox.Open).setEnabled(False)
        allProjects = project.projectsManagerInstance().getAllProjects()

        projectNames = sorted(allProjects.keys())
        for projectName in projectNames:
            self.projectsListWidget.addItem(projectName)

    ##
    # @param self The OpenProjectWindow.
    # @return The name for the project selected by the user.
    def _getSelectedProjectName(self):
        '''
        Get the name for the project selected by the user.
        '''
        return str(self.projectsListWidget.currentItem().text())

    ##
    # @param self The OpenProjectWindow.
    # @return Whether or not there's one project selected by the user.
    def _isOneProjectSelected(self):
        '''
        Tell if the user has selected a project.
        '''
        return self.projectsListWidget.currentItem() >= 0
    
    ## SLOTS
    @pyqtSignature("")
    ##
    # @param self The OpenProjectWindow.
    def accept(self):
        '''
        User accepts -> opens the selected project.  
        '''
        if self._isOneProjectSelected():
            projectName = self._getSelectedProjectName()
            project.projectsManagerInstance().setCurrentProjectName(projectName)
        QDialog.accept(self)
        
    @pyqtSignature("")
    ##
    # @param self The OpenProjectWindow.
    def reject(self):
        '''
        User has cancelled.
        '''
        QDialog.reject(self)

    @pyqtSignature("")
    ##
    # @param self The OpenProjectWindow.
    def removeProject(self):
        '''
        User asks to remove a project. Forward the erasure to the ProjectsManager.
        '''
        if self._isOneProjectSelected():
            selectedItem = self.projectsListWidget.takeItem(self.projectsListWidget.currentRow()) 
            projectName = str(selectedItem.text())
            project.projectsManagerInstance().removeProject(projectName)
            
    @pyqtSignature("")
    ##
    # @param self The OpenProjectWindow.
    def projectSelectionChanged(self):
        '''
        User has selected a project: enable the related controls.
        '''
        self.removeProjectButton.setEnabled(True)
        self.confirmationButtonBox.button(QDialogButtonBox.Open).setEnabled(True)