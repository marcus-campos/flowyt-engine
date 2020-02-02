def loading(config):
    ascii_art = (
        "\n"
        "    ____           _               _                  _    \n"
        "   / __ \         | |             | |                (_)   \n"
        "  | |  | |_ __ ___| |__   ___  ___| |_ _ __ _   _ _____    \n"
        "  | |  | | '__/ __| '_ \ / _ \/ __| __| '__| | | |_  / |   \n"
        "  | |__| | | | (__| | | |  __/\__ \ |_| |  | |_| |/ /| |   \n"
        "   \____/|_|  \___|_| |_|\___||___/\__|_|   \__, /___|_|   \n"
        "                                           __/ /           \n"
        "                                          |___/            \n"
        "                                                           \n"
        "                                              By: Devyzi   \n"
    )
    print(ascii_art + "\n")
    print(
        " * Check available routes at {0}/_workspaces/routes".format(
            __host_name(config.get("HOST"), config.get("PORT"), config.get("PREFERRED_URL_SCHEME", "http"))
        )
    )


def __host_name(host, port, preferred_url_scheme):
    return "{0}://{1}:{2}".format(preferred_url_scheme, host, port)