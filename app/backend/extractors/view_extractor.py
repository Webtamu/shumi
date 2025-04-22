from .configs import FIELD_EXTRACTION_MAP, ITEM_TO_ACTION_KEY

class ViewExtractor:
    def __init__(self, view_map):
        self.view_map = view_map

    def extract_from_item(self, item_enum):
        action_key = ITEM_TO_ACTION_KEY.get(item_enum)
        if not action_key:
            raise ValueError(f"No action key mapped for item: {item_enum}")
        return self.extract(action_key)

    def extract(self, action_key):
        config = FIELD_EXTRACTION_MAP.get(action_key)
        if not config:
            raise ValueError(f"No extraction config for action: {action_key}")
        
        view = self.view_map.get(config["view"])
        if not view:
            raise ValueError(f"View not found for action: {action_key}")

        extracted = {}
        for field_name, item_enum in config["fields"].items():
            widget = view.item_map[item_enum]["instance"]
            extracted[field_name] = widget.text()

        return extracted
