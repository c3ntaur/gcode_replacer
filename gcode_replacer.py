import PySimpleGUI as sg
from tkinter import messagebox

def readInputFile(path):
    textObj = open(path).readlines()
    return textObj


def findAndReplace(StringToFind, StringToReplaceWith, gcodeData):
    i = 0
    replaceString = StringToReplaceWith
    findString = StringToFind
    for line in gcodeData:
        if(findString in gcodeData[i] ):
            gcodeData[i] = replaceString
            #gcodeData[i] = inputFileData[i]
        i += 1
    return gcodeData

def transformData(values):
    path = values[0]
    outputPath = path[0:(len(path)-6)] + "-TRANSFORMED.gcode"

    gcodeData = readInputFile(path)
    outputList = list()

    firstGcode2Replace = values[1]
    firstGcode2ReplaceWith = values[2]
    secondGcode2Replace = values[3]
    secondGcode2ReplaceWith = values[4]

    i = 0
    
    for line in gcodeData:
        if ("G4" in gcodeData[i]):
            pass
        else:
            outputList.append(gcodeData[i])
        i += 1

    outputList = findAndReplace(firstGcode2Replace,firstGcode2ReplaceWith + "\r", outputList)

    outputList = findAndReplace(secondGcode2Replace,secondGcode2ReplaceWith + "\r", outputList)

    #outputList.remove(len(outputList)-1)
    outputList.append("G1 X0 Y0\r")

    outputFileData = open(outputPath, "w")
    j = 1
    for line in outputList:
        #print(line.rstrip())
        outputFileData.write(line)
        j += 1

    outputFileData.close()


sg.theme("DarkTeal2")
#layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")], [sg.Button("Transform Gcode")]]

layout = [[sg.T("")], [sg.Text("Browse File: "), sg.Input(), sg.FileBrowse(key="-IN-")],
          [sg.Text('First GCODE to replace:'), sg.Input("M03")],
          [ sg.Text('First GCODE to replace with'), sg.Input("M03 S10")],
          [sg.Text('Second GCODE to replace:'), sg.Input("M05")],
          [ sg.Text('Second GCODE to replace with'), sg.Input("M03 S60")],
          [sg.Button("Transform Gcode")]]

###Building Window
window = sg.Window('GCODE-TRANSFORMER', layout, size=(600, 200))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Transform Gcode":
        try:
            #print(values[1])
            #print(type(values[1]))
            #print(type(values[2]))
            transformData(values)
            messagebox.showinfo(message="Hurra das hat geklappt", title="Info")
        except:
            messagebox.showinfo(message="Ach herrje das ist schief gelaufen", title="Info")