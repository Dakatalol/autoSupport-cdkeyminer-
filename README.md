# autoSupport[cdkeyminer]

Framework that performs UI tests against outages for cdkeyminer.com

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install autoSupport.

```bash
pip install pipenv
```
```bash
pipenv install
```
```bash
pipenv shell
```
Verify that C://Users/[YOUR_USER]/.virtualenvs is present with a folder inside with the following pattern: ​"autoSupport-cdkeyminer--.xxxxxxx"

Open your Pycharm -> File -> Settings ->
Project:[PROJECT_NAME]#->Settings_Button->Add->Virtual Environment->Existing Environnment and press the "..." button. Navigate to the  C://Users/[YOUR_USER]/.virtualenvs/autoSupport-cdkeyminer--.xxxxxxx/Scripts and select python.exe

## Running the tests

Run from inside project directory.

to run a specific test:
```
py.test tests/test_logins.py
```

Pytest can autodiscover all tests:
````
py.test C:\automation\automationSupport\tests
````

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.txt)