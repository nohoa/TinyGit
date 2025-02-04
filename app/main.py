import sys
import os
import zlib
import hashlib

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
        final_path = ".git/objects/" + path+"/"+dest +"/"
        final_path += os.listdir(final_path)[0]
        #print(final_path)
        current_content = ""
        #print(os.listdir(final_path))
        with open(final_path,"rb") as f : 
            decompressed  = zlib.decompress(f.read())
            string_object = decompressed.decode("utf-8")
            current_content = string_object[8:].strip()
            print(string_object[8:].strip(),end="")
    elif command == "hash-object" :
        if len(sys.argv) < 3 : 
            raise RuntimeWarning("Add more detail (-w) filename")
         
        obj = sys.argv[3] 
        hashing(obj)   
    else:
        raise RuntimeError(f"Unknown command #{command}")


def hashing(pathname) : 
    store = "";
    print(pathname)
    with open(pathname, "rb") as fd : 
        data = fd.read()
        store = data.decode("utf-8")
    result = b'blob' + b' ' + str(len(data)).encode() + b'\x00' + data
    hash_value = hashlib.sha1(result)
    hash_val = hash_value.hexdigest()
    print(hash_val)

    gitpath =hash_val[0:2]
    dest = hash_val[2:]
    interpath = os.getcwd() +"/.git/objects/" 
    #if not os.path.exists(os.path.join(interpath,path)) :
    path1 = os.path.join(interpath,gitpath)

    if not os.path.exists(path1) :
        os.mkdir(path1)

    next_path = os.path.join(path1,dest)

    #if not os.path.exists(os.path.join(next_path,dest)) :
    #print(next_path)
    if not os.path.exists(next_path) :
        os.mkdir(next_path)

    fin_path = next_path + '/'+ pathname

    with open(fin_path, "wb") as file:
        file.write(zlib.compress(result))
    

if __name__ == "__main__":
    main()
