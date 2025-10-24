
Step 1: Initiate the virtual environment to run the AWS code prompts
python -m venv .venv
.venv\Scripts\activate
pip install "bedrock-agentcore-starter-toolkit>=0.1.21" strands-agents boto3

Step 2: Establish unique agents via a starter file and basic requirements text file
Utilize python_starter_strands.py and requirements.txt
agentcore configure -e agentcore_starter_strands.py

#Interactive prompts you'll see:

1. Execution Role: Press Enter to auto-create or provide existing role ARN/name
2. ECR Repository: Press Enter to auto-create or provide existing ECR URI
3. Requirements File: Confirm the detected requirements.txt file or specify a different path 
4. OAuth Configuration: Configure OAuth authorizer? (yes/no) - Type `no` for this tutorial
5. Request Header Allowlist: Configure request header allowlist? (yes/no) - Type `no` for this tutorial
6. Memory Configuration:
  - If existing memories found: Choose from list or press Enter to create new
  - If creating new: Enable long-term memory extraction? (yes/no) - Type `yes` for this tutorial
  - Note: Short-term memory is always enabled by default

Step 3: Launch the agent and check its status if necessary
agentcore launch
agentcore status

Step 4: Invoke the agent to prompt it for a response to your chosen message
agentcore invoke "{\"prompt\": \"How am I going to survive this hackathon?\"}" 

 - If utilizing invocation file:
 - python InvokeAgent2.py

Step 5: Cleanup (if needed)
agentcore destroy

Removes:
  - AgentCore Runtime endpoint and agent
  - AgentCore Memory resources (short- and long-term memory)
  - Amazon ECR repository and images
  - IAM roles (if auto-created)
  - CloudWatch log groups (optional)

Step 6: Invoke the Agent to use its functionality
python InvokeAgent2.py
