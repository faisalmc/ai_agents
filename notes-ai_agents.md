
# App creation on slack:
# tar on mac
tar -czvf archive_name.tar.gz file_or_directory [file_or_directory...]

tar -czvf agent-7.tar.gz agent-7

# test agent-7:
curl -sS http://localhost:8007/health

curl -sS -X POST http://localhost:8007/plan \
  -H 'Content-Type: application/json' \
  -d '{
    "config_dir": "configs.5",
    "task_dir":   "task-18.bfd",
    "hosts":      ["B-ASBR-1","C-ASBR-1"],
    "include_show_run": false
  }' | jq

curl -sS -X POST http://localhost:8007/capture \
  -H 'Content-Type: application/json' \
  -d '{
    "config_dir": "configs.5",
    "task_dir":   "task-18.bfd",
    "hosts":      ["B-ASBR-1","C-ASBR-1"]
  }'

@agent a7-plan configs.5 task-18.bfd
@agent a7-analyze configs.5 task-18.bfd



# agent-8

docker compose stop agent_8 && docker compose rm -f  agent_8  && docker compose up -d --build agent_8 

docker compose stop orchestrator_bot agent_8 && docker compose rm -f orchestrator_bot agent_8  && docker compose up -d --build orchestrator_bot agent_8 

docker compose stop orchestrator_bot agent_4 agent_8 agent_7 && docker compose rm -f orchestrator_bot agent_4 agent_8 agent_7 && docker compose up -d --build orchestrator_bot agent_4 agent_8 agent_7

**slack test for agent-8**
@agent triage BGP is flapping on C-ASBR-1
@agent triage run show ip bgp summary



**manual tests for agent-8:**
curl -s -X POST http://localhost:8008/triage/start \                                                                            
  -H "Content-Type: application/json" \
  -d '{"config_dir":"configs.5","task_dir":"task-18.bfd","host":"C-ASBR-1"}'   
  
curl -s -X POST http://localhost:8008/triage/ingest \
 -H "Content-Type: application/json" \
 -d '{"session_id":"1486e51469f94d34b9d4c74de60d1677","user_text":"BGP is flapping on site A"}'

# orchestrator
docker compose stop orchestrator_bot && docker compose rm -f orchestrator_bot  && docker compose up -d --build orchestrator_bot 

# agent-7

docker compose stop agent_7 && docker compose rm -f  agent_7  && docker compose up -d --build agent_7 


# docker -- same command for build and up
docker compose stop agent_2 && docker compose rm -f agent_2 && docker compose up -d --build agent_2


docker compose stop agent_1 && docker compose rm -f agent_1 && docker compose build --no-cache agent_1
docker compose up agent_1

docker compose stop agent_1 && docker compose rm -f agent_1 && docker compose up -d --build --no-cache agent_1

docker compose stop agent_7 && docker compose rm -f agent_7
docker compose up -d --build agent_7

docker compose stop agent_7 && docker compose rm -f agent_7 && docker compose up -d --build agent_7

docker compose stop agent_7 orchestrator_bot && docker compose rm -f agent_7 orchestrator_bot && docker compose up -d --build agent_7 orchestrator_bot


docker compose stop orchestrator_bot && docker compose rm -f orchestrator_bot && docker compose up -d --build orchestrator_bot

docker compose logs -f orchestrator_bot

docker compose down --remove-orphans
docker compose stop agent_4 && docker compose rm -f agent_4
docker compose up -d --build agent_4

docker compose up -d --build agent_2 orchestrator_bot agent_3
docker compose up -d --build agent_3
docker compose up -d --build agent_5 orchestrator_bot 

# docker -- separate build and up
docker compose down -v
docker compose down --remove-orphans
docker compose build --no-cache agent_2 orchestrator_bot
docker compose up -d agent_2 orchestrator_bot
docker compose exec orchestrator_bot sh -lc 'apk add --no-cache curl >/dev/null 2>&1 || true; curl -sf http://agent-2:8001/deploy || echo "OK: endpoint exists (will 405/422 on GET)"'
**OLD attempts**
docker compose build agent_2 orchestrator_bot

docker compose build --no-cache orchestrator
docker compose up -d orchestrator
docker compose exec orchestrator ls -l /app/slack_bot.py

docker compose up -d --build
docker-compose down

docker compose build orchestrator
docker compose up -d orchestrator

docker compose up -d orchestrator orchestrator_bot
docker compose logs -f orchestrator_bot

**Troublshooting**

docker compose exec orchestrator sh -lc 'python -c "import netmiko, paramiko; print(\"imports ok\")"'
docker compose exec agent_2 sh -lc 'echo "$SLACK_BOT_TOKEN" | sed "s/./&/g" | head -c 4; echo; echo "$SLACK_APP_TOKEN" | sed "s/./&/g" | head -c 4; echo'
* Prove the bot token works (you already did)
docker compose exec agent_2 python -c "from slack_sdk import WebClient;import os;print(WebClient(token=os.environ['SLACK_BOT_TOKEN']).auth_test())"

**ORCHESTRATOR_BOT**
docker compose exec orchestrator python slack_bot.py

docker compose exec orchestrator sh -lc \
  'curl -s -X POST http://localhost:8080/deploy -H "Content-Type: application/json" \
   -d "{\"config_dir\":\"configs.5\",\"task_dir\":\"task-1\",\"device_filter\":null,\"dry_run\":false}"'

