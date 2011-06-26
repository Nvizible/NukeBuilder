import os
import sys
import glob
import platform
import logging
import imp
import re
import copy

logging.basicConfig(level=logging.INFO)

local = ARGUMENTS.get('local', None)

localSettingsModuleName = "localSettings"
if local:
    localSettingsModuleName += "_" + local

try:
    localSettings = imp.load_module(localSettingsModuleName, *imp.find_module(localSettingsModuleName))
except ImportError:
    logging.error("No local settings file found: %s.py" % localSettingsModuleName)
    sys.exit()

pluginSettingsModuleName = "pluginSettings"

try:
    pluginSettings = imp.load_module(pluginSettingsModuleName, *imp.find_module(pluginSettingsModuleName))
except ImportError:
    logging.error("No plugin settings file found: %s.py" % pluginSettingsModuleName)
    sys.exit()

platformSettings = {}
platformSettings['darwin.i386']      = {'nuke_subpath'  : "Nuke%(nuke_version)s.app/Contents/MacOS",
                                        'compileFlags'  : {'common'  : ['-c', '-DUSE_GLEW', '-fPIC', '-msse', '-Wall'],
                                                           'debug'   : ['-g'],
                                                           'release' : ['-O']},
                                        'linkFlags'     : ['-framework', 'OpenGL'],
                                        'libs'          : ['DDImage', "GLEW"]}
                               
platformSettings['darwin.x86_64']    = {'nuke_subpath'  : "Nuke%(nuke_version)s.app/Contents/MacOS",
                                        'compileFlags'  : {'common'  : ['-c', '-DUSE_GLEW', '-fPIC', '-msse', '-arch', 'x86_64', '-Wall'],
                                                           'debug'   : ['-g'],
                                                           'release' : ['-O']},
                                        'linkFlags'     : ['-framework', 'OpenGL', '-arch', 'x86_64'],
                                        'libs'          : ['DDImage', "GLEW"]}
                               
platformSettings['linux.i386']       = {'compileFlags'  : {'common'  : ['-c', '-DUSE_GLEW', '-fPIC', '-msse', '-Wall'],
                                                           'debug'   : ['-g'],
                                                           'release' : ['-O']},
                                        'libs'          : ['DDImage', "GLEW"]}

platformSettings['linux.x86_64']    = {'compileFlags'   : {'common'  : ['-c', '-DUSE_GLEW', '-fPIC', '-msse', '-m64', '-Wall'],
                                                           'debug'   : ['-g'],
                                                           'release' : ['-O']},
                                       'linkFlags'      : ['-m64'],
                                       'libs'           : ['DDImage', "GLEW"]}

platformSettings['windows.x86']     = {'compileFlags'   : {'common'  : ['-EHsc'],
                                                           'debug'   : ['-W1', '-GX', '-D_DEBUG', '/MDd'],
                                                           'release' : ['-O2', '-DNDEBUG', '/MD' ,'/Wp64']},
                                       'linkFlags'      : '/MACHINE:X86',
                                       'libPath'        : ['C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\lib', 
                                                           'C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\PlatformSDK\\Lib'],
                                       'cppPath'        : 'C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\include',                                       
                                       'libs'           : ['DDImage', 'glew32', 'OpenGL32'],
                                       'tools'          : ["msvc", "mslink"],
                                       'CC'             : '"C:/Program Files (x86)/Microsoft Visual Studio 8/VC/bin/cl.exe"',
                                       'CXX'            : '"C:/Program Files (x86)/Microsoft Visual Studio 8/VC/bin/cl.exe"',
                                       'LINK'           : '"C:/Program Files (x86)/Microsoft Visual Studio 8/VC/bin/link.exe"',                                       
                                       }

platformSettings['windows.x86_64']  = {'compileFlags'   : {'common'  : ['-EHsc'],
                                                           'debug'   : ['-W1', '-GX', '-D_DEBUG', '/MDd'],
                                                           'release' : ['-O2', '-DNDEBUG', '/MD' ,'/Wp64']},
                                       'linkFlags'      : '/MACHINE:X64',
                                       'libPath'        : ['C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\lib\\amd64', 
                                                           'C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\PlatformSDK\\Lib\\AMD64'],
                                       'cppPath'        : 'C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\include',
                                       'libs'           : ['DDImage', 'glew32', 'OpenGL32'],
                                       'tools'          : ["msvc", "mslink"],
                                       'CC'             : '"C:/Program Files (x86)/Microsoft Visual Studio 8/VC/bin/amd64/cl.exe"',
                                       'CXX'            : '"C:/Program Files (x86)/Microsoft Visual Studio 8/VC/bin/amd64/cl.exe"',
                                       'LINK'           : '"C:/Program Files (x86)/Microsoft Visual Studio 8/VC/bin/amd64/link.exe"', 
                                       }


platformType = platform.system().lower()
architectures = ARGUMENTS.get('arch', localSettings.defaultArch).split(",")
dev = ARGUMENTS.get('dev', '0')   
mode = ARGUMENTS.get('mode', 'debug')   
buildNodes = ARGUMENTS.get('nodes', "all").split(",")
nukeVersions = ARGUMENTS.get('nuke_version', localSettings.defaultNukeVersion).split(",")

