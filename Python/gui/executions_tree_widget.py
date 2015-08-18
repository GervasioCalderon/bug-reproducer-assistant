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
PyQt graphical controls for executions tree.
'''
import os
import sys
import shutil

from PyQt4.QtCore import pyqtSignature, QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *

class ExecutionsTreeWidgetItem(QTreeWidgetItem):
    '''
    PyQt tree element for executions tree.
    '''
    class FileType:
        '''
        Type of file to be stored in the tree. It may be a Json database (execution file)
        or its child equivalent program.
        '''
        EXECUTION, EQUIV_PROGRAM = range(2)
    ##
    # @param self The ExecutionsTreeWidgetItem to construct.
    # @param myFileType This item file type (see FileType).
    # @param filePath Path of the represented file.
    def __init__(self, myFileType, filePath):
        '''
        Constructor.
        '''
        FT = ExecutionsTreeWidgetItem.FileType
        assert myFileType in (FT.EXECUTION, FT.EQUIV_PROGRAM)
        QTreeWidgetItem.__init__(self)
        self.fileType_ = myFileType
        self.filePath_ = filePath
    
    ##
    # @param self The ExecutionsTreeWidgetItem.
    # @return This item file type.
    def getFileType(self):
        '''
        This item file type (see FileType).
        '''
        return self.fileType_

    ##
    # @param self The ExecutionsTreeWidgetItem.
    # @return The path of the represented file.
    def getFilePath(self):
        '''
        Get the path of the represented file.
        '''
        return self.filePath_ 