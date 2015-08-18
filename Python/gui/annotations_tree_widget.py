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
PyQt graphical controls for annotations tree.
'''
import os
import sys
import shutil

from PyQt4.QtCore import pyqtSignature, QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *
from annotations_tree import TreeItemComposite
from bug_reproducer_assistant.base import AnnotationState

##
# @param myAnnotationState Bug-reproducer Assistant annotation state (see AnnotationState).
# @return The correspondent PyQt checked/unchecked.
def getCheckedStateFromAnnotation(myAnnotationState):
    '''
    Translate from bug_reproducer_assistant.base.AnnotationState to PyQt checked/unchecked.
    '''
    AT = AnnotationState
    return { AT.NOT_ANNOTATED: Qt.Unchecked,
             AT.SEMI_ANNOTATED: Qt.PartiallyChecked,
             AT.ANNOTATED: Qt.Checked }[myAnnotationState]
    
class AnnotationsTreeWidgetItem(QTreeWidgetItem):
    '''
    PyQt tree element for annotations tree.
    It holds a TreeItemComposite (bridge pattern),
    where the annotations logic takes place.
    This is a good separation of Interface and business logic.
    '''
    ##
    # @param self The AnnotationsTreeWidgetItem to construct.
    # @param myTreeItemComposite The TreeItemComposite instance associated to this tree item.
    # @param mayAnnotate If True, the tree item is enabled for annotations.
    def __init__(self, myTreeItemComposite, mayAnnotate = True):
        '''
        Constructor.
        '''
        QTreeWidgetItem.__init__(self)
        self.treeItemComposite_ = myTreeItemComposite
        self.mayAnnotate_ = mayAnnotate

    ##
    # @param self The AnnotationsTreeWidgetItem to construct.
    def annotate(self):
        '''
        Annotate a class or function, forwarding the work to
        the TreeItemComposite.
        '''
        if self.mayAnnotate_:
            self.treeItemComposite_.changeAnnotationState(True)

    ##
    # @param self The AnnotationsTreeWidgetItem to construct.
    def unannotate(self):
        '''
        Unannotate a class or function, forwarding the work to
        the TreeItemComposite.
        '''
        if self.mayAnnotate_:
            self.treeItemComposite_.changeAnnotationState(False)

    ##
    # @param self The AnnotationsTreeWidgetItem to construct.
    # @return The Internal TreeItemComposite.
    def getTreeItemComposite(self):
        '''
        Get the internal TreeItemComposite.
        '''
        return self.treeItemComposite_

    ##
    # @return If tree item is enabled for annotations.
    def mayAnnotate(self):
        '''
        Return if tree item is enabled for annotations.
        '''
        return self.mayAnnotate_