---
title: dissertation writing
draft: "true"
---
![[dissertation/introduction-preparation]]

# implementation
## how bulletin works
### architecture overview (client/server/worker)
### python dispatch (client)
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

# evaluation
## correctness
### unit tests of dispatch

### system integration tests (TODO: formalize)

### clock mocking for targeted dist-sys tests? (TODO)

## ergnomics (TODO)

### user flows? for sysadmin and user?
## performance

### data collection/analysis from CHAI cluster

#### probability model (TODO)

#### sample generation

### run representative jobs on bulletin and slurm

#### compare: time to first loss (latency)

#### compare: overall GPU util

#### compare: overall time to completion

#### significance levels

### outcome (hopefully!): bulletin performs better on real ML workloads