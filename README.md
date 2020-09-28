# tr-05-oauth2-code-grant-example

The project is an example of using CTR OAuth2 API.

## Guide

Clone the repository

```bash
 git clone git@github.com:CiscoSecurity/tr-05-oauth2-code-grant-example.git
```

Install [Python 3.8.5](https://www.python.org/downloads/) 

Create virtualenv
```bash
python3 -m venv <your_venv_name>
```
Activate virtualenv:

- Mac OS/Linux: ```source <your_venv_name>/bin/activate``` 

- Windows  ```<your_venv_name>\Scripts\activate.bat```

From current directory install dependencies

```bash
pip install -r requirements.txt
```

Create client to get `CTR_CLIENT_ID` and `CTR_CLIENT_SECRET` via [Swagger UI](https://visibility.amp.cisco.com/iroh/oauth2-clients/index.html#/OAuth2Client/post_iroh_oauth2_clients_clients)

Send next payload by `/iroh/oauth2-clients/clients` (POST):
```javascript
{
  "scopes": [
    "integration",
    "admin",
    "inspect"
  ],
  "description": "Your description",
  "redirects": [
    "http://localhost:5000/auth",
    "http://127.0.0.1:5000/auth"
  ],
  "availability": "org",
  "name": "Your name",
  "grants": [
    "auth-code"
  ]
}
```
Then you will receive response body, where `id` is `CTR_CLIENT_ID` and `password` is `CTR_CLIENT_SECRET`


Set up environment variables:

For Mac OS / Linux:
```bash
export CTR_CLIENT_ID=<you generated cliend id>
export CTR_CLIENT_SECRET=<you generated secret password>
```

For Windows:
```cmd
set CTR_CLIENT_ID=<you generated cliend id>
set CTR_CLIENT_SECRET=<you generated secret password>
```

Run the next command:
```bash
flask run
```

To login via account from different region choose preferable region from drop-down
