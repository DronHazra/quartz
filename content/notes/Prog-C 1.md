---
title: Prog-C 1
tags:
 - uni
 - exercises
---

## lecture 1

> What is the difference in C between ``'a'`` `"a"`?

`'a'` is a single `char`, whereas `"a"` is a string literal and thus has type `char*`. 

> Will `char i, j; for (i=0; i<10, j<5; i++,j++) ;` terminate? If so, under what circumstances?

`j` hasn't been defined and so is probably garbage. `i<10, j<5` just evaluates to `j<5`, so the loop will terminate either because the garbage `j` was initialized to is >= 5, or because `j` gets incremented enough. 

> Write an implementation of bubble sort:

```C
void bubble_sort(int arr[], int len) {
	int changed = 1;
	int temp;
	while(changed) {
		changed = 0;
		for(int i=0; i<len - 1; i++) {
			if(arr[i] > arr[i+1]) {
				temp = arr[i], arr[i] = arr[i+1], arr[i+1] = temp;
				changed = 1;
			}
		}
	}
}
void bubble_sort_modified(char arr[], int len) {
	int changed = 1;
	char temp;
	while(changed) {
		changed = 0;
		for(int i=0; i<len - 1; i++) {
			if(arr[i] > arr[i+1]) {
				temp = arr[i], arr[i] = arr[i+1], arr[i+1] = temp;
				changed = 1;
			}
		}
	}
}
```

## lecture 2
### implementing `cntlower`
```C
#include <string.h>
int cntlower(char str[]) {
    int len = strlen(str);
    int count = 0;
    for(int i = 0; i<len; i++) {
        if (str[i] < 'A') {
            count++;
        }
    }
    return count;
}
```

### implementing `SWAP`
```C
#define SWAP(t, x, y){t temp = x; x=y; y=temp;}
```


expanding the macro for `SWAP(int, v[i++], w[f(x)])`, we get:
```C
{int temp = v[i++]; v[i++] = w[f(x)], w[f(x)] = temp}
```
`i++` returns the current value of `i` and then increments `i`, which means that the second `v[i++]` refers not to the element referred to by the argument to `SWAP`, but rather 

## lectures 3 and 4
> if `p` is a pointer, what does `p[-2]` mean? when is this legal?

`p[-2]` is a shorthand for dereferencing the value stored in memory 2 times the size of the type pointed to by `p` before the address in `p`. the compiler can't tell whether it's legal, but if the computed address isn't in use by the program then the program will get an error at runtime. 

### string searching

```C
const char *strfind(const char *needle, const char *hay) {
    int i = 0;
    char *found = NULL;
    while(hay[i] != '\0') {
	int j = 0;
	while((hay[i+j] != '\0') && (needle[j] == hay[i+j])) {
	    j++;
	    if (needle[j] == '\0') {
		// if we've matched the entire needle
		found = hay + i;
		break;
	    }
	}
	if (found != NULL) {
	    break;
	}
    }
    return found;
}
```

### adding characters in a large file

```
dron@jirachi c ) time ./sum_file_mmap ~/datasets/ImageNet/ILSVRC2012_devkit_t12.tar.gz

file is 2568145 bytes long

sum: 328115312, bytes read: 2568145

________________________________________________________

Executed in    9.71 millis    fish           external

   usr time    4.83 millis    0.24 millis    4.59 millis

   sys time    4.22 millis    2.08 millis    2.14 millis

  

dron@jirachi c ) time ./sum_file ~/datasets/ImageNet/ILSVRC2012_devkit_t12.tar.gz

sum: 328115312, bytes read: 2568145

________________________________________________________

Executed in  111.94 millis    fish           external

   usr time  104.84 millis    0.15 millis  104.69 millis

   sys time    6.65 millis    1.33 millis    5.32 millis
```

and with a bigger file:

```
dron@jirachi c ) time ./sum_file_mmap ~/Downloads/UTM.dmg           **(miniforge3)**

file is 244438799 bytes long

sum: -2019725168, bytes read: 244438799

________________________________________________________

Executed in  620.94 millis    fish           external

   usr time  233.32 millis    0.26 millis  233.06 millis

   sys time   35.98 millis    2.59 millis   33.38 millis

  

dron@jirachi c ) time ./sum_file ~/Downloads/UTM.dmg                **(miniforge3)**

sum: -2019725168, bytes read: 244438799

________________________________________________________

Executed in    8.43 secs    fish           external

   usr time    8.20 secs    0.18 millis    8.20 secs

   sys time    0.21 secs    1.92 millis    0.21 secs
```

the `fread` one:

```C
#include <stdio.h>
int main(int argc, char *argv[]) {
    FILE *fp;
    unsigned char buffer;
    int bytes_read = 0;
    if ((fp=fopen(argv[1], "rb")) == 0) {
        perror("fopen error:");
        return 1;
    }
    int sum = 0;
    while(!feof(fp)) {
        bytes_read += fread(&buffer, sizeof(char), 1, fp);

        sum += buffer;
    }
    printf("sum: %d, bytes read: %d", sum, bytes_read);
    return 0;
}
```

and the `mmap` one:
```C
#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/stat.h>
int main(int argc, char *argv[]) {

    int bytes_read = 0;
    int fd = open(argv[1], O_RDWR);
    if (fd == -1) {
        perror("open error:");
        return 1;
    }

    // get size
    struct stat statbuf;
    int err = fstat(fd, &statbuf);
    if (err < 0) {
        perror("fstat error:");
        return 1;
    }
    printf("file is %lld bytes long\n", statbuf.st_size);
    // set up buffer
    unsigned char *buffer = mmap(
        NULL, statbuf.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0
    );
    if (buffer == MAP_FAILED) {
        perror("mapping failed:");
        return 1;
    }
    int sum = 0;
    for(int i=0; i < statbuf.st_size; i++) {
        sum += buffer[i];
        bytes_read += 1;
    }
    printf("sum: %d, bytes read: %d", sum, bytes_read);
    close(fd);
    munmap(buffer, statbuf.st_size);
    return 0;
}
```

the `mmap` version seems to be much faster! the performance on the large file was around 1 Mb/s. rerunning seems to eliminate get lower wall times, presumably because the ssd has some internal cache or something? whereas on first run the program has to wait for the disk to lookup those blocks, so the program sleeps during that time?

