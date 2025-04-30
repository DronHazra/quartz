# implementation
## how bulletin works

### architecture overview (client/server/worker)
Bulletin was built around a client/server/worker architecture.

- **Clients submit jobs for remote execution** on a compute node. They specify the resource and time requirements for the job.
- **Workers execute jobs** on their individual compute node. Each compute node has a worker that waits for jobs from the server and executes the received jobs with the specified resource and time limits.
- **The server coordinates between clients and workers.** It has many responsibilities, including job scheduling, deployment and signalling, monitoring worker status, and providing the interface to clients.

This architecture reflects Bulletin's role as an interface for users to interact with the cluster. It conveniently maps the functional units of a workload manager to the real machines they will run on.

Bulletin is a distributed system with shared state. There are various ways of handling shared state in a distributed system, with different fault tolerance guarantees and failure assumptions. I use a centralized PostgreSQL database as the single source of truth. This allows me to inherit its concurrency model and guarantees, but it also becomes a single point of failure. I decided that this tradeoff was worth it, for two reasons:

1. PostgreSQL has been battle-tested in many systems for many years: it is unlikely our modest load will cause failures in the database itself.  
2. The server and Postgres are colocated on the same machine. If that machine fails, the users' interface to the cluster will be blocked, removing the possibility of entering an inconsistent state.
3. A failure in Postgres is likely to be much easier to debug then a bespoke system for managing distributed state, due to its extensive documentation and history. It is plausible that system administrators will have prior experience working with Postgres. The same is not true for a bespoke system.

The final architectural requirement is a way to communicate between nodes. Bulletin also operates assuming a shared filesystem such as a `NAS`, which is very often the case. The shared filesystem is used to transport the execution payloads and results, which avoids needing to transmit potentially large payloads via the server.

Bulletin primarily uses gRPC and Protocol Buffers (protobufs) for message passing and signalling. gRPC was chosen to implement the API due to its support of long-lived streaming RPCs, connection management tools, and tight integration with `golang`. gRPC and protobufs work together seamlessly. One disadvantage is the need to keep the protos and SQL schemas in sync with one another, but this conversion would be required even if JSON were used as the underlying message. The server runs a gRPC service, with the workers and clients making RPCs to the server. 
### python dispatch (client)

One of the primary design goals for Bulletin is to make it easy to submit jobs from a notebook. To achieve this, we bridge the gap between the locally oriented, highly stateful model of a local notebook with remote execution on GPUs.

One key mismatch between local and remote execution is state. When executing locally, variables set inside a notebook are accessible throughout the notebook, and can be updated globally. This allows the user continual flexibility in how they access the intermediate and final results of their computations. 

For example, say I was sampling from an image generation diffusion model. I might write a function and run it to see the final results, but then I might want to see the intermediate states in sampling. The permissive scope of notebooks would allow for me to append to a list of image states and visualize the list outside the function, requiring no changes to any other calling code (the interface hasn't changed!). This permissive scope and global mutability is part of what makes notebooks so appealing for rapid experimentation and prototyping.

Thus, Bulletin's dispatch operates transparently on the functions called within a notebook. It offers a clear interface intended for use as a decorator: any function that should execute remotely can be tagged with a `@to_remote` decorator that accepts the relevant resource requests. When the function is called, it executes on a remote machine with all state information. On completion, it updates the local state with the new remote state. Bulletin even bridges the conflict between local CPU and remote GPU execution by moving PyTorch Tensors to the GPU automatically on the remote machine, and moving them back to the CPU on completion. **This lets users use remote compute resources as if they were local.**

To achieve this, Bulletin intercepts the local tagged function call, serializes the resulting closure *and its environment* to disk, and sends a message to the server submitting a job. Importantly, Python's default serialization module `pickle` serializes many internal structures by reference. This means that when certain structures are loaded in a fresh execution environment, these references will point to nothing. To fix this, I use an open-source library `cloudpickle` that serializes all objects by value. 

However, simply serializing and executing remotely only partially bridges the inferential gap. `cloudpickle` does not expose facilities to update 

Though they are usually referred to as functions, functions defined in a notebook are actually *closures*, in that they can refer to their environment. When the closure is called locally, 

When the closure is executed, it is first deserializes any PyTorch Tensors (or anything that implements a `.to(device)` method)


#### matching the user's mental model
#### (de-)serializing closures and their environments

### job execution (worker)

#### crash-recover model

#### `cgroups` for resource limits

#### `go` context timeouts for time limits

#### stdout/stderr streaming? (TODO)

### scheduling + allocation (server)

#### goroutine model for scheduler

#### using postgres isolation levels

#### worker connection management/failure detection (keepalives)

#### authentication (TODO)