# LéXPLORE Secchi Depth Measurements

## Project Information

The data is collected within the frame of the [LeXPLORE project](https://wp.unil.ch/lexplore/) on Lake Geneva. 
The data is used and displayed on the [Datalakes website](https://www.datalakes-eawag.ch/).

## Sensors

The CTD is an instrument used to measure the conductivity, temperature, and pressure of the lake water (the D stands for "depth," which is closely related to pressure).

## Installation

:warning You need to have [git](https://git-scm.com/downloads) installed in order to successfully clone the repository.

- Clone the repository to your local machine using the command: 

 `git clone https://github.com/LeXPLORE-Platform/secchi-depth.git`
 
 Note that the repository will be copied to your current working directory.

- Use conda and install the requirements with:

`conda env create -f environment.yml`

## Usage

### Credentials

In order to download live data `creds_example.json` should be renamed to `creds.json` and completed.

### Operation

To run the pipeline: `python scripts/main.py`

The python script `scripts/main.py` defines the different processing steps while the python script 
`scripts/instruments.py` contains the instrument classes with all the corresponding class methods to process the data. 
To add a new processing or visualization step, a new class method can be created in the `instruments.py` file and the 
step can be added in `main.py` file. Both above-mentioned python scripts are independent of the local file system.

### Arguments

Run `scripts/main.py -h` for details on the input arguments available

## Data

### Access

Data for this repository is stored in a remote object store. In order to work with the data you need 
to run `scripts/download_remote_data.py`, this will syncronise the local `data` folder with the remote 
data folder on the server. 

### License

[![CC BY 4.0][cc-by-shield]][cc-by] 

This data is released under the Creative Commons license - Attribution - CC BY (https://creativecommons.org/licenses/by/4.0/). This license states that consumers ("Data Users" herein) may distribute, adapt, reuse, remix, and build upon this work, as long as they give appropriate credit, provide a link to the license, and indicate if changes were made.
 
The Data User has an ethical obligation to cite the data source (see the DOI number) in any publication or product that results from its use. Communication, collaboration, or co-authorship (as appropriate) with the creators of this data package is encouraged. 
 
Extensive efforts are made to ensure that online data are accurate and up to date, but the authors will not take responsibility for any errors that may exist in data provided online. Furthermore, the Data User assumes all responsibility for errors in analysis or judgment resulting from use of the data. The Data User is urged to contact the authors of the data if any questions about methodology or results occur. 

### Data Structure

The data can be found in the folder `data`. The data is structured as follows:

- **Level 0**: Raw data collected from the different sensors.
- **Level 1**: Data is converted to NetCDF and quality assurance is applied. Quality flag "1" indicates that the data point didn't pass the 
quality checks and further investigation is needed, quality flag "0" indicates that the data has passed the quality assurance check. Do not forget to apply the quality check mask when analysing the data.

## Quality assurance

Quality checks include but are not limited to range validation, data type checking and flagging missing data.
The automatic quality check is controlled by the package [Envass](https://pypi.org/project/envass/). The specific methods implemented for this dataset are listed in `notes/quality_assurance.json`. 