if mode not in ["release", "debug"]:
    logging.error("Mode must be one of 'release' or 'debug' (default: 'release')")
    sys.exit()

nukeVersionREs = [re.compile("(?P<major>\d+).(?P<minor>\d+)v(?P<release>\d+)b(?P<beta>\d+)"),
                  re.compile("(?P<major>\d+).(?P<minor>\d+)v(?P<release>\d+)a(?P<alpha>\d+)"),
                  re.compile("(?P<major>\d+).(?P<minor>\d+)v(?P<release>\d+)")]

for arch in architectures:
    for nukeVersion in nukeVersions:
        if platformType == "windows":
            if arch == "32":
                platformName = "windows.x86"
            elif arch == "64":
                platformName = "windows.x86_64"
            else:
                logging.error("Invalid architecture : %s" % arch)
                sys.exit()
        elif platformType in ["linux", "darwin"]:
            if arch == "32":
                platformName = "%s.i386" % platformType
            elif arch == "64":
                platformName = "%s.x86_64" % platformType
            else:
                logging.error("Invalid architecture : %s" % arch)
                sys.exit()
        else:
            logging.error("Invalid platform : %s" % platformType)
            sys.exit()
        
        if platformName not in platformSettings:
            logging.error("Your platform is not supported")
            sys.exit()
        
        settings = copy.deepcopy(platformSettings[platformName])
        
        settings['nuke_root'] = localSettings.nukeLocation[platformName]
        
        if "nuke_subpath" in settings:
            settings['nuke_root'] = os.path.join(settings['nuke_root'], settings['nuke_subpath'])
        
        settings['nuke_version'] = nukeVersion
        
        
        buildVersionFolder = None
        for r in nukeVersionREs:
            m = re.match(r, settings['nuke_version'])
            if m:
                d = m.groupdict()
                if 'alpha' in d or 'beta' in d:
                    buildVersionFolder = settings['nuke_version']
                else:
                    buildVersionFolder = "%(major)s.%(minor)s" % d
                break
        
        if not buildVersionFolder:
            nukeInstallationsGlob = localSettings.nukeLocation[platformName] % {'nuke_version': "%sv?" % settings['nuke_version']}
            nukeInstallations = glob.glob(nukeInstallationsGlob)
            if nukeInstallations:
                nukeInstallations.sort()
                versionREStr = localSettings.nukeLocation[platformName] % {'nuke_version': "(?P<version>%sv\d)" % settings['nuke_version']}
                versionRE = re.compile(versionREStr)
                m = versionRE.match(nukeInstallations[-1])
                buildVersionFolder = settings['nuke_version']
                settings['nuke_version'] = m.groupdict()['version']
            else:
                logging.error("Invalid Nuke version : %s" % settings['nuke_version'])
                sys.exit()
        
        logging.info("Building for %s-bit Nuke %s" % (arch, settings['nuke_version']))

        settings['nuke_root'] = os.path.expandvars(settings['nuke_root'] % settings)
        
        sourceFolder = pluginSettings.sourceFolder
        buildFolder = os.path.join("build", buildVersionFolder, platformName)
        
        if not os.path.isdir(buildFolder):
            os.makedirs(buildFolder)
        
        sourceFiles = glob.glob(os.path.join(sourceFolder, "*.cpp"))
        
        nodes = []
        
        for sourceFile in sourceFiles:
            if dev == "1" or not os.path.isfile(os.path.splitext(sourceFile)[0] + ".dev"):
                nodes.append(os.path.splitext(os.path.basename(sourceFile))[0])
        
        VariantDir(buildFolder, sourceFolder)
        
        settings['nuke_lib_dir'] = settings['nuke_root']
        settings['nuke_include_dir'] = os.path.join(settings['nuke_lib_dir'], "include")
        
        env = Environment(SHLIBPREFIX = "",
                          CPPPATH = settings['nuke_include_dir'],
                          CCFLAGS = settings['compileFlags'][mode] + settings['compileFlags']['common'],
                          LIBPATH = [settings['nuke_lib_dir']],
                          LIBS = settings['libs'])
        
        if 'tools' in settings:
            env.Append(tools = settings['tools'])
        
        if 'linkFlags' in settings:
            env.Replace(LINKFLAGS = settings['linkFlags'])
            
        if 'libPath' in settings:
            env.Append(LIBPATH = settings['libPath'])
            
        if 'cppPath' in settings:   
            env.Replace(CPPPATH = [settings['nuke_include_dir'],settings['cppPath']])    
            
        if 'CC' in settings:
            env.Replace(CC = settings['CC'])
        if 'CXX' in settings:
            env.Replace(CXX = settings['CXX'])
        if 'LINK' in settings:
            env.Replace(LINK = settings['LINK'])    
            
        
        for nodeName in nodes:
            sourceFile = os.path.join(buildFolder, nodeName + ".cpp")
            
            # Check if this node should be built.
            if ("all" not in buildNodes and nodeName not in buildNodes):
                continue
                
            env.SharedLibrary(os.path.join(buildFolder, mode, nodeName), [sourceFile])
