import os
import sys

from azure.identity import AzureCliCredential
from azureml.core.compute import AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core import Workspace
from azure.ai.ml.entities import Workspace
import json
from azure.ai.ml import MLClient


def create_ml_client():
    """
    Create an Azure Machine Learning workspace client.

    This function attempts to create an Azure Machine Learning workspace client using the provided parameters. If it fails
    to create a client, it generates a new configuration file with the provided parameters and tries again.

    Parameters:
        subscription_id (str): Azure subscription ID.
        resource_group (str): Azure resource group name.
        workspace_name (str): Azure Machine Learning workspace name.
        tenant_id (str, optional): Azure Active Directory tenant ID. Default is None.

    Returns:
        azureml.core.Workspace: An Azure Machine Learning workspace client.
    """
    # Create an Azure CLI credential
    credentials = AzureCliCredential(tenant_id="0c039d92-dca1-4198-a5c5-9ff53dfe2ecb")
    
    try:
        # Try to create the Azure Machine Learning workspace client using provided parameters
        ml_client = Workspace.from_config(auth=credentials)
    except Exception as ex:
        print("An error occurred while creating the AML client:", str(ex))
        print("Creating a new configuration file...")

        # Define the workspace configuration based on the provided parameters
        client_config = {
            "subscription_id": "ec063bb6-60cf-44e6-ae24-d893fc75563e",
            "resource_group": "practice",
            "workspace_name": "machinefailure",
        }
        

        # Write the configuration to a JSON file
        config_path = "../config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as fo:
            json.dump(client_config, fo)
        
        # Try to create the Azure Machine Learning workspace client again
        ml_client = MLClient.from_config(credential=credentials, path=config_path)
    return ml_client

from azure.ai.ml.entities import Workspace
