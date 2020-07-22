from flask import request


def loading(config=None):
    ascii_art = (
        "    _____ _                     _       \n"
        "   |  ___| | _____      ___   _| |_     \n"
        "   | |_  | |/ _ \ \ /\ / / | | | __|    \n"
        "   |  _| | | (_) \ V  V /| |_| | |_     \n"
        "   |_|   |_|\___/ \_/\_/  \__, |\__|    \n"
        "                           |___/        \n"
        "                                        \n"
        "                              Engine      "
    )
    print(ascii_art + "\n")
    if config:
        print(
            " * Check available routes at {0}/_engine/workspaces/routes".format(
                __host_name(config.get("HOST"), config.get("PORT"), config.get("PREFERRED_URL_SCHEME", "http"))
            )
        )


def __host_name(host, port, preferred_url_scheme):
    if not host:
        host = "127.0.0.1"

    if not port:
        port = 5000
    return "{0}://{1}:{2}".format(preferred_url_scheme, host, port)
