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

## lectures 3 and 4
> if `p` is a pointer, what does `p[-2]` mean? when is this legal?

`p[-2]` is a shorthand for dereferencing the value stored in memory 2 times the size of the type pointed to by `p` before the address in `p`. the compiler can't tell whether it's legal, but if the computed address isn't in use by the program then the program will get an error at runtime. 

> Write a string search function:

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