---
title: Prog-C 2
tags:
 - uni
 - exercises
---
## lectures 6-7

### writing heapify
```C
typedef struct tree *t_ptr;
typedef struct tree {
    int value;
    t_ptr left;
    t_ptr right;
} tree;

void heapify(int *arr, int len, t_ptr root) {
    // allocate memory for all the nodes off the bat
    tree *nodes = malloc(sizeof(tree) * len);
    for(int i = 0; i < len; i++) {
        nodes[i].value = arr[i];
        nodes[i].left = nodes[i].right = NULL;
        // follow array heap semantics -- heap node i has children
        // 2*i + 1 and 2*i + 2
        if (i!= 0) {

            if(i%2) {
                nodes[(i-1)/2].right = &nodes[i];
            }
            else {
                nodes[(i-1)/2].left = &nodes[i];
            }
        }
        for(int j=i/2; j > 0; j = j/2) {
            // need to repair the heap
            t_ptr left = nodes[j].left;
            t_ptr right = nodes[j].right;

            if((left != NULL) && left->value < nodes[j].value) {
                int temp = left->value;
                left->value = nodes[j].value;
                nodes[j].value = temp;
            }
            else {
                if((right != NULL) && right->value < nodes[j].value) {
                    int temp = right->value;
                    right->value = nodes[j].value;
                    nodes[j].value = temp;
                }
                else {
                    // if no swaps need to be made, then we've repaired the
                    // heap and can thus stop iterating
                    break;
                }
            }
        }
    }
    *root = nodes[0];
}
```

you could also just use an array of integers to represent a binary heap, and this would remove the need for traversal during heapify — but the way i've coded it here, i'm effectively using an array anyways, so it wouldn't be drastically more efficient. it will use less space though, since we don't have to keep left and right pointers.

