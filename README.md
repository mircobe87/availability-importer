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
The input file name is configured by the variable `AVAILABILITY_FILE`.
The calendar name is specified by the variable `CALENDAR_NAME`.

Check those 2 variables and run the main file `availability-importer.py`.
