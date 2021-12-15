
# Resizing of histograms by using generalization techniques

The goal of the design challenge is to automatically make small versions of a standard chart type by
creating a tool that would “adapt” a chart to a smaller size. 


## Installation

The project is written in Python 3.8 using the graph libraries which are present such as matplotlib.

```bash
  python3 -m venv 765-test
  source 765-test/bin/activate
  pip install -r requirements.txt
  python hist-vis.py --infile titanic.csv --column "Fare" --width 1
```
    
## Usage

Files:

data -- contains the csv files which are being visualized \
hist-vis.py -- The main file which is run to produce the visualization. \
requirements.txt -- Contains all the libraries which are necessary to run the project

### Arguments to run

infile -- The name of the csv file which is placed inside the data folder which is to be taken as input. Eg: wnba.csv \
column -- The name of the column which is to be used for making the histogram. Eg: Height \
width -- The width of the visualization that you want to make in inches Eg. 2 for 2"x2" visualization 

** Since we are making square visualizations and evaluating their performance, we are taking height = width and not asking for any height parameter as input 

### Command to run : 
python hist-vis.py --infile wnba.csv --column "Height" --width 2

#### Output :
![alt text](https://github.com/RoopaD30/CS765-Tiny-charts/blob/main/output.png?raw=true)


