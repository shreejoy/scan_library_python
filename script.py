import sys
import json

success, fail = [], []
def scan(fn, depth):
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
        # print(f"Checking nested functions for {fn}.{_func}", end =" ")
        try:
            result[fn]['func'].update(scan(f"{fn}.{_func}", depth - 1))
            success.append(f"{fn}.{_func}")
        except Exception as e:
            # sys.exit(e)
            fail.append(f"{fn}.{_func}")
            
    return result

def main():
    func = input("Enter the function name to scan > ")
    depth = int(input("Enter the depth of scan > ") or 3)
    
    try:
        eval(func)
    except NameError:
        try:
            globals()[func] = __import__(func)
        except ModuleNotFoundError:
            sys.exit("Invalid function")

    dump = scan(func, depth)
    dump = json.dumps(dump, indent = 4, sort_keys = False)
    file = open(f"{func}.json", "w")
    file.write(dump)
    file.close()
    print(f"Completed scan for {func}:\n\tSuccess: {len(success)}\n\tFail: {len(fail)}")
    print(f"Dump written to {func}.json")

    if len(fail) > 0:
        print("Failed for the following functions:", fail)

    print("Done")

if __name__ == "__main__":
    main()
