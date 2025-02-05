# TinyGit
Implementation of a Tiny Github with .git file directory and structure

Testing : 

Create testing directories : 

```
mkdir test-dir && cd test-dir
```

Initialize .git directory : 

```
../your_program.sh init

```

Crate a testing txt file : 
```
echo "hello world" > test.txt

```

Create hash-object file : 

```
../your_program.sh hash-object -w test.txt

```

cat-file implementation : 

```
../your_program.sh cat-file -p [SHA_code]

```

list_tree implementation : 

If list full of tree object components : 

```

../your_program.sh tree-list  [TREE_SHA_code]

```

If list only the name  of tree object components : 

```

../your_program.sh tree-list --name-only [TREE_SHA_code]

```