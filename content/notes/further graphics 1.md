---
title: further graphics 1
tags:
 - uni
 - exercises
---
(dh700)
## parametric vs implicit surfaces

 - checking whether a point is inside/outside: easier for implicit surfaces
	 - because with our implicit function $f$, we can simply plug in a point $x$ and check whether $f(x) > 0$ or $f(x) < 0$
 - generating points on the surface: easier for parametric surfaces
	 - with our parametric surface we can simply just sweep the $u, v$ space and get points on the surface using $p(u, v)$
 - checking whether a point is on the surface: easier for implicit surfaces
	 - like with checking inside/outside, you can simply compute $f(x)$ and check if it's 0.

## a parametric ellipsoid
First, we modify the parametric equation of a sphere, scaling it along each dimension based on the scaling factors in the ellipsoid equation. 
$$
p(\varphi, \theta) = (15 \cos \theta \sin \varphi, 3 \sin \theta \sin \varphi, 15 \cos \varphi)
$$
Subbing this into the given implicit equation gives us:
$$
(\cos \theta \sin \varphi)^2 + (\sin \theta \sin \varphi)^2 + (\cos \varphi)^2 - 1 = 0
$$
which is equivalent to the implicit equation for a standard sphere, and hence is true. 

We want to prove that $P = (2, 2, -11)$ lies on the ellipsoid's surface. It's easiest to use the implicit form, where we plug in the values $$\frac 4 {225} + \frac {4} {9} + \frac {121} {225} - 1 = \frac {104 + 121} {225}  - 1 = 0$$

Next, we want the surface normal at P, which is the grad of our $f$ evaluated at P $$\nabla f = \left( \frac {2x}{225}, \frac{2y}{9}, \frac{2z}{225} \right) \Rightarrow n = (4/225, 4/9, 4/225)$$

We could probably normalize this too, but it doesn't specify in the question that we have to, so I won't. 

## triangle meshes vs point sets
> Compared to a triangle mesh, a point set lacks a vital piece of information in that it no longer identifies the neighbouring vertices of any given vertex. Why is such information necessary or useful in the first place and how do point set surfaces work without it?

This information is important in approximating local quantities like curvature. 

Point set surfaces work without this neighbour information by defining an implicit function that takes a point $x$, defines a "neighbourhood" around x, fits a surface to the sample points in the neighbourhood, and then projects $x$ onto that local approximation of the surface. 

## laplacians 
doing some computations, we get $L_u(v_0) = (0, -3, -4)$. hence $H=5$. 

we could compute the gaussian curvature by using the formula $$K(v_i) = \frac{1}{A_i} (2\pi - \sum_j \theta_j)$$ where $\theta_j$ is the angle between $v_i$, $v_j$ and $v_{j+1}$. 

## rigging and associated transformations

*Rigging* adds structure to the surface by defining a *skeleton* (with bones and joints) and defining associated weights for each point on the surface. The weights define how connected each point on the surface is to each joint or bone. Together, these gives us a body which allows for animations via transformations on the bones or joints. 

> Assume we have a cylinder with an axis aligned with the $x$-axis. The cylinder extends from −1 to 1 on the $x$-axis and has a base radius of 1. We embed two bones inside the cylinder along the $x$-axis: one extends from −1 to 0, the other from 0 to 1. We define the influence of each bone on each point on the cylinder’s surface as the inverse distance of the point to the bone. Assume we transform the second bone with the transformation $T$ .
> 
>Determine the concrete weights and give a formula of how the new position $x′$ would be computed from the weights $w_1(x)$, $w_2(x)$, $x$ and $T$ for a point $x$ on the surface (a) in the middle (i.e. with $x = 0$) and (b) on either end (i.e. with $x = ±1$).  
Hint: the weights are proportional to the influence defined above.

The distance to the (midpoint of the) bone is $\sqrt{\left(x+\frac 1 2\right)^2 + y^2 + z^2}$ for the first bone and $\sqrt{\left(x-\frac 1 2\right)^2 + y^2 + z^2}$.  The inverse is simply the reciprocal of this. 

The formula for any point $\mathbf{x}$ is $$
\mathbf{x'} = \left(
\frac{1}{\sqrt{\left(x+\frac 1 2\right)^2 + y^2 + z^2}} I + 
\frac{1}{\sqrt{\left(x-\frac 1 2\right)^2 + y^2 + z^2}}T
\right)\mathbf{x}$$
so for $x=0$ it would be $$
\mathbf{x'} = \left(
\frac{1}{\sqrt{\frac 1 4 + y^2 + z^2}} I + 
\frac{1}{\sqrt{\frac 1 4 + y^2 + z^2}}T
\right)\mathbf{x}$$
for $x=1$ it would be $$
\mathbf{x'} = \left(
\frac{1}{\sqrt{\frac 9 4 + y^2 + z^2}} I + 
\frac{1}{\sqrt{\frac 1 4 + y^2 + z^2}}T
\right)\mathbf{x}$$
and for $x=-1$ it would be
$$
\mathbf{x'} = \left(
\frac{1}{\sqrt{\frac 1 4 + y^2 + z^2}} I + 
\frac{1}{\sqrt{\frac 9 4 + y^2 + z^2}}T
\right)\mathbf{x}$$