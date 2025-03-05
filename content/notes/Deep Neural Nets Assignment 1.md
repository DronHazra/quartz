After one step, the reparametrized linear model adjusts the slope more than the original model. This can be seen analytically. Consider the weight $w_1^{(0)}$ and bias $b_1^{(0)}$ of the linear model $f$ at initialization. The reparametrized model $g$ has initial parameters $w_2^{(0)} := w_1^{(0)}/c$, $b_2^{(0)} := b_1^{(1)}$. $L_f((x, y)) = (f(x) - y)^2$, so by the chain rule: 
$$
\begin{align}
\frac{\partial L_f}{\partial w_1} &= \frac{\partial}{\partial w_1} \left(w_1x + b - y\right)^2 \\
&= 2x (w_1x+b - y) = 2x(f(x) - y) \\
\frac{\partial L_f}{\partial b_1} &= 2(w_1x + b - y) = 2 (f(x) - y) \\
\\
\frac{\partial L_g}{\partial w_2} &= \frac{\partial}{\partial w_2} \left(c\cdot w_2x + b - y\right)^2 \\
%% &= 2 (c\cdot w_2 x + b - y) \frac{\partial}{\partial w_2} (c\cdot w_2x + b - y)\\ %%
&= c\cdot 2 x(c\cdot w_2x+b - y) = c\cdot 2x(g(x) - y) \\
\frac{\partial L_g}{\partial b_2} &= 2(c\cdot w_2x + b - y) = 2(g(x) - y)
\end{align}
$$
At initialization, $f=g$, so the gradient update for the biases will be the same, but the gradient update for $w_2$ is scaled by $c$. This explains the behaviour in Figure 1: the reparametrized
model updates the slope more than than the original model.  Note that this analysis does not necessarily hold after initialization, as $w_2^{(1)} \neq w_1^{(1)} / c$. 

A natural extension is to ask whether appropriately scaling the learning rate could erase this effect. We have $w_2^{(1)} = w_2^{(0)} - \eta_2 \cdot 2c (g(x) - y)$, and
$$
\begin{align}
w_1^{(1)} &= w_1^{(0)} - \eta_1 \cdot 2 (g(x) - y) \\
\frac{w_1^{(1)}}{c} &= \frac{w_1^{(0)}}{c} - \frac{\eta_1}{c} \cdot 2(g(x) - y) \\
&= w_2^{(0)}  - \frac{\eta_1}{c} \cdot 2(g(x) - y)
\end{align}
$$

Setting $\eta_2 = \dfrac{ \eta_1} {c^2}$ means $\eta_2 \cdot 2c = \dfrac{\eta_1}{c} \cdot 2$, which would mean $w_2^{(1)} = \dfrac{w_1^{(1)}}{c}$. This is seen in 

We can empirically test this:
![[Pasted image 20250220235109.png]]


![[Pasted image 20250220224058.png]
![[Pasted image 20250220224404.png]]

The 