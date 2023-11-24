from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input
from azure.ai.ml.dsl import pipeline
from azure.ai.ml import load_component
import sys

sys.path.insert(0, "../src/modules")

import aml_config_functions as aml


#parent_dir = ""
parent_dir = "../" 

# 1. Load components
prepare_data = load_component(source=parent_dir + "./data_prep.yaml")
train_model = load_component(source=parent_dir + "./train.yaml")
test_model = load_component(source=parent_dir + "./test.yaml")
#modules = load_component(source=parent_dir + "./modules.yaml")

ml_client = aml.create_ml_client()

#cpu_compute_target, cpu_cluster = aml.get_compute(ml_client, compute_name="cpu", vm_size="STANDARD_E16S_V3", min_instance=0, max_instances=4)


# 2. Construct pipeline
@pipeline()
def machine_failure_classification(pipeline_job_input,
                                  train_input,
                                  test_input,
                                  inference_output, 
                                  ):
    """Machine failure classification."""
    prepare_sample_data = prepare_data(raw_data=pipeline_job_input)
    train_with_sample_data = train_model(train_data=train_input)
    test_model_performance = test_model(test_data=test_input,
                                       model_input=train_with_sample_data.outputs.model_output,)
    #modules_pipeline = modules()
    return {
        "pipeline_job_prepped_data": prepare_sample_data.outputs.prep_data,
        "pipeline_job_model": train_with_sample_data.outputs.model_output,
        "pipeline_inference_data": test_model_performance.outputs.inference_df,
    }




def machine_failure_job():
    """
    Configure and return a machine failure classification pipeline job.

    This function sets up a machine learning pipeline for classifying machine failures. It defines inputs for the pipeline, configures output data access modes, and sets the default compute and datastore for the pipeline.

    The function assumes the existence of specific pipeline outputs ('pipeline_job_prepped_data', 'pipeline_job_train_data', 'pipeline_job_test_data') in the 'machine_failure_classification' pipeline.

    Returns:
    PipelineJob: A configured instance of the machine failure classification pipeline job.
    """
    
    pipeline_jobs = machine_failure_classification(
        pipeline_job_input = Input(type="uri_folder", path=parent_dir + "./data/"),
        train_input = Input(type="uri_folder", path=parent_dir + "./train_data/"),
        test_input = Input(type="uri_folder", path=parent_dir + "./test_data/"),
        inference_output = 'inference_data'
    )
    # demo how to change pipeline output settings
    #pipeline_jobs.outputs.pipeline_job_prepped_data.mode = "rw_mount"
    #pipeline_jobs.outputs.pipeline_job_train_data.mode = "rw_mount"
    #pipeline_jobs.outputs.pipeline_job_test_data.mode = "rw_mount"

    # set pipeline level compute
    pipeline_jobs.settings.default_compute = "cpu-cluster"
    # set pipeline level datastore
    pipeline_jobs.settings.default_datastore = "workspaceblobstore"
    return pipeline_jobs
