import sys
import os
import zlib

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file"  and sys.argv[2] == "-p" :
        obj = sys.argv[3] 
        path =obj[0:2]
        dest = obj[2:]
        final_path = ".git/objects/" + path+"/"+dest
        current_content = ""
        with open(final_path,"rb") as f : 
            decompressed  = zlib.decompress(f.read())
            string_object = decompressed.decode("utf-8")
            current_content = string_object[8:].strip()
            print(string_object[8:].strip(),end="")
    elif command == "hash-object" and sys.argv[2] == "-w" :
            print(1)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
