from flask import Flask, request
import json
from flask_cors import CORS

from apiclient import discovery
import httplib2
from oauth2client import client

from user_library import x

CLIENT_SECRET_FILE = 'client_secret.json'

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def hello():
    auth_code = request.get_json()
    
    credentials = client.credentials_from_clientsecrets_and_code(CLIENT_SECRET_FILE, ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'], auth_code)
    email = credentials.id_token['email']
    
    
    user_id = x(email)
    if user_id:
        print(user_id)
        return json.dumps(user_id)
    else: 
        print(user_id)
        return None
    
@app.route('/add_to_gh', methods=['POST'])
def add_to_gh(auth_code, user, profile_data):
    if request.headers['Secret-Header'] == 'abc':
        url = 'https://harvest.greenhouse.io/v1/prospects'
        headers = { 'Authorization': auth_code, "On-Behalf-Of": user}

        url = 'https://harvest.greenhouse.io/v1/prospects'
        post_data = json.dumps(profile_data)
        print(post_data)

        # print('adding to GH')
        add_candidate = requests.post(url, data=post_data, headers=headers)
        print('greenhouse response')
        print(add_candidate)
        candidate_text = json.loads(add_candidate.text)
        # print(candidate_text)
        try:
            candidate_id = candidate_text['id']
            application_id = candidate_text['applications'][0]['id']
            return {'candidate_id': candidate_id, 'application_id': application_id}
        except:
            print('Greenhouse error')
            return(candidate_text)

    

app.run(debug=True)