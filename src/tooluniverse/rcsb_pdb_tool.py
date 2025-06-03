import json
from rcsbapi.data import DataQuery
from base_tool import BaseTool


class RCSBTool(BaseTool):
    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.name = tool_config.get("name")
        self.description = tool_config.get("description")
        self.input_type = tool_config.get("type")
        self.search_fields = tool_config.get("fields", {}).get("search_fields", {})
        self.return_fields = tool_config.get("fields", {}).get("return_fields", [])
        self.parameter_schema = tool_config.get("parameter", {}).get("properties", {})

    def validate_params(self, params: dict):
        for param_name, param_info in self.parameter_schema.items():
            if param_info.get("required", False) and param_name not in params:
                raise ValueError(f"Missing required parameter: {param_name}")
        return True

    def prepare_input_ids(self, params: dict):
        for param_name in self.search_fields:
            if param_name in params:
                val = params[param_name]
                return val if isinstance(val, list) else [val]
        raise ValueError("No valid search parameter provided")

    def run(self, params: dict):
        self.validate_params(params)
        input_ids = self.prepare_input_ids(params)
        query = DataQuery(
            input_type=self.input_type,
            input_ids=input_ids,
            return_data_list=self.return_fields,
        )
        return query.exec()

### TESTING CODE
# if __name__ == "__main__":
#     pdb_id = "8A67"
#     entity_index = "1"
#     entity_id = f"{pdb_id}_{entity_index}"
#     assembly_id = f"{pdb_id}-1"
#     chem_comp_id = "ATP"

#     tool_file = "src/tooluniverse/data/rcsb_pdb_tools.json"

#     with open(tool_file, "r") as f:
#         tool_defs = json.load(f)

#     if not isinstance(tool_defs, list):
#         tool_defs = [tool_defs]

#     for i, tool_json in enumerate(tool_defs):
#         try:
#             tool = RCSBTool(tool_json)

#             params = {}
#             param_props = tool_json.get("parameter", {}).get("properties", {})

#             # Dynamically assign parameter values
#             if "pdb_id" in param_props:
#                 params["pdb_id"] = pdb_id
#             elif "entity_id" in param_props:
#                 params["entity_id"] = entity_id
#             elif "instance_id" in param_props:
#                 params["instance_id"] = f"{pdb_id}.A"
#             elif "assembly_id" in param_props:
#                 params["assembly_id"] = "1"
#             elif "chem_comp_id" in param_props:
#                 params["chem_comp_id"] = chem_comp_id
#             else:
#                 print(f"[SKIP] Tool #{i + 1} ({tool.name}): no supported parameters found.")
#                 continue

#             print(f"\n--- Running Tool #{i + 1}: {tool.name} ---")
#             output = tool.run(params)
#             print(json.dumps(output, indent=4))

#         except Exception as e:
#             print(f"[ERROR] Tool #{i + 1} ({tool_json.get('name', 'Unnamed')}): {e}")
