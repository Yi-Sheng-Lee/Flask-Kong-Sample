from flask import current_app


def return_response(status, data):
    try:
        # TODO flash token
        # new_token = reflash_token()
        new_token = ""
    except Exception as e:
        status = False
        current_app.logger.error(e, exc_info=True)
        data = e.args[0]
    finally:
        return {"status": status, "data": data}


def return_value(raw_dict, keys):
    return {key: value for (key, value) in raw_dict.items() if key in keys}
