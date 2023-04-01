

#     Push management Zones to DynaTrace via API

### STEPS

### 1. Clone locally the remote repo from Github:
```
   git clone git@github.com:btrif/dynatrace-api.git

```
### 2. Install requirements:

```
pip install -r requirements.txt
```
 
### 3. Create a file .secrets.json into the root folder with the following data:
```   
.secrets.json

{
   "token_id": "dtXX01.TXXXXXXXXXXXXXXXXXXXXXXXxxV",
   "token_secret": "3XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXCG",
   "environment_id": "gss999999"
   }
```
You must replace the values with the good ones 
You generate a new token within the DynaTrace web console and replace the values with your new token data.
Observation: Token comes in the form :

<b>part1.part2.part3</b>,        three parts separated by dots.

- token_id - is part1.part2
- token_secret - is part3
- environment_id - is your id of your account.

Without these proper settings you cannot interact with the DynaTrace API.


### 4.  teams.yml file

If you have a new teams.yml file you replace the existing one into the root folder.


### 5. Run the application
<b>main.py</b> is the main executor of the entire (small) app.
It uses requests to GET, POST, UPDATE management zones.

When you run a prompter input will demand you to put the name
of the yml file. Put it in the root folder to work.

You can run it from the console :
```
> python main.py
```
or from your IDE.