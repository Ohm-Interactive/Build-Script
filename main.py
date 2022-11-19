import os
import subprocess
import sys
import time
import json
from Util import print_color
indentLevel = 0
temp = ""
canRun = True
command_args = {"sleep": 1, "if": 3, "end": 0, "variable": 3}
variables = {}
totalOutput = ""
def checkQuotes(command , index):
    if command[index][0] != "\"" and command[index][-1] != "\"":
        return False
    elif command[index][0] == "\"" and command[index][-1] != "\"":
        print_color("Strings must be surronded by two quotes.", 255, 24, 8)
        exit(1)
    elif command[index][0] != "\"" and command[index][-1] == "\"":
        print_color("Strings must be surronded by two quotes.", 255, 24, 8)
        exit(1)
    else:
        return True
def main():
    fileName = sys.argv[1]
    jsonFile = ""
    buildTimeActon = None
    if os.path.isfile("config.json"):
        jsonFile = open("config.json", "r")
        buildTimeActon = json.load(jsonFile)["postCompileActon"]
    startTime = time.perf_counter()
    if os.path.isfile(fileName):
        file = open(fileName, "r")
        contents = file.read().replace("\t", "").split("\n")
        file.close()
        for i in contents:
            global indentLevel
            global temp
            global canRun
            global variables
            global totalOutput
            command = i.replace("\0", "").split(" ")
            emtpyQuotes = 0
            for j in command:
                if j == "":
                    emtpyQuotes += 1
            for j in range(emtpyQuotes):
                command.remove("")
            try:
                throwaway = command[0]
            except:
                continue
            if canRun and command[0] != "":
                if command[0] != "run" and command[0] != "log" and command[0] != "io":
                    argument = command_args[command[0]]
                    if len(command) - 1 != argument:
                        if argument == 1:
                            print_color("Invalid use of the " + command[0] + " function. It can only have 1 argument. " + str(len(command) - 1) + " were provided", 255, 24, 8)
                            exit(1)
                        else:
                            print_color("Invalid use of the " + command[0] + " function. It can only have " + str(argument) + " arguments. " + str(len(command) - 1) + " were provided", 255, 24, 8)
                            exit(1)
                if command[0] == "run":
                    fullcommand = ""
                    for j in range(len(command)):
                        if j == 0:
                            continue
                        fullcommand += command[j] + " "
                    if fullcommand == "":
                        print_color("Invalid use of the run function. It must take at least one argument. 0 were provided ", 255, 24, 8)
                        exit(1)
                    output = subprocess.run(fullcommand, stdout=subprocess.PIPE)
                    code = output.returncode
                    totalOutput += output.stdout.decode('utf-8')
                    if code == 1:
                        print_color("Build Terminated: error from " + command[1], 255, 24, 8)
                        exit(1)
                elif command[0] == "sleep":
                    time.sleep(int(command[1]))
                elif command[0] == "if":
                    comparsion1 = command[1]
                    operation = command[2]
                    comparison2 = command[3]
                    if operation == "==":
                        isTrue = comparsion1 == comparison2
                        if isTrue:
                            temp = indentLevel
                            indentLevel += 1
                        else:
                            canRun = False
                elif command[0] == "log":
                    item = command[1]
                    if not checkQuotes(command, 1):
                        item = variables[command[1]]
                    if len(command) == 3:
                        if command[2].lower() == "normal":
                            print(item)
                        elif command[2].lower() == "debug":
                            print_color(item, 51, 184, 100)
                        elif command[2].lower() == "warn":
                            print_color(item, 250, 250, 50)
                        elif command[2].lower() == "error":
                            print_color(item, 255, 24, 8)
                            exit(1)
                    else:
                        if len(command) < 2:
                            print_color("Invalid use of the log function. It must take one or two arguments. 0 were provided", 255, 24, 8)
                            exit(1)
                        elif len(command) > 2:
                            print_color("Invalid use of the log function. It must take one or two arguments." + str(len(command) - 1) + "were provided", 255, 24, 8)
                            exit(1)
                        print(item)
                elif command[0] == "variable":
                    if command[2] != "=":
                        print_color("Invalid use of variables. You must assign a varible when creating one.", 255, 24, 8)
                        exit(1)
                    if command[3] != "output":
                        variables[command[1]] = command[3]
                    else:
                        variables[command[1]] = totalOutput
                elif command[0] == "io":
                    if command[1] == "write":
                        if len(command) == 4:
                            if checkQuotes(command, 3):
                                open(command[2], "w").write(command[3][1:-1])
                            else:
                                open(command[2], "w").write(variables[command[3]])
                        else:
                            print_color("Invalid use of the io function. While writing to a file, there must be 4 arguments. " + len(command) - 1 + " were provided.", 255, 24, 8)
            if command[0] == "end":
                if indentLevel == temp:
                    indentLevel -= 1
                    canRun = True
        endTime = time.perf_counter() - startTime
        print_color("Build complete. Compile time: " + str(round(endTime, 1)) + "s", 51, 184, 100)
        if buildTimeActon != None:
            print_color("\nRunning Post Compile Action\n", 51, 184, 100)
            subprocess.run(buildTimeActon)
    else:
        print_color("File not found", 255, 24, 8)
        exit(1)
if __name__ == "__main__":
    main()