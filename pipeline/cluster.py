import sys
sys.path.insert(0, "../src/modules")

from azure.ai.ml.entities import AmlCompute

ml_client = aml.create_ml_client()

cpu_compute_target = "cpu-cluster"

try:
    ml_client.compute.get(cpu_compute_target)
except Exception:
    print("Creating a new cpu compute target...")
    compute = AmlCompute(
        name=cpu_compute_target, size="STANDARD_E16S_V3", min_instances=0, max_instances=4
    )
    ml_client.compute.begin_create_or_update(compute).result