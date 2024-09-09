from typing import Dict


class CustomToolBase:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    def validate_params(self, params: Dict[str, any]):
        params_def = self.get_params_definition()
        for key, definition in params_def.items():
            if definition.required and key not in params:
                raise ValueError(f"Missing required parameter: {key}")
            if not isinstance(params[key], eval(definition.param_type)):
                raise ValueError(f"Incorrect type for parameter '{key}'. Expected {definition.param_type}.")
