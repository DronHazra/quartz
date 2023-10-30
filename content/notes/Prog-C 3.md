---
title: Prog-C 3
tags:
  - exercises
  - uni
---

## implementing a linked list
```C++
#include <cstddef>
#include <stdio.h>
class LinkList {
public:
    struct llnode {
        int a;
        llnode* next;
    };
    llnode* head;
    int len;

    LinkList() : head(nullptr), len(0) {};
    LinkList(int a[], int len);
    LinkList(const LinkList& ll);
    LinkList& operator=(const LinkList& ll);
    //~LinkList() {
    //    llnode* n = head;
    //    while(n != nullptr) {
    //        llnode* next = n->next;
    //        delete n;
    //        n = next;
    //    }
    //}
    int pop();
    int peek() const;
};

LinkList::LinkList(int a[], int len) : len(len) {
    if(len == 0) {
        head = nullptr;
        return;
    }
    head = new llnode();
    head->a = a[0];
    llnode *current = head;
    for(int i=1; i < len; i++) {
        llnode* node = new llnode();
        node->a = a[i];
        current->next = node;
        current = node;
    }
    current->next = nullptr;
}
LinkList::LinkList(const LinkList& ll) : len(ll.len) {
    head = new llnode();
    head->a = ll.peek();
    llnode* other = ll.head->next;
    llnode* our = head;
    while(other != nullptr) {
        llnode* node = new llnode();
        node->a = other->a;
        our->next = node;
        our = node;
        other = other->next;
    }
    our->next = nullptr;

}
LinkList& LinkList::operator=(const LinkList& ll){
    LinkList ll_copy = ll; //copy constructor called
    // delete this; i would use this if i wasn't exploiting the lack of
    // a destructor
    llnode* n = head;
    while(n != nullptr) {
        llnode* next = n->next;
        delete n;
        n = next;
    }

    head = ll_copy.head;
    len = ll.len;
    return *this;
    // this works because our destructor doesn't actually free any memory
    // and so even though ll_copy goes out of scope, its memory doesn't
    // get cleared. 
}


int LinkList::pop() {
    if(len <=0) {
        return -1;
    }
    int result = head->a;
    llnode *new_head = head->next;
    delete head;
    head = new_head;
    len--;
    return result;
}
int LinkList::peek() const {
    if (len <= 0) {
        return -1;
    }
    return head->a;
}
int main() {
    int test[] = {1, 2, 3, 4, 5};
    LinkList l1(test+1,4), l2(test,5);
    LinkList l3=l2, l4;
    l4=l1;
    printf("%d %d %d\n",l1.pop(),l3.pop(),l4.pop());
    return 0;
}
```
