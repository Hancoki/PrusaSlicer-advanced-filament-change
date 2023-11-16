import re, sys, os

# Input and output files
sourceFile = str(sys.argv[1])
fullPath = re.search(r'(.+).gcode', sourceFile)
outputFile = fullPath.group(1) + "_multi_color.gcode"
generateNewFile = False

# True - For using a print server (f.e. OctoPrint or Repetier Server) (default)
# False - For printing from SD card
usePrintServer = True

# Custom gcode for color change
nl = "\n"
comment = "; Change filament"
beep = "M300 P200 S500"         # Signal for filament change procedure
parkingPos = "X190 Y20"         # Define custom parking position
liftUpZ = "Z15"                 # Lift up the nozzle
if usePrintServer:
    pauseCommand = ";@pause"    # Pause command for printing via print server  
else:
    pauseCommand = "M25"        # Pause command for printing from SD

# Temperature for filament change
if "PET" in sourceFile:
    preheatTemp = "250"
else:
    preheatTemp = "220"

# Temperatures for used filaments (5 extruders by default)
filamentTemp = ["0","1","2","3","4"]

# Search for defined temperatures and tool changes
searchForTemp = r'M104 S(\d{3}) T(\d) ; set temperature'
searchForTool = r'^T(\d)'
ignoreFirstTool = False

# Open needed files
fileObjectIn = open(sourceFile)
fileObjectOut = open(outputFile, "w")

# Author comment
fileObjectOut.write("; This file was modified by Python script 'PrusaSlicer advanced filament change' by Hancoki." + nl)
fileObjectOut.write("; Find more information on https://github.com/Hancoki/PrusaSlicer-advanced-filament-change" + nl + nl)

# Search and replace in gcode
for line in fileObjectIn:
    matchTemp = re.search(searchForTemp, line)
    matchTool = re.search(searchForTool, line)
    if matchTemp:
        generateNewFile = True
        filamentTemp[int(matchTemp.group(2))] = matchTemp.group(1)
        fileObjectOut.write(line)
    elif matchTool:
        if ignoreFirstTool:
            fileObjectOut.write(comment + nl + beep + nl + "M104 S" + preheatTemp + nl + "G91" + nl + "G0 " + liftUpZ + nl + "G90" + nl + "G0 " + parkingPos + nl + pauseCommand + nl + "M109 R" + filamentTemp[int(matchTool.group(1))] + nl + beep + nl + comment + nl)
        else:
            fileObjectOut.write(line)
            ignoreFirstTool = True
    else:
        fileObjectOut.write(line)

# Close used files
fileObjectIn.close()
fileObjectOut.close()

# Remove unneeded file
if generateNewFile:
    os.remove(sourceFile)
else:
    os.remove(outputFile)