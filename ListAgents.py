import boto3

# Make sure boto3 is up-to-date: pip install --upgrade boto3
region = "us-west-2"   # change if your agent is in another region

# The AgentCore runtime + control plane are exposed via bedrock-agent and bedrock-agent-runtime
client = boto3.client("bedrock-agent", region_name=region)

def list_agents():
    try:
        response = client.list_agents()
        agents = response.get("agentSummaries", [])
        if not agents:
            print("⚠️ No AgentCore agents found in this region.")
        else:
            print("✅ Found agents:\n")
            for agent in agents:
                print(f"- Name: {agent['agentName']}")
                print(f"  Agent ID: {agent['agentId']}")
                print(f"  Latest Version: {agent.get('latestVersion', 'N/A')}")
                print(f"  Status: {agent.get('status', 'N/A')}")
                print()
    except Exception as e:
        print(f"⚠️ Error listing agents: {e}")

if __name__ == "__main__":
    list_agents()
