from ..helpers.enums import Items, ViewState 

FIELD_EXTRACTION_MAP = {
    "login": {
        "view": ViewState.LOGIN,
        "fields": {
            "username": Items.LOGIN_USERNAME,
            "password": Items.LOGIN_PASSWORD
        }
    },
    "create_account": {
        "view": ViewState.CREATE,
        "fields": {
            "user": Items.CREATE_ACCOUNT_USERNAME,
            "email": Items.CREATE_ACCOUNT_EMAIL,
            "pass": Items.CREATE_ACCOUNT_PASSWORD,
            "confirm_pass": Items.CREATE_ACCOUNT_PASSWORD_CONFIRM
        }
    }
}

ITEM_TO_ACTION_KEY = {
    Items.LOGIN_LOGIN: "login",
    Items.CREATE_ACCOUNT_CREATE: "create_account"
}