import requests
import json
import base64

def get_image_data(image_path):
    f = None
    with open(image_path, "rb") as image:
        f = image.read()

    return f

def get_image_description(image_path, vision_api_url, vision_api_key):
    url = vision_api_url
    image_bytes = get_image_data(image_path)

    headers = {"Prediction-Key": vision_api_key,
               "Content-Type": "application/octet-stream"}

    result = requests.post(url, data=image_bytes, headers=headers)
    predictions = json.loads(result.content)['predictions']
    description = get_best_tags(predictions)
    return description

def get_best_tags(predictions):
    tags = []
    for prediction in predictions:
        if prediction['probability'] > 0.6:
            tags.append('a "' + prediction['tagName'] + '"')

    tagStr = ", ".join(tags[i] for i in range(0, len(tags) - 1))
    if tagStr:
        tagStr += " and " + tags[-1]
    else:
        if not tags:
            for prediction in predictions:
                if prediction['probability'] > 0.28:
                    tags.append('a "' + prediction['tagName'] + '"')
            tagStr = ", ".join(tags[i] for i in range(0, len(tags) - 1))
        else:
            tagStr = tags[-1]
    return tagStr
