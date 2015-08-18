import os
import sys
import shutil

def createFolderIfNotExists(folderPath):
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)

def copyFolder(folderFrom, folderTo):
    copyCommand = r'Robocopy /E "' + folderFrom + '" "' + folderTo + '"'
    print copyCommand
    os.system( copyCommand )

THIS_FOLDER = os.path.dirname( os.path.abspath(__file__) )
INSTALLATION_FOLDER = 'C:\\Program Files\\Bug-reproducer Assistant'

CPP_INCLUDES_FOLDER_FROM = os.path.join(THIS_FOLDER, 'C++\\bug_reproducer_assistant')
CPP_FOLDER_TO = os.path.join(INSTALLATION_FOLDER, 'C++')
CPP_INCLUDES_FOLDER_TO = os.path.join(CPP_FOLDER_TO, 'include')

CPP_LIBRARIES_FOLDER_FROM = os.path.join(THIS_FOLDER, 'C++\\libs')
CPP_LIBRARIES_FOLDER_TO = os.path.join(CPP_FOLDER_TO, 'libs')

CPP_INCLUDES_BRA_FROM = os.path.join(CPP_INCLUDES_FOLDER_FROM, 'bug_reproducer_assistant\\include')
CPP_INCLUDES_JSON_FROM = os.path.join(CPP_INCLUDES_FOLDER_FROM, 'jsoncpp\\include')

PYTHON_BUG_REPRODUCER_ASSISTANT = os.path.join(THIS_FOLDER, 'Python\\bug_reproducer_assistant')

def main(pythonPath):
    createFolderIfNotExists(INSTALLATION_FOLDER)
    createFolderIfNotExists(CPP_FOLDER_TO)
    createFolderIfNotExists(CPP_INCLUDES_FOLDER_TO)
    createFolderIfNotExists(CPP_LIBRARIES_FOLDER_TO)
    copyFolder(CPP_INCLUDES_BRA_FROM, CPP_INCLUDES_FOLDER_TO)
    copyFolder(CPP_INCLUDES_JSON_FROM, CPP_INCLUDES_FOLDER_TO)
    copyFolder(CPP_LIBRARIES_FOLDER_FROM, CPP_LIBRARIES_FOLDER_TO)    
    os.system('regedit /s registryBra.reg')

    #Copy the rest of the files    
    copyFolder(THIS_FOLDER, INSTALLATION_FOLDER)
    #Copy Python bug_reproducer_assistant to Site-packages
    SITE_PACKAGES_FOLDER = os.path.join(pythonPath, 'Lib\\site-packages')
    SITE_PACKAGES_FOLDER_BRA = os.path.join(SITE_PACKAGES_FOLDER, 'bug_reproducer_assistant')
    createFolderIfNotExists(SITE_PACKAGES_FOLDER_BRA)
    copyFolder(PYTHON_BUG_REPRODUCER_ASSISTANT, SITE_PACKAGES_FOLDER_BRA)
    
    print "Installation successful! To run Bug-reproducer Assistant, go to " + os.path.join(INSTALLATION_FOLDER, 'gui') + ' and run "python main.py".'
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s install <Python installation path>" %  os.path.basename(sys.argv[0])
        sys.exit(1)
    try:
        main(sys.argv[2])
    except Exception, e:
        print 'Error installing Bug-reproducer Assistant: "' + str(e) + '"'
        import traceback
        traceback.print_exc()