from flask import Flask

import requests

# Import database module.
from firebase_admin import db

# Get a database reference to our blog.
#ref = db.reference('https://mhacks12-c37e8.firebaseio.com/')

#default_app = firebase_admin.initialize_app()
"""

users_ref = ref.child('users')
users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})


"""

url = "https://mhacks12-c37e8.firebaseio.com/users/.json"

payload = "{\n\t\"hello\": {\n\t\t\"hello2\": 12334\n\t}\n}"
headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "e7e1ce3d-c916-44fa-b94b-1b61bd6cb630,baf09016-fb5f-4fe6-899a-d1c0615ba294",
    'Host': "mhacks12-c37e8.firebaseio.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "36",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)
import pdb; pdb.set_trace()
print(response.text, flush=True)

app = Flask(__name__)





@app.route("/")
def hello():
    return "Hello World!"







#end
if __name__ == "__main__":
    app.run(port=5001)



