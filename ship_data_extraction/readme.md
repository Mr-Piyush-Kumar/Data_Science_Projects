## Project Name:- Ships Data Extraction

### Completed By:- Piyush Kumar   
   
In this project client wanted a script or application which can automatically extract the required data of ships from websites (balticshipping, marinetraffic, vesselfinder, myshiptracking and vesseltracking) using IMO numbers of ships provided in an excel file and store the extracted data in an excel file. I build an Python script using selenium and other basic Python libraries and converted it into an exe application using pyinstaller.    

<img src = "https://github.com/Mr-Piyush-Kumar/Mr-Piyush-Kumar/blob/master/ships.jpg"></img>  
   
The application takes list of IMO numbers as input and start searching of IMO numbers in balticshipping and extract data for those ships which IMO numbers are present in balticshipping and then script search for remaining IMO numbers in marinetraffic and extract data and so on. Please watch the below video to see the working of the script...   

https://user-images.githubusercontent.com/23153405/124519977-a7b9ac00-de08-11eb-8a07-0b445fdc05f4.mp4

### Files

1. imos.xlsx (List of IMO numbers for input).
2. ship_data.xlsx (Extracted data from websites).
3. imo_search_script.ipynb (script to search imo numbers in websites and extract ships data automatically).
