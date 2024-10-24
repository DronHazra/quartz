---
title: cybersec 1
tags:
- uni 
- exercises
---
## threat modelling for bike
- CIA — confidentiality, integrity, accessibility
- stride threat model

## unix permissions & privilege escalation
the key here is that `microedit` is Set-UID `benn`. 

|        | `manual.txt` | `report.txt` | `microedit` | `src/code.c` | `src/code.h` |
|--------|--------------|--------------|-------------|--------------|--------------|
| `alex` | R+ W+        | R* W*        | R* W*       | R+           |              |
| `benn` | R+           | RW+          |             | R*           |  W*          |
| `cloe` |              |              |             |              |              |

