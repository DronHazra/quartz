# introduction/preparation
## characterizing modern ML research

in the past decade, the success of deep learning methods has changed the nature of the field of machine learning. alexnet already had orders of magnitude more parameters than previous handcrafted techniques for the task — and there were many more orders of magnitude to come.

deep learning, with its hunger for large matrix multiplications, and GPUs have co-evolved over the last decade. alexnet was trained on two consumer-grade Nvidia GTX 580 GPUs, which had only 3GB VRAM each and 1.5 teraflops/second at float32. today, the workhorse GPU maintained by many academic labs and datacenters, Nvidia's A100 chip, has 40 or 80 GB VRAM configurations, with 20 teraflops/second, not accounting for the speedups from tensor cores specialized to do matrix multiplication. the largest model (denoted "extra large") in the GPT-2 family had 1.5B non-embedding parameters. the smallest model in the LLama 3 family has 8B parameters (a "Light-weight, ultra-fast model you can run anywhere.")

the compute needs of modern ML research continue to grow, with some amount of compute being almost necessary for most practical work and experimentation. 
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

### outcome: set up goals of correctness, performance, ergonomics 

## addendum: how is the CHAI cluster set up? 