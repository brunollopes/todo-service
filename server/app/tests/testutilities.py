import sys
 
PRINT = False
 
def spinCommandLine( scriptName=None, commandLine=None ):
    """ This will turn test with spaces into a command line as if sys.argv. """
    sys_argv = []
    if not commandLine:
        return sys_argv
    sys_argv.append( scriptName )
    sys_argv.extend( commandLine.split( ' ' ) )
    return sys_argv
 
def turnOnPrinting( enable=False ):
    global PRINT
    PRINT = enable
 
CONSOLE_WIDTH = 80

def printTestCaseName( functionName ):
    global PRINT
    if not PRINT:
        return
    banner = '\nRunning test case %s ' % functionName
    length = len( banner )
    sys.stdout.write( banner )
    for col in range( length, CONSOLE_WIDTH ):
        sys.stdout.write( '-' )
    sys.stdout.write( '\n' )
    sys.stdout.flush()