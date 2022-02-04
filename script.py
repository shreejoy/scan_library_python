import os
import sys
import json

success, fail = [], []


def scan(fn, relevance, depth):
    if depth == 0:
        return {}

    func = eval(fn)
    result = dict()
    result[fn] = dict()
    result[fn]['func'] = dict()
    result[fn]['callable'] = callable(func)

    for _func in dir(func):
        if '_' in _func:
            continue

        if relevance:
            print(f"Want to continue with {fn}.{_func}?")
            resume = input(f"Enter yes or no > ").lower() == 'yes'
            if not resume:
                continue

        # print(f"Checking nested functions for {fn}.{_func}", end =" ")
        try:
            result[fn]['func'].update(
                scan(f"{fn}.{_func}", False, depth - 1))
            success.append(f"{fn}.{_func}")
        except Exception as e:
            # sys.exit(e)
            fail.append(f"{fn}.{_func}")

    return result


def render(dump):
    text = str()
    for key, value in dump.items():
        text += f"<details><summary>{key} (Callable: {value['callable']})</summary>"
        if isinstance(value, dict) and isinstance(value["func"], dict) and value['func']:
            text += render(value["func"])
        text += "</details>"
    return text


def save(dump, fn):
    if not os.path.exists(fn):
        os.makedirs(fn)

    template = open("template.html", "r").read()
    template = template.replace("{{content}}", render(dump))
    template = template.replace("{{title}}", fn)
    file = open(f"{fn}/index.html", "w")
    file.write(template)
    file.close()

    file = open(f"{fn}/dump.json", "w")
    file.write(json.dumps(dump, indent=4, sort_keys=False))
    file.close()


def main():
    func = input("Enter the function name to scan > ")
    depth = int(input("Enter the depth of scan > ") or 3)

    print("Would you like to decide the relevance of the base function/class?")
    relevance = input("Enter yes/no > ").lower() == "yes"

    try:
        eval(func)
    except NameError:
        try:
            globals()[func] = __import__(func)
        except ModuleNotFoundError:
            sys.exit("Invalid function")

    save(scan(func, relevance, depth), func)
    print(f"Completed scan for {func}:")
    print(f"\tSuccess: {len(success)}\n\tFail: {len(fail)}")
    print(f"Dump written to {func}.json")

    if len(fail) > 0:
        print("Failed for the following functions:", fail)

    print("Done")


if __name__ == "__main__":
    main()
