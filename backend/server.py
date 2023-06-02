# flask server for the backend

from flask import Flask, request, jsonify

from flask_cors import CORS
import openai
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# api key
OPENAI_API_KEY = os.getenv("API_KEY")

# flask server for the backend

from flask import Flask, request, jsonify

from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# api key
OPENAI_API_KEY = "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"

# set the api key
openai.api_key = OPENAI_API_KEY

# handle /generate
@app.route("/generate", methods=["POST"])
def generate():
    # get the characteristics from the request
    characteristics = request.json["characteristics"]

    # create image prompts
    messages = [
        {
            "role": "system", 
            "content": "You are an assistant who is good at making background about the character."
        },
        {
            "role": "user",
            "content": "Make details about the character who is " + characteristics + "."
        },
    ]

    # create the prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    character_detail = response['choices'][0]['message']['content']
    print(character_detail)

    # create image prompts
    messages = [
        {
            "role": "system", 
            "content": "You are an assistant who is good at creating prompts for image creation for a character."
        },
        {
            "role": "assistant",
            "content": character_detail
        },
        {
            "role": "user", 
            "content": "Condense in 1 line up to 8 distinct descriptions focused on nouns and adjectives separated by ,. Give me 1 line only."
        }
    ]

    # create the prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    prompt = response['choices'][0]['message']['content']

    print(prompt)

    # create the image
    response = openai.Image.create(
        prompt=f"PFP NFT anime style, {prompt}",
        n=1,
        size="256x256",
    )

    image_url = response['data'][0]['url']

    # return the image url and the prompt
    return jsonify({"image_url": image_url, "character_detail": character_detail})

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

    # return the response
    return jsonify({"message": answer})

# start the server on port 5000
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
    


