# **VascuSens**  
A python project to produce a visualisation of blockages in an artery, based on given data from SMART stents. The visualisation algorithms used are based off of the [pyEIT](https://github.com/liubenyuan/pyEIT) open-source framework. The software uses electrical impedance data from 16 electrodes, 8 positive and 8 negative, to produce a 2D Electrical Impedance Tomography visualisation.

## **Installation**
1. Clone the source code to your local machine using git:  
   - If you don't have git installed on your machine press the following [link]( https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to check/download git  
   - Make sure you are running Python 3.10 with `python --version`. If not, all active releases can be found [here](https://www.python.org/downloads/)
   - To clone the repository run the following code into your terminal:  
    <code>git clone https://stgit.dcs.gla.ac.uk/team-project-h/2021/cs33/cs33-main.git</code>  
   - run `pip install -r requirements.txt`  
    
    Alternatively, the source code zip file is available [here.](https://github.com/StamTheo28/EIT-Imaging-Python/archive/refs/heads/main.zip)

2. Install the executable Version:  
    ***Note*** The executable version works only on Windows 64-bit System  
    - Download the VascuSens installer on your machine by clicking on this [link](https://drive.google.com/file/d/1Hr9mUtghUvzLqqcHWFfcSue5nxPF_RyP/view?usp=drive_link) and pressing download on the Windows 64-bit Installer on the latest release. 
   - Run the msi installer that has just been downloaded  
   - Choose the install location of the app on your local machine  
   - At the chosen location, there will be a folder containing the executable file “VascuSensVis” and any data it needs. Do not remove the executable from the folder. Instead, create a shortcut on your desktop to the executable file, for example  
   - To run the app, simply run the executable file or any shortcuts made to it  

## **Documentation**
The Documents section shows how you can use the software using the GUI or the terminal. All appropriate documentation/demos on how to use them are located in this [link](https://stgit.dcs.gla.ac.uk/team-project-h/2021/cs33/cs33-main/-/wikis/Documentation%20&%20Demo).  

## **Data Format**
The data used must have the specific format below:  
- It must be a 33x80 xlsx file  
- The first row must be the Frequency from 20-100HZ  
- The other 32 rows for each column should be the impedance readings  
- The order of which data should be stored are explained below:
    - Positive nodes are marked as A and negative nodes as B:   
    [<img src="doc/data%20format/Clockface.png" width="500"/>](Clockface.png)  
    - There order is:  
    ![data_order](doc/data%20format/data_order.PNG)

## **Dependencies**
**Python 3.10 is required**  
| Dependencies | Version |
| ------ | ------ |
| numpy | >= 1.19.1 |
| scipy | >= 1.5.0 |
| matplotlib | >= 3.3.2 |
| pandas | >= 1.1.3 |
| openpyxl | |
| shapely | |
| pyeit | == 1.1.6 |

## **Examples**
Here are examples of the output of the software by using the two command line interface approaches  
***Note*** This requires you to clone the source code and cd into the /vascusense/ folder in your terminal  

1. Using GUI option:

Run the main python script with the --gui option, as in the following command <code> python main.py --gui </code>
### Example 1:
![Example1_gui](doc/examples/gui_example1_20%25_blockage.png)
### Example 2:  
![Example2_gui](doc/examples/gui_example2_50%25_blockage.png)

2. Using command line:

Run the main python script with optional arguments (note that INPUT_PATH is required), as in the following command <code> python main.py -i \[INPUT_PATH] -c \[FREQUENCY] -b \[BASELINE_PATH] -f \[FLATTEN] </code>

### Example 1:
<code> python main.py -i //data/Second_Set/Blockage_10.xlsx -c 20 -b //data/Second_Set/Baseline.xlsx </code>

![Example1_command](doc/examples/tetminal_example1_10%25_blockage.png)

### Example 2:
<code> python main.py -i //data/Second_Set/Blockage_5.xlsx -c 20 -b //data/Second_Set/Baseline.xlsx -f 1 </code>

![Example1_command](doc/examples/terminal_example2_5%25_blockage.png)


## **Current Development Team**  

| Name       | Student ID  | Email | Customer Role | SCRUM Role |
| ------ | ------ | ------ | ------ | ------ | 
| Luke Hopkins | 2447720h | 2447720h@student.gla.ac.uk | Variable | Variable | 
| Thomas McCausland  | 2472525m | 2472525m@student.gla.ac.uk | Variable | Variable |
| Yifei Yu | 2572252y | 2572252y@student.gla.ac.uk | Variable | Variable | 
| Stamatis Theocharous| 2380138t | 2380138t@student.gla.ac.uk | Variable | Variable | 

*Note: Customer Roles and SCRUM roles all vary between each Sprint in order for all members of the team to get hands-on experience in every role.*
