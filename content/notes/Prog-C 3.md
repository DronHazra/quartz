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

> If a function `f` has a static instance of a class as a local variable, when might the class constructor be called?

The constructor likely has behaviour that depends on what happens at runtime, so perhaps when the function is first called? It can't be called at compile-time (which is plausibly when static primitives would be allocated).

## writing a `Matrix` class

```C++
class Vector {
    int a, b;
    friend class Matrix;
public:
    Vector(int a, int b) : a(a), b(b) {};
};

class Matrix {
    int row_0[2];
    int row_1[2];
    friend class Vector;
public: 
    Matrix(int r_0[2], int r_1[2]) {
        for (int i=0; i<2; i++) {
            row_0[i] = r_0[i];
            row_1[i] = r_1[i];
        }
    }
    Matrix& operator+(const Matrix&);
    Matrix& operator*(const Matrix&);
    Matrix& operator-(const Matrix&);
    Matrix& operator/(const Matrix&);
    Vector& operator*(const Vector&);
};

Matrix& Matrix::operator+(const Matrix& m2) {
    int new_0[2];
    int new_1[2];
    for(int i=0; i < 2; i++) {
        new_0[i] = row_0[i] + m2.row_0[i];
        new_1[i] = row_1[i] + m2.row_1[i];
    }
    Matrix *result = new Matrix(new_0, new_1);
    return *result;
}

Matrix& Matrix::operator-(const Matrix& m2) {
    int new_0[2];
    int new_1[2];
    for(int i=0; i < 2; i++) {
        new_0[i] = row_0[i] + m2.row_0[i];
        new_1[i] = row_1[i] + m2.row_1[i];
    }
    Matrix *result = new Matrix(new_0, new_1);
    return *result;
}

Matrix& Matrix::operator*(const Matrix& m2) {
    int new_0[2];
    int new_1[2];
    new_0[0] = row_0[0] * m2.row_0[0] + row_0[1] * m2.row_1[0];
    new_1[0] = row_1[0] * m2.row_0[0] + row_1[1] * m2.row_1[0];
    new_0[1] = row_0[0] * m2.row_0[1] + row_0[1] * m2.row_1[1];
    new_1[1] = row_1[0] * m2.row_0[1] + row_1[1] * m2.row_1[1];
    Matrix *result = new Matrix(new_0, new_1);
    return *result;
}

// i don't feel like implementing matrix inversion :)
Vector& Matrix::operator*(const Vector& v) {

    int a = row_0[0] * v.a + row_0[1] * v.b;
    int b = row_1[0] * v.a + row_1[1] * v.b;
    Vector* result = new Vector(a, b);
    return *result;
}
```

## abstract classes, `virtual` and memory leaks
> give an example where failure to make a destructor `virtual` causes a memory leak.

say we have a linked list class, and we subclass it and add in a cache field. now say we have a function that copies a linked list into an array and then deletes the linked list. if we cast our cached linked list to a normal linked list to pass into this function, then the destructor for the uncached linked list will be called, and the array won't be freed — memory leak!

> why should destructors in an abstract class almost always be declared virtual?

because they have no memory to free, so any call to that destructor will almost certainly fail to free the memory allocated to the derived class.

## using destructors to release resources

```C
int process_file(char *name) {
    FILE *p = fopen(name, "r");
    if (p==NULL) return ERR_NOTFOUND;

    while (...) {
        ...
        if (...) return ERR_MALFORMED;
        process_one_option();
        ...
    }
    fclose(p);
    return SUCCESS;
}

```

this code has a bug — when it fails and returns `ERR_MALFORMED`, it doesn't close the file, and so eventually the program will trip the os file handle limit.

in C, we fix this by simply closing the file when we error:

```C
int process_file(char *name) {
    FILE *p = fopen(name, "r");
    if (p==NULL) return ERR_NOTFOUND;

    while (...) {
        ...
        if (...) {return ERR_MALFORMED; fclose(p)}
        process_one_option();
        ...
    }
    fclose(p);
    return SUCCESS;
}
```

in C++, we should use a destructor and throw an exception — when the exception is thrown, the local context of the execution is destructed and this hopefully will release any resources we hold.

```C++
class NotFound {};
class managed_file{
    FILE *p;
public:
    managed_file(char *name) {
        p = fopen(name, "r");
        if (p == nullptr) {
            throw NotFound();
        }
    }
    ~managed_file() {
        if (p!= nullptr) {
            fclose(p);
        }
        delete this;
    }
};
void process_file(char *name) {
    managed_file f = managed_file(name);
    while (...) {
        ...
        if(...) throw Malformed();
        process_one_option();
        ...
    }
}
```
here, if the file is malformed, we unwind the call stack to the calling function, invoking the destructor on `f` which closes the file pointer we were holding on to.

## a templated `Stack`
```C++
template<typename T> class Stack { 
    struct Item { //class with all public members
        T val;
        Item* next;
        Item(T v) : val(v), next(0) {}
    };
    Item* head;
    // forbid users being able to copy stacks:
    Stack(const Stack& s) {} //private
    Stack& operator=(const Stack& s) {} //private
public:
    Stack() : head(0) {}
    ~Stack(); // should generally be virtual
    T pop();
    void push(T val);
    void append(T val);
};

template<typename T> void Stack<T>::append(T val) {
    Item **pp = &head;
    while(*pp) {
        pp = &((*pp)->next);
    }
    *pp = new Item(val);
}

template<typename T> void Stack<T>::push(T val) {
    Item *i = new Item(val);
    i->next = head;
    head = i;
}
template<typename T> T Stack<T>::pop() {
    Item *result = head;
    head = head->next;
    return result;
}
template<typename T> Stack<T>::~Stack() {
    Item **pp = &head;
    while(*pp) {
        Item **next = &((*pp)->next);
        delete **pp;
        pp = next;
    }
}
```
