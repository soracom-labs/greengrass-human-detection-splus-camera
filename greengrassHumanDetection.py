import time
import boto3
import numpy as np
import picamera
import requests
import json
import io
import cv2
from threading import Timer

camera = picamera.PiCamera()

ml_endpoint_name = "human-detector-model"
runtime= boto3.client('runtime.sagemaker')

unified_endpoint = "http://unified.soracom.io"
harvest_files_endpoint = "http://harvest-files.soracom.io/camera_input.jpg"

# When deployed to a Greengrass core, this code will be executed immediately
# as a long-lived lambda function.  The code will enter the infinite while loop
# below.
def greengrass_human_detection_run():

    try: 
        payload = get_image_from_cam()

        #send image to SageMaker endpoint
        response = runtime.invoke_endpoint(EndpointName=ml_endpoint_name,
                                            ContentType='image/jpeg',
                                            Body=payload)

        predictions = json.loads(response['Body'].read().decode())
        print(predictions)

        #format data
        data = format_data(predictions)

        # send json data to Soracom Unified Endpoint
        requests.post(unified_endpoint, json=data)

        # send image to Harvest Files
        requests.post(harvest_files_endpoint, headers={'content-type': 'image/jpeg'}, data=payload)

    except Exception as e:
        print("Exception occured during prediction: ", e)

    # Asynchronously schedule this function to be run again in 60 seconds
    Timer(60, greengrass_human_detection_run).start()

# Formats prediction data before sending to Soracom
def format_data(predictions):
    num_predictions = len(predictions['input.jpg']['detections'])
    avg_confidence = 1.00

    if num_predictions > 0:
        total_confidence = 0
        for detection in predictions['input.jpg']['detections']:
            total_confidence += detection['confidence']

        avg_confidence = total_confidence / num_predictions

    predictions['nPeople'] = num_predictions
    predictions['avgConfidence'] = avg_confidence

    # Using the following lat and long as this device will not move
    # To get real lat and long estimate, get Cell Id from 
    # metadata.soracom.io/v1/subscriber and convert using an opensource
    # Cell ID converter
    predictions['lat'] = 47.6141522
    predictions['long'] = -122.2546382
    return predictions

#Captures an image from the PiCamera
def get_image_from_cam():
    stream = io.BytesIO()
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
    return stream.getvalue()

# Execute the function above
greengrass_human_detection_run()

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop
def function_handler(event, context):
    return
