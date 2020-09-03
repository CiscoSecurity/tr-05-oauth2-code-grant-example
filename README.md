# tr-05-oauth2-code-grant-example

The project is an example of using CTR OAuth2 API.

## Guide

Clone the repository

```bash
 git clone git@github.com:CiscoSecurity/tr-05-oauth2-code-grant-example.git
```

Install [Python 3.8.5](https://www.python.org/downloads/) 

From current directory install dependencies

```bash
pip install -r requirements.txt
```

Set up environment variables

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