import json, argparse, pathlib

SERVER_INFO_PATH = pathlib.Path("server_info.json")


def load_server_info():
    contentToRead = SERVER_INFO_PATH.read_text()
    return json.loads(contentToRead)


def get_server_info(variableName):
    global serverInfo
    try:
        data = serverInfo.get(variableName)
        print(data)
        return data
    except KeyError:
        raise KeyError


def update_server_info(variableNameAndValue):
    global serverInfo
    inputs = variableNameAndValue.split("/")
    if len(inputs) == 2:
        varName = inputs[0]
        value = int(inputs[1])
    else:
        raise ValueError("Invalid input. Valid form: [varName/Value]")
    
    try:
        # condition checks
        isValidPlayerCount = value >= 0 and varName == "player_count"
        isValidStateInput = (value < 2 and value >= 0) and varName == "server_state"
        # ---
        if isValidPlayerCount or isValidStateInput:
            serverInfo[varName] = value
        else:
            raise ValueError("Invalid input either that variable name doesn't exist or the value is out of range")
    except KeyError:
        raise KeyError("That variable name doesn't exist")


def reset_server_info():
    global serverInfo
    serverInfo = {
        "player_count": 0,
        "server_state": 0,
    }
    print("Reset success")


def save_server_info():
    writeInfo = json.dumps(serverInfo, indent=2)
    SERVER_INFO_PATH.write_text(writeInfo)


if __name__ == "__main__":
    serverInfo = load_server_info() #preloads server info

    parser = argparse.ArgumentParser(description="Server info manager")

    parser.add_argument("--reset", action="store_true", help="Resets the serverInfo dictionary and saves it to the json.")
    parser.add_argument("--update", help="Updates server info and saves it to the json.")
    parser.add_argument("--get", help="Gets server info corresponding to the variable name. [player_count, server_state]")

    args = parser.parse_args()

    if args.reset:
        reset_server_info()
        save_server_info()

    if args.update:
        update_server_info(args.update)
        save_server_info()

    if args.get:
        get_server_info(args.get)