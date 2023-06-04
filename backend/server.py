# flask server for the backend

from flask import Flask, request, jsonify, Response

from flask_cors import CORS
import openai
import requests
from io import BytesIO
from PIL import Image
import pillow_avif
import boto3

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# api key
OPENAI_API_KEY = os.getenv("API_KEY")

voiceIds = {
    'Female': {
        'Child': ['Ivy'],
        'Adult': ['Joanna', 'Kendra', 'Kimberly', 'Salli', 'Ruth']
    },
    'Male': {
        'Child': ['Justin', 'Kevin'],
        'Adult': ['Joey', 'Matthew', 'Stephen']
    }
}

voiceIdNames = ['Ivy', 'Joanna', 'Kendra', 'Kimberly', 'Salli', 'Ruth', 'Justin', 'Kevin', 'Joey', 'Matthew', 'Stephen']


def synthesize_speech(text, voiceId, filename):
    polly_client = boto3.Session(
        region_name='us-west-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId=voiceId,
                                              OutputFormat='mp3',
                                              Text=text)
    audio_stream = response['AudioStream']

    file = open(filename, 'wb')
    file.write(response['AudioStream'].read())
    file.close()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# api key
OPENAI_API_KEY = "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"

# set the api key
openai.api_key = OPENAI_API_KEY

# handle /generate
@app.route("/generate", methods=["POST"])
def generate():
    # get image_url from the request
    image_url = request.json["image_url"]

    # get the characteristics from the request
    characteristics = request.json["characteristics"]

    # create image prompts
    messages = [
        {
            "role": "system", 
            "content": "You are an assistant who is good at making name and backgrounds about the character."
        },
        {
            "role": "user",
            "content": "Make details about the character who is " + characteristics + ".\n" + "Keep it breif."
        },
    ]

    # create the prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    character_detail = response['choices'][0]['message']['content']
    print(character_detail)

    messages.append({'role': 'assistant', 'content': character_detail})

    messages.append({'role': 'user', 'content': f'Choose one voice that is the best match.\n {voiceIds}'})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = response['choices'][0]['message']['content']

    # search for which voiceId is in the answer string
    for voiceId in voiceIdNames:
        if voiceId in answer:
            print(voiceId)
            break

    # get original image in PIL Image format
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # resize image
    image = image.resize((256, 256))

    # Convert the image to a BytesIO object
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()

    # create the image
    response = openai.Image.create_edit(
        image=byte_array,
        mask=open("bayc_mask.png", "rb"),
        prompt=f"No text on the background, {characteristics}",
        n=1,
        size="512x512",
    )

    image_url = response['data'][0]['url']

    # return the image url and the prompt
    return jsonify({"image_url": image_url, "character_detail": character_detail, "voice_id": voiceId, "answer": answer, "characteristics": characteristics})

# handle chat
@app.route("/chat", methods=["POST"])
def chat():
    # get the messages from the request
    messages = request.json["messages"]

    print(messages)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = response['choices'][0]['message']['content']

    # return the response (answer and speech)
    return jsonify({"message": answer})

@app.route('/synthesize', methods=['GET'])
def synthesize_speech():
    # get the text from the request
    text = request.args.get('text')
    voiceId = request.args.get('voiceId')

    polly_client = boto3.Session(
        region_name='us-west-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId=voiceId,
                                              OutputFormat='mp3',
                                              Text=text)

    audio_stream = response['AudioStream']

    def generate():
        for chunk in audio_stream:
            yield chunk

    return Response(generate(), mimetype='audio/mpeg')

# start the server on port 5000
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
    



