---
title: artificial intelligence
tags:
- uni
- exercises
---

## search
> Explain why breadth-first search is optimal if path-cost is a non-decreasing function of node-depth.

Breadth-first search explores each node at a certain depth $d$ before continuing to the next depth $d+1$, hence it will find the goal node $s^*$ with the minimal depth (call it $d_{\text{min}}$) and path cost $p^*$. 

All other goal nodes have a depth $\ge d_{\text{min}}$. Since path cost is a non-decreasing function of node depth, all other goal nodes thus have a path cost $\ge p^*$, and so BFS finds the optimal goal.

> Iterative deepening depends on the fact that *the vast majority of the nodes in a tree are in the bottom level.*
> - Denote by $f_1(b, d)$ the total number of nodes appearing in a tree with branching factor $b$ and depth $d$. Find a closed-form expression for $f_1(b, d)$.
> - Denote by $f_2(b, d)$ the total number of nodes generated in a complete iterative deepening search to depth $d$ of a tree having branching factor $b$. Find a closed-form expression for $f_2(b, d)$ in terms of $f_1(b, d)$.
> - How do $f_1(b, d)$ and $f_2(b, d)$ compare when $b$ is large?

$$
f_1(b, d) = \sum_{i=0}^d b^i = \frac{b^{d+1} - 1}{b-1}
$$

Each iteration of iterative deepening visits every node in the tree up to the current depth level. So the $i$-th iteration generates $f_1(b, i)$ nodes. 

$$
f_2(b, d) = \sum_{i=0}^d f_1(b, i) = \sum_{i=0}^d \frac{b^{i+1} - 1}{b-1} = \frac{1}{b-1}\left(b\cdot f_1(b, d) - d\right)
$$
$$
f_2(b, d) = \frac{b}{b-1} f_1(b, d) - \frac{d}{b-1}
$$


When $b$ is large, the $\frac{d}{b-1}$ term disappears, $\frac{b}{b-1}$ goes to 1, so $f_2(b, d) \approx f_1(b, d)$.

> The $A^*$ tree-search algorithm does not perform a goal test on any state *until it has selected it for expansion.* We might consider a slightly different approach: namely, each time a node is expanded check all of its descendants to see if they include a goal. Give two reasons why this is a misguided idea, where possible illustrating your answer using a specific example of a search tree for which it would be problematic.

The core property this might violate is optimality — a goal selected in such a way may not be the optimal choice. This of course depends on the precise implementation, which isn't clear. What happens when we check all the descendants of a node $s$ and find a goal $g$?
- If we do nothing, then we effectively have the same algorithm with some wasted work. 
- If we *return* $g$, then we lose optimality. Normal $A*$ guarantees that when a goal is selected, it has the minimal path cost. This modified version jumps the gun — another goal node might have a lower total path cost.

Also, we may of course consider whether "descendants" is meant to say all nodes in the relevant subtree. If this is the correct interpretation, then we are basically doing an extra tree search at each node expansion — *much* more overhead. 

### proofs about monotonicity

> The $f$-cost is defined in the usual way as $$f(n) = p(n) + h(n)$$ where $n$ is any node, $p$ denotes path cost and $h$ denotes the heuristic. An admissible heuristic is one for which, for any $n$ $$h(n) \le \text{actual distance from } n \text{ to the goal}$$ and a heuristic is monotonic if for consecutive nodes $n$ and $n'$ it is always the case that $$ f(n') \ge f(n).$$

> Prove that $h$ is monotonic if an only if it obeys the triangle inequality, which states that for any consecutive nodes $n$ and $n'$ $$h(n) \le c_{n\rightarrow n'} + h(n')$$ where $c_{n\rightarrow n'}$ is the cost of moving from $n$ to $n'$. 

Take arbitrary consecutive nodes $n, n'$. Noting that $c_{n\rightarrow n'} = p(n') - p(n)$, $$h(n) \le p(n') - p(n) + h(n') \iff p(n) + h(n) \le p(n') + h(n')$$ which is equivalent to monotonicity $f(n) \le f(n')$. 

> Prove that if a heuristic is monotonic then it is also admissible.

First note an extension of monotonicity. If there is a path from $n$ to $n'$, then $h(n) \le h(n')$. This follows from application of the monotonicity definition at each step on the path from $n$ to $n'$. 

This in hand, assume for contradiction that $\exists n$ such that $h(n) > h^*(n)$ where $h^*$ is the true distance function. Let the closest goal from $n$ be $g$. Then $f(g) = p(g) + h(g) = p(g)$. We know $p(g) \le p(n) + h^*(n)$ since the path cost to $g$ is cannot be greater than the path cost to get to $n$ plus the distance from $n$ to $g$. This gives us $$f(g) = p(g) \le p(n) + h^*(n) < p(n) + h(n) = f(n).$$ From $f(g) < f(n)$, we get $h(g) < h(n) + p(n) - p(g)$. $p(n) - p(g) = -h^*(n)$, so $h(g) < 0$ which is a contradiction. 

> In RBFS we are replacing $f$ values every time we backtrack to explore the current best alternative. This seems to imply a need to remember the new f values for all the nodes in the path we’re discarding, and this in turn suggests a potentially exponential memory requirement. Why is this not the case?

These updated $f$ values only need to be stored for the siblings of the searched node, not the one for the whole path. This is because if that sibling is expanded again, its updated $f$ value will propagate to all its immediate descendants.

