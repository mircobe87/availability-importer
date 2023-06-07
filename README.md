# Availability Importer
*python app to load availability shifts in a specific Google Calendar*

## Configuration File
The file `shifts.conf` tells to the program how all the valid shifts are.
```
# shift start[hh:mm] length[h]
      A        00:00         8
      B        08:00         8
      C        16:00         8
      D        00:00         9
      E        18:00         6
```

## Input Files
The program accepts in input a CSV file where each column specifys a day of the year in format DD/MM.
Here an example
```
1/6,2/6,3/6,4/6,5/6,6/6,7/6,8/6,9/6,10/6,11/6,12/6,13/6,14/6,15/6,16/6,17/6,18/6,19/6,20/6,21/6,22/6,23/6,24/6,25/6,26/6,27/6,28/6,29/6,30/6
   ,  A,   ,  B,   ,  D,   ,   ,   ,   B,    ,    ,   E,    ,   D,    ,   A,    ,    ,   E,    ,    ,    ,    ,   C,    ,    ,    ,   E,
```

## Usage
1. Clone this repository
2. Create a folder `.venv` inside the root project folder
3. Create the virtual environment:
      ```
      python -m venv /path/to/.venv
      ```
4. Activate the virtual environment running the proper script available in `.venv` folder
      Platform | Shell      | Command to activate virtual environment
      ---------|------------|----------------------------------------
      POSIX    | bash/zsh   | `$ source <venv>/bin/activate`
      POSIX    | fish       | `$ source <venv>/bin/activate.fish`
      POSIX    | csh/tcsh   | `$ source <venv>/bin/activate.csh`
      POSIX    | PowerShell | `$ <venv>/bin/Activate.ps1`
      Windows  | cmd.exe    | `C:\> <venv>\Scripts\activate.bat`
      Windows  | PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1`
5. Install all dependencies
      ```
      pip install -r requirements.txt
      ```
6. Run the application

```
usage: availability-importer.py [-h] [-c CALENDAR_NAME] EVENT_FILE

Load availability in google calendar.

positional arguments:
  EVENT_FILE            the CSV file coniainig event to upload.

options:
  -h, --help            show this help message and exit
  -c CALENDAR_NAME, --calendar CALENDAR_NAME
                        the name of calendar where you want to upload events.
```
