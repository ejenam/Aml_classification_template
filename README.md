# Aml_classification_template

This repo contains code for running an experiment on AML
SRC folder contains modules and various functions required to train and test scrips.
STEPS:
set up an azure resource group and workspace
use - az login- on the terminal to get your subscription id and tenant id
register the environment after replacing the azure credential with yours.
the dependency folder contains the environment required to run this experiment
use -python environment_register.py to register the environment
create the compute cluster. run the cluster.py file
Run the main.py to trigger the job.
