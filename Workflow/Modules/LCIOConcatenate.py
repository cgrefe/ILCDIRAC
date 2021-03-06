#####################################################
# $HeadURL$
#####################################################
"""
Module to concatenate LCIO files
@author: Chiong Bon Lam
@since: Dec 17, 2011
"""

__RCSID__ = "$Id$"

from DIRAC.Core.Utilities.Subprocess                      import shellCall
from ILCDIRAC.Workflow.Modules.ModuleBase                 import ModuleBase
from DIRAC                                                import S_OK, S_ERROR, gLogger
from ILCDIRAC.Core.Utilities.PrepareLibs                  import removeLibc
from ILCDIRAC.Core.Utilities.resolvePathsAndNames         import getProdFilename
import os

class LCIOConcatenate(ModuleBase):
  """ LCIO concatenate module
  """
  def __init__(self):

    super(LCIOConcatenate, self).__init__()

    self.STEP_NUMBER = ''
    self.log         = gLogger.getSubLogger( "LCIOConcatenate" )
    self.args        = ''
    self.result      = S_ERROR()
        
    # Step parameters

    self.applicationName = "lcio"
    #

    self.log.info("%s initialized" % ( self.__str__() ))

  def applicationSpecificInputs(self):
    """ Resolve LCIO concatenate specific parameters, called from ModuleBase
    """

    if not self.OutputFile:
      return S_ERROR( 'No output file defined' )
    
    if self.workflow_commons.has_key("IS_PROD"):
      if self.workflow_commons["IS_PROD"]:
        if self.workflow_commons.has_key('ProductionOutputData'):
          outputlist = self.workflow_commons['ProductionOutputData'].split(";")
          for obj in outputlist:
            if obj.lower().count("_sim_") or obj.lower().count("_rec_") or obj.lower().count("_dst_"):
              self.OutputFile = os.path.basename(obj)
        else:
          self.OutputFile = getProdFilename(self.OutputFile, int(self.workflow_commons["PRODUCTION_ID"]),
                                              int(self.workflow_commons["JOB_ID"]))

    return S_OK('Parameters resolved')

  def execute(self):
    """ Execute the module, called by JobAgent
    """
    # Get input variables

    self.result = self.resolveInputVariables()
    # Checks

    if not self.systemConfig:
      self.result = S_ERROR( 'No ILC platform selected' )

    if not self.result['OK']:
      return self.result

    if not os.environ.has_key("LCIO"):
      self.log.error("Environment variable LCIO was not defined, cannot do anything")
      return S_ERROR("Environment variable LCIO was not defined, cannot do anything")

    # removeLibc

    removeLibc( os.path.join( os.environ["LCIO"], "lib" ) )

    # Setting up script

    LD_LIBRARY_PATH = os.path.join( "$LCIO", "lib" )
    if os.environ.has_key('LD_LIBRARY_PATH'):
      LD_LIBRARY_PATH += ":" + os.environ['LD_LIBRARY_PATH']

    PATH = "$LCIO/bin"
    if os.environ.has_key('PATH'):
      PATH += ":" + os.environ['PATH']

    scriptContent = """
#!/bin/sh

################################################################################
# Dynamically generated script by LCIOConcatenate module                       #
################################################################################

declare -x LD_LIBRARY_PATH=%s
declare -x PATH=%s

lcio concat -f *.slcio -o %s

exit $?

""" % (
    LD_LIBRARY_PATH,
    PATH,
    self.OutputFile
)

    # Write script to file

    scriptPath = 'LCIOConcatenate_%s_Run_%s.tcl' % ( self.applicationVersion, self.STEP_NUMBER )

    if os.path.exists(scriptPath):
      os.remove(scriptPath)

    script = open( scriptPath, 'w' )
    script.write( scriptContent )
    script.close()

    # Setup log file for application stdout

    if os.path.exists(self.applicationLog):
      os.remove(self.applicationLog)

    # Run code

    os.chmod( scriptPath, 0755 )

    command = '"./%s"' % ( scriptPath )

    self.setApplicationStatus( 'LCIOConcatenate %s step %s' % ( self.applicationVersion, self.STEP_NUMBER ) )
    self.stdError = ''

    self.result = shellCall(
                            0,
                            command,
                            callbackFunction = self.redirectLogOutput,
                            bufferLimit = 20971520
                            )

        # Check results

    resultTuple = self.result['Value']
    status      = resultTuple[0]

    self.log.info( "Status after the application execution is %s" % str( status ) )

    return self.finalStatusReport(status)

