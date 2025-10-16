# Sectorfile Installer
## Usage
Sectorfile Installer helps you set up Euroscope for your next session.

Simply Download the latest version from the [Releases page](https://github.com/VACC-Austria/Sectorfile-Installer/releases) and let it guide you through the setup.

Sectorfile Installer will tell you, when there is a newer Sectorfile available or when your VACC recommends you Upgrade your Euroscope to a newer version.

## Finding the Logs
Logs and other application data can be found in the AppData directory: `C:\Users\<your-user>\AppData\Local\SectorfileInstaller\session-launcher.log`

## Developers
### Setup
```
# set up a venv
py -m venv venv

# activate it
.\venv\Scripts\Activate.ps1

# install the dependencies
pip install -r requirements.txt

# install the dev dependencies
pip install -r requirements.dev.txt
```

To set up the configuration you want to use, you need a powershell with admin rights. Create a Symlink from `vacc` to your desired configuration directory by running the following command from the Repository root:
```powershell
New-Item -Path vacc -itemType SymbolicLink -Value vacc-austria

# Now run the app
python .\Session-Launcher.py
```

### Package
To locally test the package build, run the `build.bat` script. It will create the .exe file and put it into the dist/ folder.

To release a package, create a version tag (e.g. `v1.2.3`) and push it to the repository. A github action then builds the Package and creates a Release.
