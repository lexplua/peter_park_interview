import base64
import json

import boto3

rekognition_client = boto3.client('rekognition')


def detect_image_text(bytes):
    response = rekognition_client.detect_text(Image={'Bytes': bytes})
    return ' '.join(block['DetectedText'] for block in response['TextDetections'])

def handler(event, context):
    if 'image' not in event['body']:
        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": 'Missing `image` POST parameter',
                "ErrorMessage": f"Missing `image` POST parameter, only {event['body']} are present"
            }
        }
        return lambda_response
    request_body = event['body']

    try:
        request_body = json.loads(request_body)
        image = request_body['image']
        image_decoded = base64.b64decode(image)

        text = detect_image_text(image_decoded)
        lambda_response = {
            'statusCode': 200,
            'body': {
                'text': text
            }
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
