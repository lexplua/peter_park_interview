import base64
import boto3

rekognition_client = boto3.client('rekognition')


def detect_image_text(bytes):
    response = rekognition_client.detect_text(Image={'Bytes': bytes})
    return ' '.join(block['DetectedText'] for block in response['TextDetections'])


def handler(event, context):
    image = event.get('image', None)
    if image is None:
        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": 'Missing `image` POST parameter',
                "ErrorMessage": 'Missing `image` POST parameter'
            }
        }
        return lambda_response
    else:
        image_decoded = base64.b64decode(image)
        try:
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