*verify the handler in the running container (should show the minimal return):*
docker compose exec orchestrator sh -lc 'sed -n "/@app.post(\"\\/deploy\")/,/return/p" /app/app.py'



docker compose exec orchestrator_bot sh -lc '
ls -l /app/agents/agent-7/slack_ui.py || true
ls -l /app/ai_agents/agents/agent-7/slack_ui.py || true
python - <<PY
import importlib.util, sys
p="/app/agents/agent-7/slack_ui.py"
spec=importlib.util.spec_from_file_location("a7_slack_ui", p)
try:
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    print("OK:", hasattr(m,"build_overview_blocks"))
except Exception as e:
    print("IMPORT_ERR:", e)
PY'


docker compose exec orchestrator_bot sh -lc '
echo "A7_SLACK_UI_PATH=$A7_SLACK_UI_PATH";
python - <<PY
import os, importlib.util
p=os.getenv("A7_SLACK_UI_PATH","/app/agents/agent-7/slack_ui.py")
print("Using:", p)
spec=importlib.util.spec_from_file_location("a7_slack_ui", p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print("build_overview_blocks:", hasattr(m,"build_overview_blocks"))
PY'
**Checking agent-4 API**

* Expect: "Agent-4 HTTP API"
  
curl -sS http://localhost:8003/openapi.json | jq '.info.title'
curl -sS -X POST "$AGENT_7_URL/analyze" \
  -H 'Content-Type: application/json' \
  -d '{"config_dir":"configs.5","task_id":"task-18.bfd"}' | jq

* checking **Checking agent-4 API** from **agent-7** >> response: *{"status":"accepted"}*

docker compose exec agent_7 sh -lc 'curl -sS http://agent_4:8003/openapi.json | head'
curl -sS -X POST "$ORCH_A4_CAPTURE_URL" \
  -H 'Content-Type: application/json' \
  -d '{
    "config_dir":"configs.5",
    "task_id":"task-18.bfd",
    "overlay_ini_rel":"show_cmds.agent7.ini",
    "out_subdir":"agent7",
    "skip_grading": true,
    "hosts": ["B-ASBR-1","C-ASBR-1"],
    "dry_run": true
  }'

**Auth test inside agent_4 container (confirms workspace & token):**
docker compose exec agent_4 bash -lc \
'python - <<PY
import os
from slack_sdk import WebClient
cl=WebClient(token=os.environ["SLACK_BOT_TOKEN"])
print(cl.auth_test())
PY'

**Direct post by channel ID inside agent_4 (bypasses your app logic):**
docker compose exec agent_4 bash -lc \
'python - <<PY
import os
from slack_sdk import WebClient
cl=WebClient(token=os.environ["SLACK_BOT_TOKEN"])
resp=cl.chat_postMessage(channel=os.environ["SLACK_CHANNEL_ID"], text="Agent-4 → direct post sanity check")
print(resp)
PY'


docker compose exec agent_4 env | egrep 'SLACK_(BOT_TOKEN|APP_TOKEN|CHANNEL|CHANNEL_ID)'

# current implementation

current code for each agent based upon slash commands:
- agent2: /push-configs <configs_dir> <task-dir>
- agent3: /analyze-log <hostname> <configs_dir> <task-dir>
- agent4: /operational-check <config_dir> <task>
- agent5: /operational-analyze <config_dir> <task_dir>
- agent1: automatically runs and checks for github commits ... 

too long!  do not give long answers.  We want to do step by step approach.  remember this guideline!

	•	Four sub-agents (mapped to your Agents 1–4):
	1.	Agent-1 (Summarize/plan) – reads task YAML / repo and outputs a deployment plan.
	2.	Agent-2 (Deploy/Push) – this one wraps your existing Netmiko logic as an ADK Tool (imperative action).
	3.	Agent-3 (Quick log triage) – reads .log and flags CLI/commit errors.
	4.	Agent-4 (Deep analysis) – LLM-heavy diagnosis; can be triggered conditionally by 2/3.
	•	Slack ingress
Keep one Slack Bolt (Socket Mode) app (“orchestrator-bot”). It converts /deploy … or @orchestrator deploy … into a JSON payload, POSTs it to the ADK orchestrator’s /ingest endpoint, and relays progress + results back to Slack. (You’re no longer creating a separate slash command per agent.)

# Docker container
## orchestrator 

### Test for agent-2

curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{"task_id":"task-1","config_dir":"configs.5","task_dir":"task-2","device_filter":["A-PE-1"],"dry_run":true}'
    
    faisal@Faisals-MacBook-Pro ai_agents % curl -X POST http://localhost:8080/deploy \
      -H "Content-Type: application/json" \
      -d '{"task_id":"t1","config_dir":"configs.3.demo","device_filter":["A-PE-1"],"dry_run":true}'


curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{"task_id":"task-1","config_dir":"configs.5","task_dir":"task-18.bfd.bravo_charlie","dry_run":true}'

#### Test for agent-3 (to write agent3_<host>-analysis.json)

curl -X POST http://localhost:8002/analyze-host-json \
  -H "Content-Type: application/json" \
  -d '{"config_dir":"configs.5","task_id":"task-18.bfd.bravo_charlie","hostname":"A-ASBR-1"}'


docker compose exec orchestrator sh -lc 'python -c "import netmiko, paramiko; print(\"imports ok\")"'
