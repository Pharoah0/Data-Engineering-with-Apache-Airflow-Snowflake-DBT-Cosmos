# Import our cosmos packages and use the ProfileConfig class to define the configuration for the Snowflake connection.
# This is using the SnowflakeUserPasswordProfileMapping class from Cosmos to map the Snowflake connection in Airflow to a dbt profile.
# The purpose of this is so we can leverage the Airflow connection UI instead of needing to add the connection via dbt, enabling us to manage all of our credentials from a single UI, instead of duplicating them.

from datetime import datetime
import os
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from pathlib import Path

dbt_project_path = Path("/usr/local/airflow/dags/cosmosproject")

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_conn",
        profile_args={"database": "DEMO_DBT", "schema": "PUBLIC"},
    ),
)


dbt_snowflake_dag = DbtDag(
    project_config=ProjectConfig(
        dbt_project_path,
    ),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
    ),
    schedule_interval="@daily",
    start_date=datetime(2023, 9, 10),
    catchup=False,
    dag_id="dbt_snowflake_dag",
)
