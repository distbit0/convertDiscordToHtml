import pandas as pd
import time
from os import path
import json
import glob
import socket
import pyperclip
import subprocess
import os
import re

def getAbsPath(relPath):
    basepath = path.dirname(__file__)
    fullPath = path.abspath(path.join(basepath, relPath))

    return fullPath


def getConfig():
    configFileName = getAbsPath("./config.json")
    with open(configFileName) as config:
        config = json.loads(config.read())

    return config

def createHtmlFromCSV(csvFilePath):
    df = pd.read_csv(csvFilePath)
    firstMsg = re.sub(r"[^a-zA-Z ]", "", str(df["Content"][i]))
    firstMsg = firstMsg.lower()[:100]

    html = """
    <html>
    <head>
    <title>""" + firstMsg + """</title>
    <style>
    </style>
    </head>
    <body>
    """
    for i in range(len(df)):
        if pd.isna(df["Content"][i]):
            continue
        html += "<p>" + df["Username"][i] + ": " + df["Content"][i] + "</p>"
    html += """
    </table>
    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    config = getConfig()
    inputDir, outputDir = config["inputDir"], config["outputDir"]
    csvFilePaths = glob.glob(inputDir + "/Discord_chat*.csv")
    for csvFilePath in csvFilePaths:
        currentTime = str(time.time())
        htmlFilePath = outputDir + currentTime + ".html"
        html = createHtmlFromCSV(csvFilePath)
        with open(htmlFilePath, "w") as f:
            f.write(html)
        if config["htmlFolderUrl"]:
            hostname = socket.gethostname()
            localIP = socket.gethostbyname(hostname)
            urlToOpen = config["htmlFolderUrl"].replace("localhost", localIP) + currentTime + ".html"
            pyperclip.copy(urlToOpen)
        else:
            urlToOpen = htmlFilePath
        subprocess.run(["xdg-open", urlToOpen])
        os.remove(csvFilePath)
