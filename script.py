import sys
import json

def scan(fn, depth = 1):
    if depth > 3:
        return {}
    func = eval(fn)
    result = dict()
    result[fn] = dict()
    result[fn]['func'] = dict()
    result[fn]['callable'] = callable(fn)
    for _func in dir(func):
        if '_' in _func or not _func.islower():
            continue
        print(f"Checking nested functions for {fn}.{_func}", end =" ")
        try:
            result[fn]['func'].update(scan(f"{fn}.{_func}", depth + 1))
            print("...SUCCESS")
        except:
            print("...FAILED")
            
    return result

def main():
    func = input("Enter the function name to scan > ")
    
    try:
        eval(func)
    except NameError:
        try:
            globals()[func] = __import__(func)
        except ModuleNotFoundError:
            sys.exit("Invalid function")

    dump = scan(func)       
    dump = json.dumps(dump, indent = 4, sort_keys = False)
    file = open(f"{func}.json", "w")
    file.write(dump)
    file.close()

if __name__ == "__main__":
    main()
