from mistralai import Mistral
from brave_api import get_compare_image
import base64
import os
from dotenv import load_dotenv

# Load environment variables from env.local
load_dotenv('env.local')

api_key = os.getenv("API_KEY")
model = "pixtral-12b-2409"
client = Mistral(api_key=api_key)


def encode_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# image_path = "./image.png"


def get_image_type(image_path):
    pointer = len(image_path) - 1
    file_extension = ""

    while image_path[pointer] != ".":  # im assuming the path is correct
        file_extension += image_path[pointer]
        pointer -= 1

    file_extension = file_extension[::-1]

    if file_extension == "jpeg":
        return "data:image/jpeg;base64"
    elif file_extension == "png":
        return "data:image/png;base64"


def describe_scan_and_verify(scan_image_path):
    list_image = encode_image_base64(scan_image_path)
    chat_response = client.chat.complete(
        model=model,
        top_p = 0.3,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the medical condition shown on the image only using words that you would put into a search engine to find the image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": f"{get_image_type(scan_image_path)},{list_image}",
                    },
                ],
            }
        ],
    )
    response1 = chat_response.choices[0].message.content
    image2_url = get_compare_image(response1)
    print(image2_url)

    chat_response2 = client.chat.complete(
        model=model,
        top_p = 0.3,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Here are two medical images. do they indicate the same condition? yes or no. Return a json with match_condition field (either true or false), explanation field explaining your decision and severity field with one of these values: [critical, moderate, healthy].",
                    },
                    {
                        "type": "image_url",
                        "image_url": f"{get_image_type(scan_image_path)},{list_image}",
                    },
                    {"type": "image_url", "image_url": f"{image2_url}"},
                ],
            }
        ]
    )
    response2 = chat_response2.choices[0].message.content
    print(response2, "response 2")
    return response1, response2

# similarity check of images
