from azure.ai.ml import load_component
from azure.ai.ml import dsl, Input, Output
import os
import sys
from pipeline import *

pipeline_jobs = machine_failure_job()

sys.path.insert(1, '/Users/ejenamvictor/Desktop/project_new/modules')
#current_dir = os.path.dirname(os.path.abspath(__file__))
#src_dir = os.path.join(current_dir, '..', 'modules')
#sys.path.append(src_dir)

sys.path.insert(0, "../src/modules")

import aml_config_functions as aml

#from aml_config_functions import *
#from pipeline import *

#ml_client = aml.create_ml_client(tenant_id="0c039d92-dca1-4198-a5c5-9ff53dfe2ecb", 
#                     subscription_id="ec063bb6-60cf-44e6-ae24-d893fc75563e", 
#                     resource_group="practice", workspace_name="machinefailure")

ml_client = aml.create_ml_client()

#pipeline_jobs = machine_failure_job()

def submit_job():
# submit job to workspace
    jobs = ml_client.jobs.create_or_update(
    pipeline_jobs, experiment_name="machine_failure_pipeline_recent"
)
    return jobs

submit_job()
