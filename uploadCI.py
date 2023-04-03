import json
import os
import requests

apiAddress = "http://127.0.0.1:8081/"
urlPrefix = apiAddress + "bot" + os.getenv("TELEGRAM_TOKEN")

def findString(sourceStr, targetStr):
    if str(sourceStr).find(str(targetStr)) == -1:
        return False
    else:
        return True

def genFileDirectory(path):
    files_walk = os.walk(path)
    target = {}
    for root, dirs, file_name_dic in files_walk:
        for fileName in file_name_dic:
            if findString(fileName, "arm64"):
                target["document"] = (fileName, open(path + "/" + fileName, "rb"))

    return target

def sendAPKs(path):
    file = genFileDirectory("./apks")

    parma = {
        "chat_id": os.environ.get("CHAT_ID"),
        "caption": "version: " + os.environ.get("VERSION_NAME") + "(" + os.environ.get("VERSION_CODE") + ")" + "\n" + os.environ.get("COMMIT_MESSAGE"),
    }

    print(parma)

    r = requests.post(urlPrefix + "/sendDocument", params=parma, files=file)

if __name__ == "__main__":
    startID = sendAPKs("./apks")