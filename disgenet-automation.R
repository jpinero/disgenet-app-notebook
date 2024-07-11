# ©2024 MedBioinformatics Solutions SL
# Example script to illustrate the use of the Automation module of DISGENET Cytoscape App (https://apps.cytoscape.org/apps/disgenetapp)
# Before executing the script, ensure you have Cytoscape running and the DISGENET Cytoscape App installed 
# Requirements: httr, RCy3

if(!"RCy3" %in% installed.packages()){
  if (!requireNamespace("BiocManager", quietly=TRUE))
    install.packages("BiocManager")
  BiocManager::install("RCy3")
}
library(RCy3)

#Install and load the library httr
install.packages("httr")
library(httr)

# We will create an object for the REST calls to the DISGENET automation module. The parameters are:
# netType: A string containing the type of the network to be created (gene-disease-net,variant-disease-net)
# host: The host of the url.
# port: The listening port, by default 1234.
# version: currently v8 (the version can be checked in the version endpoint).
# The function returns a string in url format (url), with the given parameters.


disgenetRestUrl<-function(netType,host="127.0.0.1",port=1234,version="v8"){
  if(is.null(netType)){
    print("Network type not specified.")
  }else{
    url<-sprintf("http://%s:%i/disgenet/%s/%s",host,port,version,netType)
  }
  return (url)
}

# Creating the url for GDAs
disgenetRestUrl(netType = "gene-disease-net")

# Next, we will create an object that will execute the REST calls to the DISGENET automation module in Cytoscape and retrieve the operation results. The parameters are:
# netType: A string containing the type of the network to be created (gene-disease-net,variant-disease-net)
# netParams: A list with the parameters to create the network.
# The function returns the object result, a list with the results of the operation.

disgenetRestCall<-function(netType,netParams){
  url<-disgenetRestUrl(netType)
  restCall<-POST(url, body = netParams, encode = "json")
  result<-content(restCall,"parsed")
  return(result)
}

#Example search 1 GDA
geneDisParams <- list(
  source = "UNIPROT",
  geneProteinClass = "Kinase",
  diseaseSearch = " ",
  geneSearch = "BRAF",
  initialScoreValue = "0.8",
  finalScoreValue = "1.0"
)
# Generate the gene-disease network in Cytoscape
geneDisResult <- disgenetRestCall("gene-disease-net",geneDisParams)

#Example search 2 GDA
geneDisParams <- list(
  source = "CURATED",
  geneProteinClass = "ALL",
  diseaseClass = "Respiratory Tract Diseases",
  diseaseSearch = "Asthma",
  geneSearch = " ",
  initialScoreValue = "0.0",
  finalScoreValue = "1.0"
)

# Generate the gene-disease network in Cytoscape
geneDisResult <- disgenetRestCall("gene-disease-net",geneDisParams)

# Searching for VDA

# Example 1 VDA
variantDisParams <- list(
  source= "CURATED",
  diseaseClass = "Respiratory Tract Diseases",
  diseaseSearch= "Allergic asthma;Adult onset asthma;IgE-mediated allergic asthma",
  initialScoreValue= "0.0",
  finalScoreValue = "1.0",
  showGenes= "false"
)

# Generate the variant-disease network in Cytoscape
variantDisResult <- disgenetRestCall("variant-disease-net",variantDisParams)

# Change the layout of the network
layoutNetwork("kamada-kawai" , network = variantDisResult$networkResult$networkName)



