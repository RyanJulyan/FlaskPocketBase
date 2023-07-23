# FlaskPocketBase
An attempt at implementing an equivalent Flask  pocketbase (https://pocketbase.io/) an Open Source backend for your next SaaS and Mobile app. Features: Realtime database, Authentication, File storage, Admin dashboard, Extensions, Plugins

## Notes:
This is part of the natural progression from the Flask-BDA project found here: [https://github.com/RyanJulyan/Flask-BDA](https://github.com/RyanJulyan/Flask-BDA) and should be considered it's successor or alternative approach.


# Repos
## Replit
[https://replit.com/@RyanJulyan/FlaskPocketBase](https://replit.com/@RyanJulyan/FlaskPocketBase)
## Github
[https://github.com/RyanJulyan/FlaskPocketBase](https://github.com/RyanJulyan/FlaskPocketBase)

# Install Dev requirements

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you can search for "cmd" in your windows search
            * Right-click on the icon, and click on the "Run as administrator" option
                * You may need to navigate to your project when running as administrator `cd <Path To>/GAP_API`
```shell
cd <Path To>/FlaskPocketbaseApp

pip install --no-cache-dir -r requirements/dev.txt
```


**Note:** The `requirements.txt` references the `requirements/prod.txt` in the `requirements/` folder. To make sure you have the dev requirements please ensure you install `requirements/dev.txt` from the `requirements/` folder. 


### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
        * You may need to run "cmd" as administrator to run `pip install --upgrade pip`
            * To do this, you can search for "cmd" in your windows search
            * Right-click on the icon, and click on the "Run as administrator" option
                * You may need to navigate to your project when running as administrator `cd <Path To>/GAP_API`
```shell
cd <Path To>/FlaskPocketbaseApp

python -m venv venv

venv\Scripts\activate

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

set ENV=development
set FLASK_APP=app
set FLASK_DEBUG=1

python .\main.py
# flask --debug run --port 5000

```

# Adding Plugins
