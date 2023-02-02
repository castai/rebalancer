from datetime import datetime, timedelta
from dis import dis
import requests
import time
import os
import logging

def get_savings_report(cluster_id, headers):
    url = "https://api.cast.ai/v1/kubernetes/external-clusters/{}/estimated-savings".format
    get_savings = requests.get(url=url(cluster_id), headers=headers)

    if get_savings.status_code != 200:
        print("Unable to retrieve savings report, exiting")
        exit
    if get_savings.json()["recommendations"]["Layman"]["savingsPercentage"] > os.environ("SAVINGS_THRESHOLD"):
        return True
    else:
        return False

def get_nodes(cluster_id, headers):

    url = "https://api.cast.ai/v1/kubernetes/external-clusters/{}/nodes".format
    get_nodes = requests.get(url=url(cluster_id), headers=headers)
    if get_nodes.status_code != 200:
        print("Unable to get node list, exiting")
        exit

    rebalance_nodes = {"minNodes": 0, "rebalancingNodes": []}

    for item in get_nodes.json()["items"]:
        node = {"nodeId": item["id"]}
        rebalance_nodes["rebalancingNodes"].append(node)
    return rebalance_nodes

def create_rebalance_plan(cluster_id, headers, nodes):

    url = "https://api.cast.ai/v1/kubernetes/clusters/{}/rebalancing-plans".format
    print(url(cluster_id))
    get_plan = requests.post(url=url(cluster_id), headers=headers, json=nodes)
    if get_plan.status_code != 202:
        print("Unable to create rebalance plan, exiting")
        print(get_plan)
        exit
    planId = get_plan.json()["rebalancingPlanId"]
    return planId

def run_rebalance_plan(cluster_id, headers, plan_id):
    print("Running rebalance planID: " + plan_id)

    url = "https://api.cast.ai/v1/kubernetes/clusters/{}/rebalancing-plans/{}/execute".format

    run_json = {"clusterId": cluster_id, "rebalancingPlanId": plan_id}
    run_plan = requests.post(url=url(cluster_id, plan_id), headers=headers, json=run_json)
    if run_plan.status_code != 202:
        print("Unable to run rebalance plan, exiting")
        print(run_plan)
        exit

def main():
    castai_api_token = os.environ["API_KEY"]
    cluster_id = os.environ["CLUSTER_ID"]
    headers={"Content-Type": 'application/json', "X-API-Key": castai_api_token}

    print("rebalancer running on cluster: " + cluster_id)

    if get_savings_report(cluster_id, headers):
        node_list = get_nodes(cluster_id, headers)
        plan_id = create_rebalance_plan(cluster_id, headers, node_list)
        time.sleep(60)
        run_rebalance_plan(cluster_id, headers, plan_id)
    else:
        print("Rebalancing is not needed at this time")

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print("action failed:" + str(err))
        exit(1)