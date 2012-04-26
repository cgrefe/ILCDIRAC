# $HeadURL$
# $Id$
'''
ILCDIRAC.Core.Utilities.PrepareOptionFiles

This provides a set of methods to prepare the option files needed by the ILC applications.

Created on Jan 29, 2010

@author: Stephane Poss
'''
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import string

def PrepareSteeringFile(inputSteering,outputSteering,detectormodel,stdhepFile,mac,nbOfRuns,startFrom,debug,outputlcio=None):
  """Writes out a steering file for Mokka
  
  Using specified parameters in the job definition passed from L{MokkaAnalysis}
  
  @param inputSteering: input steering file name
  @type inputSteering: string
  @param outputSteering: new steering file that will be used by Mokka
  @type outputSteering: string
  @param detectormodel: detector model to use from the DB
  @type detectormodel: string
  @param stdhepFile: generator file name to put in the mac file, if needed
  @type stdhepFile: string
  @param mac: input mac file
  @type mac: string
  @param nbOfRuns: number of runs to use
  @type nbOfRuns: string
  @param startFrom: First event to read from the generator file
  @type startFrom: int
  @param debug: overwrite default print level, if set to True, don't change input steering parameter
  @type debug: bool
  @param outputlcio: output slcio file name, not used
  @type outputlcio: string
  @return True
  
  """
  macname = "mokkamac.mac"
  if len(mac)<1:
    macfile = file(macname,"w")
    if len(stdhepFile)>0:
      macfile.write("/generator/generator %s\n"%stdhepFile)
    macfile.write("/run/beamOn %s\n"%nbOfRuns)
    macfile.close()
  else:
    macname = mac
    
  input = file(inputSteering,"r")
  output = file(str(outputSteering),"w")
  for line in input:
    if line.find("/Mokka/init/initialMacroFile")<0:
      if line.find("/Mokka/init/BatchMode")<0:
        if outputlcio:
          if line.find("lcioFilename")<0:
            #if line.find("#")>1:
              if detectormodel:
                if line.find("/Mokka/init/detectorModel")<0:
                  output.write(line)
                else:
                  output.write(line)
              else:
                output.write(line)
        else:
          #if line.find("#")==1:
            if detectormodel:
              if line.find("/Mokka/init/detectorModel")<0:
                output.write(line)
            else:
              output.write(line)
  if detectormodel:
    output.write("/Mokka/init/detectorModel %s\n"%detectormodel)
  
  if not debug:
    output.write("/Mokka/init/printLevel 1\n")

  output.write("/Mokka/init/BatchMode true\n")
  output.write("/Mokka/init/initialMacroFile %s\n"%macname)
  if outputlcio:
    output.write("/Mokka/init/lcioFilename %s\n"%outputlcio)
  output.write("/Mokka/init/startEventNumber %d"%startFrom)
  output.close()
  return True

def PrepareXMLFile(finalxml,inputXML,inputGEAR,inputSLCIO,numberofevts,outputREC,outputDST,debug):
  """Write out a xml file for Marlin
  
  Takes in input the specified job parameters for Marlin application given from L{MarlinAnalysis}
  
  @param finalxml: name of the xml file that will be used by Marlin
  @type finalxml: string
  @param inputXML: name of the provided input XML file
  @type inputXML: string
  @param inputSLCIO: input slcio file list
  @type inputSLCIO: list of strings
  @param numberofevts: number of events to process
  @type numberofevts: int
  @param outputREC: file name of REC
  @type outputREC: string
  @param outputDST: file name of DST
  @type outputDST: string
  @param debug: set to True to use given mode, otherwise set verbosity to SILENT
  @type debug: bool
  @return: True
  
  """
  tree = ElementTree()
  tree.parse(inputXML)
  params = tree.findall('global/parameter')
  lciolistfound = False
  for param in params:
    if param.attrib.has_key('name'):
      if param.attrib['name']=='LCIOInputFiles':
        lciolistfound = True
        param.text = inputSLCIO
      if len(numberofevts)>0:
        if param.attrib['name']=='MaxRecordNumber':
          if param.attrib.has_key('value'):
            param.attrib['value'] = numberofevts
      if param.attrib['name']=="GearXMLFile":
        if param.attrib.has_key('value'):
          param.attrib['value'] = inputGEAR
      if not debug:
        if param.attrib['name']=='Verbosity':
          param.text = "SILENT"
  if not lciolistfound:
    name = {}
    name["name"]="LCIOInputFiles"
    lciolist = Element("parameter",name)
    lciolist.text = inputSLCIO
    globparams = tree.find("global")
    globparams.append(lciolist)

  params = tree.findall('processor')
  for param in params:
    if param.attrib.has_key('name'):
      if len(outputREC)>0:
        if param.attrib['name']=='MyLCIOOutputProcessor':
          subparams = param.findall('parameter')
          for subparam in subparams:
            if subparam.attrib.has_key('name'):
              if subparam.attrib['name']=='LCIOOutputFile':
                subparam.text = outputREC
      if len(outputDST)>0:
        if param.attrib['name']=='DSTOutput':
          subparams = param.findall('parameter')
          for subparam in subparams:
            if subparam.attrib.has_key('name'):
              if subparam.attrib['name']=='LCIOOutputFile':
                subparam.text = outputDST

  
  tree.write(finalxml)
  return True

