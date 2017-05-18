from grader import *
import requests
import base64
import time

def getToken():
    authRequest = requests.post("https://-5mQz7uMmJcLfHOp6eKPCl3g57e1BhP9Fpy_duDn:pHkssPIL5qdQGkU_-9EvKWuzp-mrDXZa-35rf1bg@api.clarifai.com/v1/token/", data = {"grant_type": "client_credentials"}, verify = False)
    json_data = json.loads(authRequest.text)

    if "access_token" in json_data:
        return json_data["access_token"]
    else:
        return "Authentication Failure"

def generateHeader(authToken):
    return {"Authorization": "Bearer " + authToken}

#def decodeImage(imageb64):
#    with open(imageb64, 'rb') as f:
#        return f.read()

#def decodedImageToRealImage(decodedString, imageName):
#    with open(imageName, "wb") as fh:
#        fh.write(base64.decodestring(decodedString))

def openImage(imageName):
    return {"encoded_image": open(imageName, 'rb')}
    
def chooseDataClasses(classesList):
    return {"select_classes": classesList}

#Siia teha kontrollid, et kas JSON õigel kujul jne.
def parseResult(jsonResult):
    json_data = json.loads(jsonResult.text)
    print (json_data["results"][0]["result"]["tag"]["probs"])
    return max(json_data["results"][0]["result"]["tag"]["probs"])


@test
@set_description('Pildituvastus')
def do_test(m):
    
    authenticationToken = getToken()
    assert not (authenticationToken == "Authentication Failure"), "Autentimine ebaõnnestus - automaatkontroll hetkel ei tööta!"

    requestHeader = generateHeader(authenticationToken)
    
    #decodedImageToRealImage(decodeImage("screenshot.jpg.b64"), "screenshot.jpg")
    image = openImage("screenshot.jpg")
    
    dataClasses = chooseDataClasses(["flag"])

    #fileToCheck = {"encoded_image": open('screenshot.jpg', 'rb')}
    
    response = requests.post("https://api.clarifai.com/v1/tag/", files = image, data = dataClasses, headers = requestHeader, verify = False)
    #response = requests.post("https://api.clarifai.com/v1/tag/", files = fileToCheck, data = {"select_classes": "flag"}, headers = requestHeader, verify = False)
    finalResult = float(parseResult(response))*100
    finalResult = ("%.2f" % finalResult)
    
    with open(os.path.join(os.environ['HOME'], "testResult.txt"), "w") as f:
        f.write("Result: " + finalResult + "\n")
    
    assert (float(finalResult) >= 70), "Kahjuks ei suutnud pildituvastamise automaatkontroll Teie esitatud lahendusest piisavalt selgelt pilti välja lugeda. Teie pildituvastuse skoor oli " + finalResult + "%, kuid minimaalne skoor automaatseks arvestuseks on 70%. Teil on võimalik oma pildile lisada detaile, et seda oleks parem tuvastada. Kui soovite pildi nii jätta, siis hinnatakse Teie pilt käsitsi."
    #assert False, finalResult

