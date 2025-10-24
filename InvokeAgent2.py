import boto3
import json
import uuid

region = "us-west-2"

# Dictionary of deployed AgentCore runtimes
AGENTS = {
    "job_market": "arn:aws:bedrock-agentcore:us-west-2:528160042459:runtime/Aether_CareerAlign-k67gL0GXm7",
    "course_catalog": "arn:aws:bedrock-agentcore:us-west-2:528160042459:runtime/Aether_CourseCrafter-TAW2Pv59hE",
    "career_matching": "arn:aws:bedrock-agentcore:us-west-2:528160042459:runtime/Aether_InsightSeeker-wLOAg5FONW",
    "project_advisor": "arn:aws:bedrock-agentcore:us-west-2:528160042459:runtime/Aether_ProjectAdvisor_LabubuLarry-iIO3XmDhRi"
}

client = boto3.client("bedrock-agentcore", region_name=region)

def invoke_agent(agent_key: str, prompt: str, session_id: str):
    agent_arn = AGENTS[agent_key]
    payload = json.dumps({"prompt": prompt}).encode()

    response = client.invoke_agent_runtime(
        agentRuntimeArn=agent_arn,
        runtimeSessionId=session_id,
        payload=payload
    )

    # Handle streaming
    ctype = response.get("contentType", "")
    if "text/event-stream" in ctype:
        content = []
        for line in response["response"].iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = line[6:]
                    print(data)
                    content.append(data)
        return "\n".join(content)

    elif ctype == "application/json":
        content = b"".join(response.get("response", []))
        return json.loads(content.decode("utf-8"))

    else:
        return response


if __name__ == "__main__":
    session_id = str(uuid.uuid4())
    current_agent = "career_matching"  # default

    print("✅ Connected to AgentCore")
    print("Available agents:", ", ".join(AGENTS.keys()))
    print("Type '/use agent_name' to switch.\n")

    while True:
        user_input = input(f"You ({current_agent}): ")
        if user_input.lower() in {"exit", "quit"}:
            break

        if user_input.startswith("/use "):
            new_agent = user_input.split(" ", 1)[1].strip()
            if new_agent in AGENTS:
                current_agent = new_agent
                print(f"🔀 Switched to {current_agent} agent.")
            else:
                print(f"⚠️ Unknown agent '{new_agent}'. Available: {', '.join(AGENTS.keys())}")
            continue

        reply = invoke_agent(current_agent, user_input, session_id)
        print(f"\n{current_agent} agent replied:\n{reply}\n")
