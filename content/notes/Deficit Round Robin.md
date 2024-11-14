---
title: Deficit Round Robin
tags:
  - definition
---
- give each queue a deficit counter
- serve packet if `size <= quantum + deficit`, if you can't serve the packet, augment the deficit counter by quantum