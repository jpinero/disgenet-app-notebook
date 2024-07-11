'''
2024 MedBioinformatics Solutions SL
Example script to illustrate the use of the Automation module of DISGENET Cytoscape App
Before executing the script, ensure you have Cytoscape running and the DISGENET Cytoscape App installed
'''
import json

import requests



def disgenetRestUrl(netType,host="127.0.0.1",port=1234,version="v8"):
    """
    We will create an object for the REST calls to the DISGENET automation module. The parameters are:
    netType: A string containing the type of the network to be created (gene-disease-net,variant-disease-net)
    host: The host of the url.
    port: The listening port, by default 1234.
    version: currently v8 (the version can be checked in the version endpoint).
    The function returns a string in url format (url), with the given parameters.
    """
    url = "http://"+host+":"+str(port)+"/disgenet/"+version+"/"+netType
    return url


def disgenetRestCall(netType,netParams):
    """
    Next, we will create an object that will execute the REST calls to the DISGENET automation module in Cytoscape
    and retrieve the operation results. The parameters are:
    netType: A string containing the type of the network to be created (gene-disease-net,variant-disease-net)
    netParams: A list with the parameters to create the network.
    The function returns the object result, a list with the results of the operation.
    """
    url = disgenetRestUrl(netType)
    HEADERS = {'Content-Type': 'application/json'}
    restCall = requests.post(url,data=json.dumps(netParams),headers=HEADERS)
    result = restCall.json()
    return result

def printHash(hashToPrint):
    """Prints all the key-values found in a python dictionary(hash) with a single line for entry and the format key - value.
    @param hashToPrint hash to be printed.
    """
    for key, value in hashToPrint.items():
        print(key+" - "+value)
        
def printOperationResult(operationResult):
    """Prints the response of the REST call to the DISGENET automation module.
    @param hashToPrint hash to be printed.
    """
    message = operationResult["message"]
    print(message)
    if 'networkResult' in operationResult:
        netResult = operationResult["networkResult"]
        printHash(netResult)
    elif 'errors' in operationResult:
        errors = operationResult["errors"]
        printHash(errors)
        
#Example of params for the gene-disease network.
geneDisParams = {
    "source" : "UNIPROT",
    "diseaseClass": "Neoplasms",
    "geneProteinClass" : "Kinase",
    "diseaseSearch" : "",
    "geneSearch" : "BRAF",
    "initialScoreValue" : "0.0",
    "finalScoreValue" : "1.0"
    }

#Generate the gene-disease network, and show the resuland show the results.ts.
printOperationResult(disgenetRestCall("gene-disease-net", geneDisParams))

geneDisParams = {
    "source" : "CURATED",
    "diseaseClass": "ALL",
    "geneProteinClass" : "ALL",
    "diseaseSearch" : "Asthma",
    "geneSearch" : " ",
    "initialScoreValue" : "0.0",
    "finalScoreValue" : "1.0"
    }


#Generate the gene-disease network, and show the resuland show the results.ts.
printOperationResult(disgenetRestCall("gene-disease-net", geneDisParams))


#Example of params for the variant-disase network.
variantDisParams = {
    "source" : "ALL",
    "diseaseClass": "Respiratory Tract Diseases",
    "diseaseSearch" : "Allergic asthma;Adult onset asthma;IgE-mediated allergic asthma",
    "geneSearch" : " ",
    "variantSearch" : " ",
    "initialScoreValue" : "0.0",
    "finalScoreValue" : "1.0",
    "showGenes" : "false"
    }

#Generate the variant-disease network, and show the results.
printOperationResult(disgenetRestCall("variant-disease-net", variantDisParams))
