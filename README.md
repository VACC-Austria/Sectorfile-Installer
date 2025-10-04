This installer checks whether newer files are available on a server compared to the local ones.  
When the program starts, it first verifies if a newer version of the installer is available online.  

The main screen contains three control elements:  
- **Settings**  
  - Language  
  - Username  
  - VATSIM ID  
  - VATSIM Password  
  - VATSIM Rating  
  - Hoppie Code  
  - Audio Tool for VATSIM
- **Custom Files**  
- **Fresh Install**  
- **Start**  

When pressing **Fresh Install**:  
   - Download and install EuroScope  
   - Open GNG Webpage and open Sectorfile folder for extracting the GNG file 

When pressing **Start**, 2 different scenarios:
1.When Airac isn't Up to Date:
   - Check if the local EuroScope version matches the online version. If not, download and install EuroScope  
   - Check if the local sector file version matches the online version. If not, Open GNG Webpage and open Sectorfile folder for extracting the GNG file.  

2.When Airac is Up to Date:
   - Check if the local EuroScope version matches the online version. If not, download and install EuroScope  
   - Check if the local sector file version matches the online version.
   - Transfer custom files into the installed sector file  
   - Insert user data from settings into all profiles  
   - If multiple profiles exist, open the selection window and start EuroScope with the chosen profile  
   - Launch the audio tool for VATSIM  


**DEVELOPER**
all you must set is 
URL = "HTPP link where all your onlinefiles are stored"
FIR = "4-Letter Code of your FIR"
Packagename = "How the Correct Packagename is called at https://files.aero-nav.com/"
Testing = True or False, depenting if you are using this file as py or convert it into a exe file via auto-py-to-exe

**Required online Files**
- EuroScope.tff
- EuroScope.zip
- installerversion.txt
