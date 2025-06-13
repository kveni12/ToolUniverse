import json
from rcsbapi.data import DataQuery
from base_tool import BaseTool
from rcsb_pdb_tool import RCSBTool  # Your defined tool wrapper

# Load all tool definitions
with open("src/tooluniverse/data/rcsb_pdb_tools.json", "r") as f:
    tool_defs = json.load(f)

if not isinstance(tool_defs, list):
    tool_defs = [tool_defs]

# Set up fixed test IDs for input
test_ids = {
    "pdb_id": "8A67",
    "entity_id": "8A67_1",
    "instance_id": "8A67.A",
    "assembly_id": "8A67-1",
    "chem_comp_id": "ATP"
}

# Run test cases for all tools
for i, tool_def in enumerate(tool_defs):
    try:
        tool = RCSBTool(tool_def)
        params = {}

        # Dynamically assign parameter values
        for param_name in tool.parameter_schema.keys():
            if param_name in test_ids:
                params[param_name] = test_ids[param_name]

        if not params:
            print(f"[SKIP] Tool #{i + 1} ({tool.name}): No supported parameters found in test_ids.")
            continue

        print(f"\n[{i + 1}] Running tool: {tool.name} with params: {params}")
        result = tool.run(params)

        print("✅ Success. Output preview:")
        print(json.dumps(result, indent=2)[:500])  # Print a snippet

    except Exception as e:
        print(f"❌ Failed. Tool #{i + 1} ({tool_def.get('name', 'Unnamed')}): {e}")
