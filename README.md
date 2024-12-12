# Documentation for the project

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
    python -m pip install -r requirements.txt
#  Run all Test DBs (Prerequisite to run test cases) 
    $env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)" # For Powershell
    set PYTHONPATH=%PYTHONPATH%;%CD%  # For CMD 
    export PYTHONPATH=$(pwd) # bash to permanent set to ~/.bashrc | ~/.zshrc | ~/.config/fish/config.fish

    python .\tests\test_env_manager.py --start
# Other useful commands 
    python .\sources\tests\test_env_manager.py -h  | --status | --start | --stop
    python .\sources\tests\test_env_manager.py 
    docker rm -f $(docker ps -a -q -f "name=test_loco_") # Remove all service container 


     in my case (venv) D:\workspace\loco_noco_rdbms>set PYTHONPATH=%PYTHONPATH%;%CD%
    (venv) D:\workspace\loco_noco_rdbms\loco_noco>python .\tests\test_env_manager.py --start

   pytest tests/test_postgres.py
