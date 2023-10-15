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
