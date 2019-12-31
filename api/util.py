## Utils package contains commonly used functions.
def Message(success, message):
    response_obect = {
        "success": success,
        "message": message,
    }
    return response_obect


def InternalErrResp():
    err = Message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500


def ErrResp(message, error_reason, code):
    err = Message(False, message)
    err["error_reason"] = error_reason

    return err, int(code)
