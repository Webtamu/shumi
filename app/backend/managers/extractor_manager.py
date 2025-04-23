from ..helpers import Items, ViewState

FIELD_EXTRACTION_MAP = {
    Items.LOGIN_LOGIN: {
        "view": ViewState.LOGIN,
        "fields": {
            "username": Items.LOGIN_USERNAME,
            "password": Items.LOGIN_PASSWORD
        }
    },
    Items.CREATE_ACCOUNT_CREATE: {
        "view": ViewState.CREATE,
        "fields": {
            "user": Items.CREATE_ACCOUNT_USERNAME,
            "email": Items.CREATE_ACCOUNT_EMAIL,
            "pass": Items.CREATE_ACCOUNT_PASSWORD,
            "confirm_pass": Items.CREATE_ACCOUNT_PASSWORD_CONFIRM
        }
    }
}


class ExtractorManager:
    def __init__(self, view_map):
        self.view_map = view_map

    def extract(self, item: Items) -> dict:
        extracted = {}
        config = FIELD_EXTRACTION_MAP.get(item, None)
        if not config:
            return extracted

        view = self.view_map.get(config["view"])

        for field_name, item_enum in config["fields"].items():
            widget = view.item_map[item_enum]["instance"]
            extracted[field_name] = widget.text()

        return extracted
