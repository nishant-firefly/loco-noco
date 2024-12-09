
## Activate Virtual Environment
```bash
# Create a virtual environment  (One Time) 
python -m venv venv
# Powersehll :  .\venv\Scripts\Activate.ps1
# Cmd :  .\venv\Scripts\Activate.bat 
python -m pip install --upgrade pip
```
### To Run test cases 

```bash
#  Install Dependency (One Time) 
    python -m pip install -r .\sources\tests\requirements.txt
#  Run all Test DBs (Prerequisite to run test cases) 
    $env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)" # For Powershell
    set PYTHONPATH=%PYTHONPATH%;%CD%  # For CMD 
    export PYTHONPATH=$(pwd) # bash to permanent set to ~/.bashrc | ~/.zshrc | ~/.config/fish/config.fish

    python .\sources\tests\test_env_manager.py --start
# Other useful commands 
    python .\sources\tests\test_env_manager.py -h  | --status | --start | --stop
    python .\sources\tests\test_env_manager.py 
    docker rm -f $(docker ps -a -q -f "name=test_loco_") # Remove all service container 
```
python main.py