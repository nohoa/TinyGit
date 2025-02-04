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

        with open(final_path,"rb") as f : 
            decompressed  = zlib.decompress(f.read())
            string_object = decompressed.decode("utf-8")
            print("Content of the file is : ",string_object[7:].strip(),end="")
    elif command == "hash-object" :
        if len(sys.argv) < 3 : 
            raise RuntimeWarning("Add more detail (-w) filename")
         
        obj = sys.argv[3] 
        hashing(obj)   
    else:
        raise RuntimeError(f"Unknown command #{command}")


def hashing(pathname) : 
    store = "";
    with open(pathname, "rb") as fd : 
        data = fd.read()
        store = data.decode("utf-8")
        #print(store)
    result = b'blob' + b' ' + str(len(data)).encode() + b'\x00' + store.encode("utf-8")
    hash_value = hashlib.sha1(result)
    hash_val = hash_value.hexdigest()

    print("Hash value of blob object is: ",hash_val)

    gitpath =hash_val[0:2]
    dest = hash_val[2:]
    interpath = os.getcwd() +"/.git/objects/" 

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
