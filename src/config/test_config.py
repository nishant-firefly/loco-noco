# Configuration settings for Docker and databases
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, "loco_noco", "data", "test_data.xlsx")

TEST_ENV_CONFIG = {
    "services": {
        "postgres": {
            "image": "postgres:13",
            "container_name": "test_loco_noco_postgres",
            "environment": {
                "POSTGRES_USER": "test_user",
                "POSTGRES_PASSWORD": "test_password",
                "POSTGRES_DB": "test_db",
            },
            "ports": {"5432": "5432"},  
            "healthcheck": {
                "test": ["CMD-SHELL", "pg_isready -U test_user -d test_db -p 5432"],
                "interval": 5,
                "retries": 5,
            },
            "resources": {
                "mem_limit": "256m",  # Limit memory to 256MB
                "cpus": "0.5",        # Limit to half a CPU
            },
        },
        # "mysql": {
        #     "image": "mysql:8",
        #     "container_name": "test_loco_noco_mysql",
        #     "environment": {
        #         "MYSQL_USER": "test_user",
        #         "MYSQL_PASSWORD": "test_password",
        #         "MYSQL_DATABASE": "test_db",
        #     },
        #     "ports": {"3306": "3306"},
        #     "command": "--default-authentication-plugin=mysql_native_password",
        #     "healthcheck": {
        #         "test": ["CMD", "mysqladmin", "ping", "-h", "localhost"],
        #         "interval": 5,
        #         "retries": 5,
        #     },
        #     "resources": {
        #         "mem_limit": "256m",  # Limit memory to 256MB
        #         "cpus": "0.5",        # Limit to half a CPU
        #     },
        # },
        # "oracle": {
        #     "image": "gvenzl/oracle-xe:21-slim",
        #     "container_name": "test_loco_noco_oracle",
        #     "environment": {
        #         "ORACLE_PASSWORD": "test_password",
        #         "APP_USER": "test_user",
        #         "APP_USER_PASSWORD": "test_password",
        #     },
        #     "ports": {"1521": "1521"},
        #     "healthcheck": {
        #         "test": ["CMD-SHELL", "echo 'SELECT 1 FROM DUAL;' | sqlplus test_user/test_password@localhost:1521/XEPDB1"],
        #         "interval": 10,
        #         "retries": 5,
        #     },
        #     "resources": {
        #         "mem_limit": "512m",  # Oracle requires more memory
        #         "cpus": "1.0",        # Limit to 1 CPU
        #     },
        # },
        # "mssql": {
        #     "image": "mcr.microsoft.com/mssql/server:2019-latest",
        #     "container_name": "test_loco_noco_mssql",
        #     "environment": {
        #         "ACCEPT_EULA": "Y",
        #         "SA_PASSWORD": "Test@1234",
        #     },
        #     "ports": {"1433": "1433"},
        #     "healthcheck": {
        #         "test": ["CMD", "/opt/mssql-tools/bin/sqlcmd", "-S", "localhost,1433", "-U", "SA", "-P", "Test@1234", "-Q", "SELECT 1"],
        #         "interval": 5,
        #         "retries": 5,
        #     },
        #     "resources": {
        #         "mem_limit": "512m",  # MSSQL also requires more memory
        #         "cpus": "1.0",        # Limit to 1 CPU
        #     },
        # },
        # "elasticsearch": {
        #     "image": "docker.elastic.co/elasticsearch/elasticsearch:7.17.10",
        #     "container_name": "test_loco_noco_elasticsearch",
        #     "environment": {
        #         "discovery.type": "single-node",
        #         "ES_JAVA_OPTS": "-Xms256m -Xmx256m",  # Reduce JVM heap size
        #     },
        #     "ports": {"9200": "9200"},
        #     "healthcheck": {
        #         "test": ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health"],
        #         "interval": 10,
        #         "retries": 5,
        #     },
        #     "resources": {
        #         "mem_limit": "512m",  # Minimum memory for Elasticsearch
        #         "cpus": "1.0",        # Limit to 1 CPU
        #     },
        # },
    }
}

