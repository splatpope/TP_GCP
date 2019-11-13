###############################
# 0. Set environment variables
###############################

PROJECT_ID="MON_PROJECT_ID"
PUB_SUB_TOPIC_NAME="MON_TOPIC"

##############################
# 1. Setup the environment
##############################

#Import libraries
from google.cloud import storage
from google.cloud import vision
from google.cloud import pubsub_v1



###########################################
# CREATE HERE BELOW YOUR LIBRARIES CLIENTS

## PubSub Client

## Cloud Vision client

###########################################

publisher = pubsub_v1.PublisherClient()
vision_client = vision.ImageAnnotatorClient()


#########################################################################################
# 2. Process with OCR the images that triggered the event
#########################################################################################

"""
Here, you will define the function that will be processed following the triggering event 
(e.g. the upload of an image into your bucket).

"""

# ----------------------------------------------------
# Process function
def process_image(file, context):
    """
    Cloud Function triggered by Cloud Storage when a file is changed.
    
    Args:
        file (dict): Metadata of the changed file, provided by the triggering
                                 Cloud Storage event.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to stdout and Stackdriver Logging

    """
    
    # Validate function request with parameters checkin
    bucket = file['bucket']
    name = file['name']

    #OCR the new picture
    detected_text = detect_text(bucket=bucket, filename=name)

    ######################################################
    #HERE, Publish to PubSub to trigger the next function
    topic_path = publisher.topic_path(PROJECT_ID, PUB_SUB_TOPIC_NAME)
    publisher.publish(topic_path, bytes(detected_text, encoding='utf-8'), image_name=name)


    ######################################################
#
# ----------------------------------------------------


# -----------------------------------------------------------------------
# Call the vision API to do OCR on the image
def detect_text(bucket, filename):

    """
    
    This function call the Vision API to apply OCR to the input image.

    Args:
        file (dict): Metadata of the changed file, provided by the triggering
                                 Cloud Storage event.
        context (google.cloud.functions.Context): Metadata of triggering event.

    Returns:
        The text read on the picture
    
    """
    #################################################
    # HERE, do the OCR by requesting to Vision API
    # Make sure to explore what is contained in the resulting object

	tdr = vision_client.text_detection({'source' : { 'image_uri' : 'gs://{}/{}'.format(bucket,filename)}})
	annotations = tdr.text_annotations
	rawResult = annotations[0].description
	
    return rawResult

    ########################################################
    
 
#
# ----------------------------------------------------