def PrepareMacFile(inputmac,outputmac,stdhep,nbevts,startfrom,detector=None,outputlcio=None,debug = False):
  """Writes out a mac file for SLIC
  
  Takes the parameters passed from L{SLICAnalysis} to define a new mac file if none was provided
  
  @param inputmac: name of the specified mac file
  @type inputmac: string
  @param outputmac: name of the final mac file used by SLIC
  @type outputmac: string
  @param stdhep: name of the generator file to use
  @type stdhep: string
  @param nbevts: number of events to process
  @type nbevts: string
  @param startfrom: event nu,ber to start from in the generator file
  @type startfrom: string
  @param detector: Detector model to use.  
  @type detector: string
  @param outputlcio: name of the produced output slcio file, this is useful when combined with setOutputData of ILCJob class
  @type outputlcio: string

  @return: True
  """
  inputmacfile = file(inputmac,'r')
  output = file(outputmac,'w')
  listtext = []
  for line in inputmacfile:
    if line.find("/generator/filename")<0:
      if line.find("/generator/skipEvents")<0:
        #if line.find("/run/initialize")<0:
        if line.find("/lcio/path")<0:
          if line.find("/run/beamOn")<0:
            if detector:
              if line.find("/lcdd/url")< 0:
                if outputlcio:
                  if line.find("/lcio/filename")<0:
                    #output.write(line)
                    listtext.append(line)
                else:
                  #output.write(line)
                  listtext.append(line)
            else :
              if outputlcio:
                if line.find("/lcio/filename")<0:
                  #output.write(line)
                  listtext.append(line)
              else: 
                #output.write(line)
                listtext.append(line)

  finaltext = string.join(listtext,"\n")
  finaltext += "\n"
  if detector:
    output.write("/lcdd/url %s.lcdd\n"%detector)
  #output.write("/run/initialize\n")
  if outputlcio:
    output.write("/lcio/filename %s\n"%outputlcio)
  output.write(finaltext)
  if len(stdhep)>0:
    output.write("/generator/filename %s\n"%stdhep)
  output.write("/generator/skipEvents %s\n"%startfrom)
  output.write("/run/beamOn %s\n"%nbevts)
  inputmacfile.close()
  output.close()
  return True

def PrepareLCSIMFile(inputlcsim,outputlcsim,inputslcio,jars=None,cachedir = None, debug=False):
  """Writes out a lcsim file for LCSIM
  
  Takes the parameters passed from LCSIMAnalysis
  
  @param inputlcsim: name of the provided lcsim
  @type inputlcsim: string
  @param outputlcsim: name of the lcsim file on which LCSIM is going to run, defined in L{LCSIMAnalysis}
  @type outputlcsim: string
  @param inputslcio: list of slcio files on which LCSIM should run
  @type inputslcio: list of string
  @param jars: list of jar files that should be added in the classpath definition
  @type jars: list of strings
  @param cachedir: folder that holds the cache directory, instead of Home
  @type cachedir: string
  @param debug: By default set verbosity to true
  @type debug: bool
  
  @return: string
  """
  printtext = ''

  tree = ElementTree()
  tree.parse(inputlcsim)
  ##handle the input slcio file list
  filesinlcsim = tree.find("inputFiles")
  if filesinlcsim:
    filesinlcsim.clear()
  else:
    baseelem = tree.find("lcsim")
    filesinlcsim = Element("inputFiles")
    baseelem.append(filesinlcsim)
  #set = Element("fileSet")
  for slcio in inputslcio:
    newfile = Element('file')
    newfile.text = slcio
    filesinlcsim.append(newfile)
  #filesinlcsim.append(set)

  if jars:
    if len(jars)>0:
      classpath = tree.find("classpath")
      if classpath:
        classpath.clear()
      else:
        baseelem = tree.find("lcsim")
        classpath = Element("classpath")    
        baseelem.append(classpath)
      for jar in jars:
        newjar = Element("jar")
        newjar.text = jar
        classpath.append(newjar)
        
  #handle verbosity
  if debug:
    debugline = tree.find("verbose")
    if debugline :
      debugline.text = 'true'
    else:
      control = tree.find('control')
      debugelem = Element('verbose')
      debugelem.text = 'true'
      control.append(debugelem)        

  if cachedir:
    cachedirline= tree.find("cacheDirectory")
    if cachedirline:
      cachedirline.text = cachedir
    else:
      control = tree.find('control')
      cachedirelem = Element("cacheDirectory")
      cachedirelem.text = cachedir
      control.append(cachedirelem)

  drivers = tree.findall("drivers/driver")      
  eventInterval = tree.find("drivers/driver/eventInterval")
  if eventInterval:
    evtint = eventInterval.text
    if int(evtint)<10:    
      eventInterval.text = "10"
  else:
    notdriver = True
    for driver in drivers:
      if driver.attrib.has_key("type"):
        if driver.attrib["type"]=="org.lcsim.job.EventMarkerDriver" :
          eventInterval = Element("eventInterval")
          eventInterval.text = "10"
          driver.append(eventInterval)
          notdriver = False
    if notdriver:
      drivers = tree.find("drivers")
      propdict = {}
      propdict['name']='evtMarker'
      propdict['type']='org.lcsim.job.EventMarkerDriver'
      eventmarker = Element("driver",propdict)
      eventInterval = Element("eventInterval")
      eventInterval.text = "10"
      eventmarker.append(eventInterval)
      drivers.append(eventmarker)
      execut = tree.find("execute")
      if(execut):
        evtmarkattrib = {}
        evtmarkattrib['name']="evtMarker"
        evtmark= Element("driver",evtmarkattrib)
        execut.append(evtmark)
        
  #drivers = tree.findall("drivers/driver")      

  mark = tree.find("drivers/driver/marker")
  if mark:
    printtext = mark.text
  else:
    for driver in drivers:
      if driver.attrib.has_key("type"):
        if driver.attrib["type"]=="org.lcsim.job.EventMarkerDriver" :
          marker = Element("marker")
          marker.text = "LCSIM"
          driver.append(marker)
          printtext = marker.text
  
  tree.write(outputlcsim)
  return printtext