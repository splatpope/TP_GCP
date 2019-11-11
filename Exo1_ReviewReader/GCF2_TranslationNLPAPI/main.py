###############################
# 0. Set environment variables
###############################

TARGET_LANGUAGE="en"
DESTINATION_BUCKET="LE_NOM_DE_VOTRE_BUCKET_DE_DESTINATION"

##############################
# 1. Setup the environment
##############################

#Import libraries
from google.cloud import storage
from google.cloud import translate
from google.cloud import language

from google.protobuf.json_format import MessageToDict

import datetime, base64, json, os


###########################################
# CREATE HERE BELOW YOUR LIBRARIES CLIENTS

## Translation client

## NLP client

## Storage client

###########################################


#########################################################################################
# 2. Process with OCR the images that triggered the event
#########################################################################################

"""
Here, you will define the function that will process the received PubSub message. First, use Translate API
to retreive the text original language then translate it to the language you choose.

"""
# ----------------------------------------------------
# PubSub reception function
def process_text(event, context):
    
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    
    text_to_analyze = base64.b64decode(event['data']).decode('utf-8')
    original_image=event["attributes"]["image_name"]
    original_image_export_name=original_image[0:-4]+".json"

    #Analyze the text received with Translate API
    result=analyzeText(text_to_analyze)

    #Extract timestamp from filename
    timestamp=extractTimestamp(original_image)

    #Add timestamp and original text to result dictionnary
    result["timestamp"]=timestamp
    result["originalText"]=text_to_analyze

    #Write result to JSON before writing to Google Cloud Storage (we have to do it)
    with open("/tmp/myJson.json", 'w') as f:
        json.dump(result, f)
	
    
    #############################################
    # HERE, write the JSON file to your bucket




    ##############################################
    

#
# ----------------------------------------------------


# ----------------------------------------------------
# Translate / NLP API Processing function
def analyzeText(text):

    # HERE, detect language and translate to English
    
    


    # HERE, use NLP API to detect sentiment and entities
    

    # Compile everything in a dictionnary and return it
    result={}
    result["originalLanguage"]=detectedLanguage
    result["translatedTextInEnglish"]=translatedText
    result["entities"]=MessageToDict(response_entities)
    result["sentiment"]=MessageToDict(response_sentiment)

    return result


# ----------------------------------------------------
# Extract timestamp from filename
def extractTimestamp(filename):

    date=filename[0:-4]
    date_time_obj = datetime.datetime.strptime(date, '%y_%m_%d')
    return str(date_time_obj.date())