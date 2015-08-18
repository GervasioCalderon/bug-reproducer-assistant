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
Utilities for reading/writing the Windows registry.
'''
import _winreg

BUG_REPRODUCER_ASSISTANT_KEY = r"SOFTWARE\Bug-reproducer Assistant"
INSTALL_PATH = "InstallPath"
FIRST_USE = "FirstUse"

##
# @param valueNameStr Value to search in the "Bug-reproducer Assistant" registry folder.
# @param type Type of the value to read (_winreg.REG_SZ, _winreg.REG_DWORD, etc.).
# @return The actual value found in the registry.
def readValueFromRegistry(valueNameStr, type):
    '''
    Read a value from "Bug-reproducer Assistant" registry.
    '''
    aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    try:
        aKey = _winreg.OpenKey(aReg, BUG_REPRODUCER_ASSISTANT_KEY) 
        try:
            value, readType = _winreg.QueryValueEx(aKey, valueNameStr)
            assert readType == type
            return value
        finally:
            _winreg.CloseKey(aKey)
    finally:
        _winreg.CloseKey(aReg)

##
# @param valueNameStr Value to search in the "Bug-reproducer Assistant" registry folder.
# @param type Type of the value to write (_winreg.REG_SZ, _winreg.REG_DWORD, etc.).
# @param value Actual value to save.
def writeValueIntoRegistry(valueNameStr, type, value):
    '''
    Write a value into "Bug-reproducer Assistant" registry.
    '''
    aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    try:
        try:
            aKey = _winreg.OpenKey(aReg, BUG_REPRODUCER_ASSISTANT_KEY, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.SetValueEx(aKey, valueNameStr, 0, type, value)
        finally:
            _winreg.CloseKey(aReg)
    finally:
        _winreg.CloseKey(aReg)

##
# @return "Bug-reproducer Assistant" install path.
def readInstallPathFromRegistry():
    '''
    Get "Bug-reproducer Assistant" install path from the registry.
    '''
    return readValueFromRegistry(INSTALL_PATH, _winreg.REG_SZ)

##
# @return Whether the program hasn't run yet. 
def readFirstUseFromRegistry():
    '''
    Get "first use" (the program hasn't run yet) flag from the registry.
    '''
    return readValueFromRegistry(FIRST_USE, _winreg.REG_DWORD)

##
# @param installPath "Bug-reproducer Assistant" install path from the registry.
def writeInstallPathIntoRegistry(installPath):
    '''
    Write "Bug-reproducer Assistant" install path into the registry.
    '''
    writeValueIntoRegistry(INSTALL_PATH, _winreg.REG_SZ, installPath)

##
# @param firstUse If True, the program hasn't run yet.
def writeFirstUseIntoRegistry(firstUse):
    '''
    Write "first use" (the program hasn't run yet) flag into the registry.
    '''
    writeValueIntoRegistry(FIRST_USE, _winreg.REG_DWORD, firstUse)

if __name__ == '__main__':
    installPath = readInstallPathFromRegistry()
    firstUse = readFirstUseFromRegistry()

    print "ORIGINAL VALUES: "
    print "installPath: " + installPath
    print "firstUse: " + str(firstUse)
    print ""

    installPathBkp = installPath
    firstUseBkp = firstUse

    #Test writing    
    installPath = r"C:\Bochini\Maranga"
    firstUse = 25

    writeInstallPathIntoRegistry(installPath)
    writeFirstUseIntoRegistry(firstUse)
    
    installPathRead = readInstallPathFromRegistry()
    firstUseRead = readFirstUseFromRegistry()   

    print "WRITING TEST VALUES: "
    print "installPath: " + installPathRead
    print "firstUse: " + str(firstUseRead)
    print ""

    #Restore original values
    writeInstallPathIntoRegistry(installPathBkp)
    writeFirstUseIntoRegistry(firstUseBkp)

    installPathRestored = readInstallPathFromRegistry()
    firstUseRestored = readFirstUseFromRegistry()   

    print "RESTORING OLD VALUES: "
    print "installPath: " + installPathRestored
    print "firstUse: " + str(firstUseRestored)