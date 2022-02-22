# Artifact of FlexTree, FlexSpace and FlexDB

**Note: This repository contains the materials for EuroSys '22 AEC only. For the usage and implementation details of
FlexTree, FlexSpace and FlexDB, plase check the [main repository](https://github.com/flexible-address-space/flexspace)
where all the future updates will be maintained.**

## Artifact Evaluation Instruction (EuroSys '22 AE)

All the necessary artifacts have been included and documented in this repository.
The major claims of the core functionalities of FlexTree, FlexSpace and FlexDB are implemented.
Please refer to the [Implementation Details](https://github.com/flexible-address-space/flexspace#implementation-details)
section of the main repository's documentation for their interface (as well as the functionality under the APIs).
To test their core functionalities, you can use the minimal example shown in the main repository's
[Demo](https://github.com/flexible-address-space/flexspace#demo) section.

All the experimental results reported in the paper were produced on one of our servers with the following configuration:

| Resource | Specifications |
| --- | --- |
| CPU | 2x Intel Xeon(R) Silver 4210 |
| Disk | Intel Optane 905P 960G (Model: SSDPED1D960GAY) |
| Memory | 128GB (we limited the memory to 64GB in the experiments) |
| OS | Arch Linux w/ `linux-lts 5.10.32` |
| Tool chain | `clang 12.0.1`, `jemalloc 5.2.1`, `liburing 2.0` |

Specifically, the server has unlimited locked memory. You can raise the corresponding limit by adding
`* - memlock unlimited` to `/etc/security/limits.conf`.

The file systems we used to compare against FlexSpace are all in the mainline kernel.
You need to install `e2fsprogs`, `xfsprogs`, `f2fs-tools` and `btrfs-progs` in the user space to make `mkfs` work.
RocksDB can be installed via its official source code or Linux distrbution provided packages.
We used a patched version of KVell to support variable-sized keys.
Its code can be found in [this repository](https://github.com/flexible-address-space/eurosys22-artifact-kvell).

**Before running the experiments, you should run the `bootstrap.sh` script in this repository to fetch the snapshot of
our implementation prepared for the artifact evaluation.**

To help the evaluators test our implementation more easily, we will provide the access to the server we used, which
has the configuration shown in the table.
We will collect the public keys from the evaluators via hotcrp.
The environment on the server is ready to run FlexTree, FlexSpace, FlexDB and corresponding experiments
without further modifications to the operating system or the storage device.
In the following, we will provide evaluation instructions based on this server.

The major results of the experiments for each system in the submission are:

- FlexTree: Table 1
- FlexSpace: Table 2 and Figure 10
- FlexDB: Figure 11 (incl. 6 sub-figures), Table 4, Figure 12 (incl. 2 sub-figures)

Note that the figure/table IDs only apply to the submission version of the paper.
They are subject to change after the final revision.

Before running the experiments, you first need to log in on the provided server via `ssh` with username `flex`.
When you successfully logged in, please clone this repository in your `HOME` directory.
The server has already set up all the necessary dependencies.
For each experiment, we also have automated all the procedures so that it is not necessary to re-configure the system.
However, since some experiments take a long time to perform, **we strongly suggest using tools like `tmux` or
GNU `screen` to persist the experiment process through multiple `ssh` sessions.**

In the following, we introduce how to execute the
experiments and get the results (including the raw data and the figures).

### FlexTree Experiments (Section 6.1)

The estimated running time of the experiments in this part is around **70 minutes**.

#### Table 1

To produce the results shown in Table 1, first `cd` into `flextree_benchmark` directory.
Then, you can inspect the script `reproduce.sh` (as well as `test.c` if needed).
After that, simply execute the script by `./reproduce.sh` and the experiments will start running.
The results will be printed out directly to `stdout`. The results returned are expected to be similar to
Table 1 in the submission, or showing a similar trend.

### FlexSpace Experiments (Section 6.2)

The estimated running time of the experiments in this part is around **22 hours**.

To produce the results shown in Table 2 and Figure 10, first `cd` into `flexfile_benchmark` directory.
Then, you can inspect the script `reproduce.sh` (as well as `*.c` files if needed).
After that, simply execute the script by `./reproduce.sh` and the experiments will start running.
The results will be stored in `flexfile_benchmark/results/flexfile/` directory.

#### Table 2

Table 2 consists of two set of experiment configurations.
The 4KB block / 1GB space results can be found in `flexfile_benchmark/results/flexfile/micro-4096-262144/` directory.
The 64KB block / 16GB space results can be found in `flexfile_benchmark/results/flexfile/micro-16384-262144/` directory.
To generate the table contents of each part, you have to first `cd` into the results directory.
Then, copy `flexfile_benchmark/throughput.py` and `flexfile_benchmark/smart.py` to the results directory via `cp`.
Executing `python throughput.py` inside the results directory will produce all the throughput-related data in the table,
following the same layout as shown in the submission.
The data are printed directly to `stdout` in LaTeX table format.
Running `python smart.py` will generate the write amplification ratios shown in the table.
Note that for `smart.py`, you will need to update the variable `base` in the source code to the corresponding data
written size in GB (1 or 16) to get the correct write amplification ratio.
The default value is 1.

#### Figure 10

The results for multi-threaded read experiments shown in Figure 10 are stored in
`flexfile_benchmark/results/flexfile/multi/multi-4096-262144/` directory.
You need to manually inspect the data and compare them with the results shown in Figure 10.
The expected results are FlexSpace shows similar or slightly lower throughput than XFS (except in sequential read).
With more threads, the performance gap will get smaller and FlexSpace will perform similarly compared to XFS with 8
threads.

### FlexDB Experiments (Section 6.3)

The estimated running time of the experiments in this part is around **30 hours**.

The results of this part can be reproduced by running the one-shot script `flexdb_benchmark/reproduce.sh`.
You can simply `cd` into `flexdb_benchmark` directory and use `./reproduce.sh` to run all FlexDB-related experiments.
Before running the experiments, you can also review the content of the scripts we used in `flexdb_benchmark/scripts/`
directory.
Note that you have to make sure that when running the script, the `PWD` is `flexdb_benchmark` (similar as in previous
experiments).

After the script finishes execution, the experimental results are all stored in `flexdb_benchmark/results/flexdb/`
directory. You can follow the following steps to generate the figures or tables in the submission.
Note that the absolute numbers in the figures may not strictly align with those reported in the paper.
However, they should follow similar trends.

#### Figure 11 (a)(b)

In `flexdb_benchmark/results/flexdb/write/` directory, there are to plotting scripts - `write.py` and `wa.py`.
You can simply issue `python write.py` and `python wa.py` within the directory.
The scripts will produce `flexdb-write.pdf` and `flexdb-wa.pdf`, which correspond to Figures 11(a) and 11(b),
respectively.

#### Figure 11 \(c\)(d)

In `flexdb_benchmark/results/flexdb/write/` directory, there are to plotting scripts - `read.py` and `scan.py`.
Using `python` to execute them will produce `flexdb-read.pdf` and `flexdb-scan.pdf`,
which correspond to Figure 11\(c\) and 11(d), respectively.

#### Figure 11 (e)

You can issue `python scale.py` in `flexdb_benchmark/results/flexdb/scale/` directory.
The script will produce `flexdb-scale.pdf` which corresponds to Figure 11(e).

#### Figure 11 (f)

There will be four directories in `flexdb_benchmark/results/flexdb/gc/` directory.
The directory names correspond to the bars in Figure 11(f).
In each directory, there will be a file containing the experiment output.
You can check the last line of each file where the throughput is reported after `mops` string (it stands for million
operations per second).

#### Table 4

The latency-related results in Table 4 can be found under `flexdb_benchmark/results/flexdb/latency/` directory.
To decode the latency metrics, you can refer to the CDF output in each file.
Specifically, for 99P and 95P latencies, you can check the very first `95.xx` and `99.yy` in the last column.
Then, the number in the first column in that row corresponds to the latency number in micro-seconds.
To calculate the average latency, you can run the provided script `latency.py` in the directory.
Note that before running `latency.py`, you need to manually parse the output file and only keep the CDF-related
outputs. Do not include any other lines, like the throughput.

#### Figure 12 (a)(b)

The YCSB results could be found in `flexdb_benchmark/results/flexdb/ycsb` and
`flexdb_benchmark/results/flexdb/ycsb-oc` directories.
There will be a Python script under each directory.
Executing the script will produce `flexdb-ycsb.pdf` and `flexdb-ycsb-oc.pdf`, which correspond to Figure 12(a) and
12(b), respectively.
