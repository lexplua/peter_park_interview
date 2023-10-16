import base64
import json
import logging
import boto3

rekognition_client = boto3.client('rekognition')

logging.basicConfig(level=logging.INFO)

def detect_image_text(bytes):
    response = rekognition_client.detect_text(Image={'Bytes': bytes})
    return ' '.join(block['DetectedText'] for block in response['TextDetections'])

def handler(event, context):
    logging.info("OCR handler started")

    request_body = event['body']
    logging.info("Request body received")
    try:
        request_body = json.loads(request_body)
        image = request_body['image']
        logging.info("Encoded image retrieved from body")
        image_decoded = base64.b64decode(image)
        logging.info("Image bytes decoded")
        text = detect_image_text(image_decoded)
        lambda_response = {
            'statusCode': 200,
            'body': json.dumps({
                'text': text
            })
        }
        return lambda_response
    except Exception as e:
        lamda_response = {
            'statusCode': 400,
            'body': {
                'Error': "Exception during image processing",
                'ErrorMessage': str(e)
            }
        }
        return lamda_response
