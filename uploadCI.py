import json
import shutil
import time
import os
import requests

apiAddress = "http://127.0.0.1:8081/"
urlPrefix = apiAddress + "bot" + os.getenv("TELEGRAM_TOKEN", "")


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
                newFileName = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".apk"
                shutil.copyfile(
                    path + "/" + fileName, path + "/" + newFileName
                )
                target["document"] = (fileName, open(path + "/" + newFileName, "rb"))

    return target


def sendMetadataDesc():
    parma = {
        "chat_id": -1002135305446,
        "text": os.environ["COMMIT_MESSAGE"],
    }
    print(parma)
    response = requests.post(urlPrefix + "/sendMessage", params=parma)
    print(response.json())
    return response.json()["result"]["message_id"]


def sendApkToChat(path):
    file = genFileDirectory("./apks")

    parma = {
        "chat_id": os.environ.get("CHAT_ID"),
        "caption": "New Nnngram build. Congratulations!\n\nVersion: "
        + os.environ.get("VERSION_NAME", "")
        + "("
        + os.environ.get("VERSION_CODE", "")
        + ")"
        + "\n\nCommit message:\n"
        + os.environ.get("COMMIT_MESSAGE", ""),
    }

    print(parma)

    r = requests.post(urlPrefix + "/sendDocument", params=parma, files=file)
    print(r.json())


def sendAPKs(path):
    file = genFileDirectory("./apks")

    parma = {
        "chat_id": -1001848519901,
        "caption": "New Nnngram build. Congratulations!\n\nVersion: "
        + os.environ.get("VERSION_NAME", "")
        + "("
        + os.environ.get("VERSION_CODE", "")
        + ")"
        + "\n\nCommit message:\n"
        + os.environ.get("COMMIT_MESSAGE", ""),
    }

    print(parma)

    response = requests.post(urlPrefix + "/sendDocument", params=parma, files=file)
    print(response.json())
    return response.json()["result"]["message_id"] - 1


def sendMetadata(changesID, startID):
    parma = {
        "chat_id": -1002135305446,
        "text": str(os.getenv("VERSION_NAME"))
        + ","
        + str(os.getenv("VERSION_CODE"))
        + ","
        + str(startID)
        + ","
        + str(changesID)
        + ",false",
    }
    response = requests.get(urlPrefix + "/sendMessage", params=parma)


if __name__ == "__main__":
    changesID = sendMetadataDesc()
    sendApkToChat("./apks")
    startID = sendAPKs("./apks")
    sendMetadata(changesID, startID)
