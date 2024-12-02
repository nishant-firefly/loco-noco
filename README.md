> Activate Venv
    python -m venv venv
        Powersehll :  .\venv\Scripts\Activate.ps1
        Cmd :  .\venv\Scripts\Activate.bat 

    python -m pip install --upgrade pip
> To Run test cases 
 Step 1 : Ensure services are running 
    python -m pip install -r .\sources\tests\requirements.txt
    python .\sources\tests\test_env_manager.py -h  | --status | --start | --stop
    python .\sources\tests\test_env_manager.py 
    docker rm -f $(docker ps -a -q -f "name=test_loco_") # Remove all service container 
 Step 2 : Ensure services are running 


