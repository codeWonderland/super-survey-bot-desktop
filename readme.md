# Super Survey Bot Desktop

## Installation
### Windows
Installation is really easy, just download the project and double click the SurveyBot.exe file

## Dev Setup
### Windows
Open powershell, navigate to the project directory, and type the following:

```
$ virtualenv venv --distribute
$ venv/Scripts/activate
$ pip install -r requirements.txt
```

### Unix Systems
Open a terminal, navigate to the project directory, and type the following:

```bash
$ virtualenv venv --distribute
$ source venv/bin/activate
$ pip install -r requirements.txt
```

To Disable Virtualenv:

```bash
$ deactivate
```

### Pycharm
Navigate to `File > Settings > Project > Project Interpreter`

Click on the dropdown next to project interpreter and select `Show All` and a new window will appear

Click the plus, select `Virtualenv` then select the `Existing Environment` button. Set the interpeter to `$PROJECTDIR/venv/bin/python`
