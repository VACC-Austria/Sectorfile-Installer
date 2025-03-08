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
- **Fresh Install**  
- **Start**  

When pressing **Fresh Install**, there are two different options:  

1. **Start Without User AIRAC Data**  
   - Download and install EuroScope  
   - Download and install the sector file  
   - Transfer custom files into the installed sector file  

2. **Start With User AIRAC Data**  
   - Check if the local "FS-Navigator 4.x" and "Global Air Traffic Control" AIRAC are installed  
   - Verify if the AIRAC matches the online version  
   - Download and install EuroScope  
   - Download and install the sector file  
   - Remove and replace VOR, NDB, FIX, Airport, Runway, SID, and STAR in the `.sct` section with "Global Air Traffic Control" AIRAC data (limited by `Setting.csv`)  
   - Remove and replace SID/STAR in the `.ese` section with "Global Air Traffic Control" AIRAC data (limited by `Setting.csv`)  
   - Transfer custom files into the installed sector file  

When pressing **Start**, there are two different options:  

1. **Start Without User AIRAC Data**  
   - Check if the local EuroScope version matches the online version. If not, download and install EuroScope  
   - Check if the local sector file version matches the online version. If not, download and install the sector file  
   - Transfer custom files into the installed sector file  
   - Insert user data from settings into all profiles  
   - If multiple profiles exist, open the selection window and start EuroScope with the chosen profile  
   - Launch the audio tool for VATSIM  

2. **Start With User AIRAC Data**  
   - Check if the local "FS-Navigator 4.x" and "Global Air Traffic Control" AIRAC are installed  
   - Verify if the AIRAC matches the online version  
   - Check if the local EuroScope version matches the online version. If not, download and install EuroScope  
   - Check if the local sector file version matches the online version. If not, download and install the sector file  
   - Remove and replace VOR, NDB, FIX, Airport, Runway, SID, and STAR in the `.sct` section with "Global Air Traffic Control" AIRAC data (limited by `Setting.csv`)  
   - Remove and replace SID/STAR in the `.ese` section with "Global Air Traffic Control" AIRAC data (limited by `Setting.csv`)  
   - Transfer custom files into the installed sector file  
   - Insert user data from settings into all profiles  
   - If multiple profiles exist, open the selection window and start EuroScope with the chosen profile  
   - Launch the audio tool for VATSIM  

**Possible online Files**
- settings.csv (required)
  - FIR
  - minLat
  - maxLat
  - minLon
  - maxLon
  - ownNavdata
    if user need own Navdata True/False
  - SidStarAirports
    For which Airport SIDSTAR should be created. example: LO create SIDSTARS for all Airports starting with LO
  - AirportRWY
    Which Airport should have runways in the runway selection dialog, same logic as SidStarsAirports
- EuroScope.tff (required)
- ProceduresCombiner.csv (required if OwnNavdata=True)
- Procedures.csv (optional)
- runways.csv (optional)
- waypoints.csv (optional)
