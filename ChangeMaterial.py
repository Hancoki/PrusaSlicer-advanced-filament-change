import re, sys, os

# Filenames
sourceFile = str(sys.argv[1])
fullPath = re.search(r'(^[A-Z].+).gcode', sourceFile)
outputFile = fullPath.group(1) + "_multi_color.gcode"

# Custom gcode for color change
comment = "; ### Change filament with Python ###"
beep = "M300 P1000 S4000"
parkingPos = "G0 X190 Y20"
pauseCommand = ";@pause"
nl = "\n"

# Temperature for filament change
preheatTemp = ""

# Temperatures for used filaments
filamentTemp = []
listIndex = 0

# Variables for testing
countExtr = 0
replaceTool = 0

# Search for defined temperatures and tool changes
searchForTemp = r'M104 S(\d{3}) T[1-9] ; set temperature'
searchForTool = r'^T[1-9]'

fileObjectIn = open(sourceFile)
fileObjectOut = open(outputFile, "w")

# Check material for preheat temperature
if "PLA" in sourceFile:
    preheatTemp = "220"
elif "PET" in sourceFile:
    preheatTemp = "250"

# Search and replace in gcode
for line in fileObjectIn:
    matchTemp = re.search(searchForTemp, line)
    matchTool = re.search(searchForTool, line)
    if matchTemp:
        countExtr += 1
        filamentTemp.append(matchTemp.group(1))
        fileObjectOut.write(line)
    elif matchTool:
        replaceTool += 1
        fileObjectOut.write(comment + nl + beep + nl + "G91" + nl + "M104 S" + preheatTemp + nl + "G0 Z15" + nl + "G90" + nl + parkingPos + nl + pauseCommand + nl + "M109 R" + str(filamentTemp[listIndex]) + nl + beep + nl + comment + nl)
        listIndex += 1
    else:
        fileObjectOut.write(line)

fileObjectIn.close()
fileObjectOut.close()

# Remove the sourcefile
os.remove(sourceFile)