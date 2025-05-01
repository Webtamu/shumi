from ..helpers import Items, ViewState

FIELD_EXTRACTION_MAP = {
    Items.LOGIN_LOGIN: {
        "view": ViewState.LOGIN,
        "fields": {
            "username": {"item": Items.LOGIN_USERNAME, "type": "text"},
            "password": {"item": Items.LOGIN_PASSWORD,  "type": "text"},
            "stay_signed_in": {"item": Items.LOGIN_STAY_SIGNED_IN, "type": "checkbox"}
        }
    },
    Items.CREATE_ACCOUNT_CREATE: {
        "view": ViewState.CREATE,
        "fields": {
            "user": {"item": Items.CREATE_ACCOUNT_USERNAME, "type": "text"},
            "email": {"item": Items.CREATE_ACCOUNT_EMAIL, "type": "text"},
            "pass": {"item": Items.CREATE_ACCOUNT_PASSWORD, "type": "text"},
            "confirm_pass": {"item": Items.CREATE_ACCOUNT_PASSWORD_CONFIRM, "type": "text"},
        }
    },
    Items.BEGIN_TAKE: {
        "view": ViewState.SUMMARY,
        "fields": {
            "notes": {"item": Items.SUMMARY_NOTES, "type": "edit_text"},
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

        for field_name, field_config in config["fields"].items():
            item_enum = field_config["item"]
            field_type = field_config["type"]

            if item_enum not in view.item_map:
                continue

            widget = view.item_map[item_enum]["instance"]
            if field_type == "text":
                extracted[field_name] = widget.text()
            elif field_type == "checkbox":
                extracted[field_name] = widget.isChecked()
            elif field_type == "edit_text":
                extracted[field_name] = widget.toPlainText()

        return extracted
