import boto3

region = "us-west-2"  # change if your runtimes are in another region

# AgentCore control plane client
client = boto3.client("bedrock-agentcore", region_name=region)

def list_runtimes():
    try:
        response = client.list_agent_runtimes()
        runtimes = response.get("agentRuntimeSummaries", [])
        if not runtimes:
            print("⚠️ No AgentCore runtimes found in this region.")
        else:
            print("✅ Found runtimes:\n")
            for rt in runtimes:
                print(f"- Name: {rt['name']}")
                print(f"  ARN: {rt['agentRuntimeArn']}")
                print(f"  Status: {rt['status']}")
                print(f"  Created: {rt.get('creationTime')}")
                print()
    except Exception as e:
        print(f"⚠️ Error listing runtimes: {e}")

if __name__ == "__main__":
    list_runtimes()
