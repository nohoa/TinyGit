import sys
import os
import zlib
import hashlib
import re

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
        final_path = obj_path(obj)
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
    elif command == "ls-tree" :
        if len(sys.argv) < 3 :
            raise RuntimeWarning("Add more detail to read tree object")
        if len(sys.argv) == 3 :
            write_tree_hash_value = sys.argv[2]
            list_tree = parsing_tree_with_more_info(write_tree_hash_value)
            for item in list_tree :
                 print(item)
        else : 
            if sys.argv[2] != "--name-only" :
                raise RuntimeError("Wrong syntax requirement")

            else : 
                #Extract hash value 
                write_tree_hash_value = sys.argv[3]

                list_tree = parsing_tree(write_tree_hash_value)

                for item in list_tree : 
                    print(item)


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

def obj_path(obj) :
    path =obj[0:2]
    dest = obj[2:]
    final_path = ".git/objects/" + path+"/"+dest +"/"
    return final_path
    

def parsing_tree(write_tree_hash_value) :
    list_of_component_file = []
    with open(f".git/objects/{write_tree_hash_value[:2]}/{write_tree_hash_value[2:]}", "rb") as f:
                    decompressed  = zlib.decompress(f.read())

                    #Split based on element of tree object 
                    split_component = decompressed.split(b"\0")

                    for item in range(1,len(split_component)) :
                        split_byte_object = [bytes([b]) for b in split_component[item]]
                        flag = False 
                        for item1 in split_byte_object :
                            if item1 == b' ' :
                                flag = True
                                break

                        if flag == False or len(split_byte_object) == 1 : 
                            continue

                        id = len(split_byte_object)-1
                        starter = split_byte_object[id]
                        id -= 1

                        while(split_byte_object[id] != b' ') :
                            starter += split_byte_object[id]
                            id -= 1
                        
                        byte_answer = starter.decode("utf-8")
                        component_file = byte_answer[::-1]

                        list_of_component_file.append(component_file)
    return list_of_component_file

def parsing_tree_with_more_info(write_tree_hash_value) :
    list_of_component_file = []
    with open(f".git/objects/{write_tree_hash_value[:2]}/{write_tree_hash_value[2:]}", "rb") as f:
                    decompressed  = zlib.decompress(f.read())

                    #Split based on element of tree object 
                    split_component = decompressed.split(b"\0")

                    for item in range(1,len(split_component)) :
                        split_byte_object = [bytes([b]) for b in split_component[item]]
                        flag = False 
                        for item1 in split_byte_object :
                            if item1 == b' ' :
                                flag = True
                                break

                        if flag == False or len(split_byte_object) == 1 : 
                            continue
                        
                        #print(split_component[item])

                        id = len(split_byte_object)-1
                        starter = split_byte_object[id]
                        id -= 1
                        #print(split_byte_object)
                        while(split_byte_object[id] != b' ') :
                            starter += split_byte_object[id]
                            id -= 1
                        id -= 1
                        if(id < 1) :
                             index_value = b''
                        else :
                             index_value = split_byte_object[id]
                        ls = re.split(r'(?=\\x)', str(split_component[item]))
                        answer_file = ls[-1]
                        answer_file = answer_file[2:-1]
                        list_of_component_file.append(answer_file)
    return list_of_component_file

if __name__ == "__main__":
    main()
