import os
import sys
import glob
import platform
import logging
import imp
import re

local = ARGUMENTS.get('local', None)

localModuleName = "localSettings"
if local:
    localModuleName += "_" + local

try:
    localSettings = imp.load_module(localModuleName, *imp.find_module(localModuleName))
except ImportError:
    logging.error("No local settings file found: %s.py" % localModuleName)
    sys.exit()

platformSettings = {}
platformSettings['darwin.i386']      = {'compileFlags'  : {'common'  : ['-c', '-DUSE_GLEW', '-fPIC', '-msse', '-Wall'],
                                                           'debug'   : ['-g'],
                                                           'release' : ['-O']},
                                        'linkFlags'     : ['-framework', 'OpenGL'],
                                        'libs'          : ['DDImage', "GLEW"]}
                               
platformSettings['darwin.x86_64']    = {'compileFlags'  : {'common'  : ['-c', '-DUSE_GLEW', '-fPIC', '-msse', '-arch', 'x86_64', '-Wall'],
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

def getTrueFalse(val):
    trueVals = ("1", "true", "y", "yes", True, 1)
    falseVals = ("0", "false", "n", "no", False, 0)
    if isinstance(val, str):
        val = val.lower()
    return True if val in trueVals else False if val in falseVals else None


platformType = platform.system().lower()
arch = ARGUMENTS.get('arch', localSettings.defaultArch)

nukeVersionREs = [re.compile("(?P<major>\d+).(?P<minor>\d+)v(?P<release>\d+)b(?P<beta>\d+)"),
                  re.compile("(?P<major>\d+).(?P<minor>\d+)v(?P<release>\d+)a(?P<alpha>\d+)"),
                  re.compile("(?P<major>\d+).(?P<minor>\d+)v(?P<release>\d+)")]

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

settings = platformSettings[platformName]

settings['platformType'] = platformType

settings['nuke_root'] = localSettings.nukeLocation[platformName]

dev = getTrueFalse(ARGUMENTS.get('dev', '0'))
if dev is None:
    logging.error("'dev' value should be 0 or 1, True or False, Yes or No")
    sys.exit()

mode = ARGUMENTS.get('mode', 'debug')

buildNodes = (ARGUMENTS.get('nodes', "") + "," + ARGUMENTS.get("node", "")).strip(",")

if buildNodes:
    buildNodes = buildNodes.split(",")
else:
    buildNodes = ["all"]

settings['nuke_version'] = ARGUMENTS.get('nuke_version', localSettings.defaultNukeVersion)
settings['nuke_root'] = ARGUMENTS.get('nuke_root', os.path.expandvars(settings['nuke_root'] % settings))

if mode not in ["release", "debug"]:
    logging.error("Mode must be one of 'release' or 'debug' (default: 'release')")
    sys.exit()

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
    logging.error("Invalid Nuke version : %s" % settings['nuke_version'])
    sys.exit()

settings['nuke_build_version'] = buildVersionFolder

settings['install_locations'] = {}
for installPath in ("plugins", "menu"):
    settings['install_locations'][installPath] = os.path.expandvars(localSettings.install[mode][installPath] % settings) if localSettings.install[mode][installPath] else None

print settings['install_locations']

sourceFolder = "source"
menuFolder = "menu"
buildFolder = os.path.join("build", buildVersionFolder, platformName)

if not os.path.isdir(buildFolder):
    os.makedirs(buildFolder)

sourceFiles = glob.glob(os.path.join(sourceFolder, "*.cpp"))
menuFiles = glob.glob(os.path.join(menuFolder, "*.py"))

nodes = []

for sourceFile in sourceFiles:
    nodes.append({'name': os.path.splitext(os.path.basename(sourceFile))[0], 'dev': os.path.isfile(os.path.splitext(sourceFile)[0] + ".dev")})

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
    

for node in nodes:
    # Check if this node should be built.
    if node['name'] in buildNodes or ("all" in buildNodes and (not node['dev'] or dev)):
        buildPath = os.path.join(buildFolder, mode, node['name'])
        builtLib = env.SharedLibrary(buildPath, [os.path.join(buildFolder, node['name'] + ".cpp")])
        env.Install(settings['install_locations']['plugins'], builtLib)

for menuFile in menuFiles:
    env.Install(settings['install_locations']['menu'], menuFile)

if settings['install_locations']['plugins']:
    env.Alias("install", settings['install_locations']['plugins'])

if settings['install_locations']['menu']:
    env.Alias("install", settings['install_locations']['menu'])

"""
TODO: Create a test to load Nuke in terminal mode and check if the plugins load properly
"""
