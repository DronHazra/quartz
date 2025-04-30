# introduction/preparation
## characterizing modern ML research

### Scaling and The Need For Compute
in the past decade, the success of deep learning methods has changed the nature of the field of machine learning. alexnet already had orders of magnitude more parameters than previous handcrafted techniques for the task — and there were many more orders of magnitude to come.

deep learning, with its hunger for large matrix multiplications, has co-evolved with GPU technology. alexnet was trained on two consumer-grade Nvidia GTX 580 GPUs, which had only 3GB VRAM each and 1.5 teraflops/second at float32. Compared to the A100 chip, the workhorse data center GPU that many academic labs maintain, has either 40 or 80 GB VRAM and 20 teraflops/second. the models have also grown: the largest model (denoted "extra large") in the GPT-2 family had 1.5B non-embedding parameters. the smallest model in the LLama 3 family has 8B parameters (a "Light-weight, ultra-fast model you can run anywhere.").

most modern, practical work thus requires significant compute resources, and the resource requirements continue to grow. even more compute is required to facilitate experimentation and robust empirical tests. training a single model or testing a single architecture may require relatively modest resources; deriving empirical scaling laws or comparisons between multiple models can take significantly more compute. 

compute requirements vary between research fields and styles, but the broad hunger for compute is impossible to ignore.

There are 3 main ways research labs acquire compute:

1. **Renting on-demand cloud GPUs** from providers like AWS, GCP, or Azure
2. **Purchasing consumer-grade desktop GPUs** attached to local workstations
3. **Reserving capacity from on-premises data centers** (clusters)

Using desktop GPUs is common among robotics labs, due to the low latency required to control robots in real time. However, these chips are limited by their desktop requirements: they cannot offer the same performance or scale as a data center chip. 

Renting cloud GPUs has no upfront cost and no fixed costs, making it easy for independent researchers and smaller labs with less institutional support. The on-demand rentals make it easy to adapt to compute needs at any given time and always use up-to-date hardware. However, renting cloud GPUs for sustained, long-term use, as would be the case for a larger research lab, is expensive. Cloud GPUs are also subject to availability constraints from the provider, which can be unpredictable and difficult to plan around. 

Because of these, research institutions — particularly universities, established labs, and even some independent research organizations — have chosen to invest in on-premises GPU clusters. For sustained high-volume workloads, it is the more cost-effective solution despite the high upfront capital expenditure. High-profile examples that take this approach include MIT, UC Berkeley, and our very own University of Cambridge. 

These large centralized clusters beget the need for robust systems that administer access to the cluster and manage the workloads that are submitted by users. This is the problem of *cluster management.* 
### compute needs => large clusters => cluster management
#### "scaling laws" and larger-scale experiments

#### why on-prem clusters are common (uni/lab/independent)

#### outcome: why is cluster management necessary?

#### outcome: who is cluster management for? (stakeholders)

### focus on iteration speed + fast feedback loops => notebooks dominate

#### ML research is fast and hacky
#### so notebooks are useful
#### how do notebooks work? how do they support fast feedback loops? 

#### outcome: why should a cluster manager target the notebook use-case?

### case study: SLURM

#### SLURM treats GPUs poorly

#### SLURM treats notebooks poorly

### outcome: motivation for design goals

## design goals for bulletin (my cluster manager)

### functional requirements (declarative spec)
### non-functional requirements/goals (ergonomics/performance)
- target notebooks (stakeholder: user, metric: steps to launch notebook job?)
- easy set-up + good defaults (stakeholder: sysadmin, metric: unclear?)
- better utilization (stakeholder: sysadmin)
- lower latency/time-to-first-loss (stakeholder: user)
### differences with SLURM 
### outcome: set up goals of correctness, performance, ergonomics 

## starting point
## addendum: how is the CHAI cluster set up? 