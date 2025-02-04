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

