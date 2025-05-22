---
title: "How to Accelerate your Research"
teaching: 45
exercises: 45
questions:
- What are the benefits of scaling resources over optimizing code?
- How can multiple cores and nodes be utilized effectively?
- What are the best practices for using high-performance computing clusters and cloud computing?
objectives:
- Understand the concept of scaling resources to accelerate research.
- Learn how to use multiple cores, nodes, and parallel computing.
- Gain knowledge of high-performance computing, including clusters and cloud computing.
- Develop skills in planning and simulating distributed computing tasks.
- Identify and address common research bottlenecks.
keypoints:
- Scaling resources can be more efficient than optimizing code.
- Effective use of multiple cores and nodes can significantly speed up research tasks.
- High-performance computing clusters and cloud computing offer powerful resources for research.
- Identifying and solving research bottlenecks can improve overall productivity.
---

## Overview



## Today's focus
Today we will consider an example task that is integral to our research work, but is taking a long time to complete.
The completion of this task is a bottleneck for progress.


## Making things go faster

When most people want to make their code or workflow faster, they think of optimisation.
Specifically, code optimisation.

Before we engage in any kind of optimization, there are a few things we should do first:
- Understand what the problem is (or rather, confirm a problem exists)
- Measure the current state of things (benchmark + first profile)
- Have a target in mind for what is "good enough"

When thinking about the problem, remember that your code doesn't run in isolation.
It runs as part of a larger workflow, that includes other pieces of code as well as non-automated things like researcher thinking time.
Consider your entire workflow, and how much time is spent on waiting for code to run vs you analyzing results.
If you have other useful work that can be done while your code runs, then do that, it'll be time well spent.

**Amdahl's Law**: 
- System speed-up limited by the slowest component.

**Paul’s rule of thumb**: 
- You are the slowest component.

**Therefore**: 
1. Focus on reducing **your** active interaction time,
2. *then* on your total wait time, 
3. *then* on cpu time.

A reason to confirm that we *need* to optimize our code is that we want to avoid premature optimization:
[![ObligatoryXKCD](https://imgs.xkcd.com/comics/is_it_worth_the_time.png)](https://xkcd.com/1205/)

### Example workflow
Suppose that we have a workflow that is composed of some number of sub-tasks.
In the simplest case, this workflow isn't really a "flow" - it's just a list of things to do that don't depend on each other.
For argument sake, lets assume there are 50 tasks, each taking 2 mins to compelte, so that the user has to wait 100 minutes between starting the workflow, and seeing it completed.

![Workflow]({{page.root}}{% link fig/WallTimeSerial.png %})

In general you have the following options available to you:
1. Do nothing.
    - Accept that the time taken is unchangable and just make do. 
    - This requires zero investment of time, and is a good option if you never plan to run the workflow more than once.
2. Make the individual tasks take less time:
    - Optimise the code to be more efficient (typically large time investment)
    - Run the same code on faster hardware (typically small time investment)
3. Do multiple tasks at once:
    - Run one task per cpu available (being aware of RAM limits)
    - Run your workflow on multiple computers at once (desktops, or nodes of an HPC)
4. Skip some of the tasks:
    - Save the outputs of each task, and only re-run them as needed (checkpointing or caching)
    - Caching is a typical [space-time tradeoff](https://en.wikipedia.org/wiki/Space%E2%80%93time_tradeoff) but is also one of the [Two hard problems in computing](https://martinfowler.com/bliki/TwoHardThings.html)

We are going to not engage in 1 because there is nothing to teach.
We will not exlpore 4 except to say that [`make`](https://www.gnu.org/software/make/manual/make.html) and [`NextFlow`](https://www.nextflow.io/) both have a caching mechanism that you can use without having to write any extra code.
The focus of today's workshop will be on 2 and 3 - making things faster and doing more work at once.

## Writing performant code

Code optimization is the process of improving the efficiency of your code to reduce execution time, memory usage, or other resource consumption.
However, optimization should be approached carefully to avoid unnecessary complexity or premature efforts.
Below are key considerations and strategies for optimizing code (for speed):

1. **When to Optimize**
    - **Measure First**: Use profiling tools (e.g., `cProfile`, `line_profiler`) to identify bottlenecks in your code.
    - **Set Goals**: Define what "good enough" performance looks like for your use case.
    - **Avoid Premature Optimization**: Focus on correctness and clarity first; optimize only when necessary.
2. **General Strategies**
    - **Use Efficient Algorithms**: Choose algorithms with better time and space complexity for your problem.
    - **Leverage Existing Libraries**: Libraries like `numpy`, `pandas`, and `scipy` are highly optimized for performance.
    - **Minimize Redundant Computations**: Cache results of expensive operations if they are reused (e.g., memoization).
3. **Python-Specific Tips**
    - **Vectorization**: Replace loops with vectorized operations using libraries like `numpy`.
    - **Data Structures**: Use appropriate data structures (e.g., `set` for membership checks, `deque` for queues).
    - **Avoid Global Variables**: Accessing global variables can slow down your code due to namespace lookups.
4. **Iterative Optimization**
    - **Test After Each Change**: Ensure that optimizations do not introduce bugs or regressions.
    - **Benchmark**: Use tools like `timeit` to measure the impact of your changes.

In this workshop we aren't going to do any optimisation, for that you can check out our other lessones [here](https://adacs-australia.github.io/2023_ASA_ECR_Python_Workshop/Optimization/index.html) or [here](https://adacs-australia.github.io/2023-03-20-Coding-Best-Practices-Workshop/Optimization/index.html).
Instead, we will talk about how you can write code that is likely be to be "pretty fast" or "good enough" to start with - performant code.

### Don't repeat others

The first thing to note is that other people have been writing code for a lot longer than you have and there are some true experts out there that spend a lot of time making their code as fast as possible.
Rather than trying to compete with them, or reproduce their efforts, you should look to build upon their success.
So before you start to code up some functions, workflows, or libraries, have a look online and see if you can find some existing libraries.
Some excellent examples that most people likely alreay use are `numpy`, `scipy`, `pandas`, and `astropy`.
These libraries are developed by teams of folks who pay close attention to getting the right answer, in the shortest time possible, and usually without exploding your RAM.

Places to look for useful libraries:
- Your peers and collaborators - ask what other people are using (bonus, they also be a good source of help when things go bad),
- [PyPI (Python Package Index)](https://pypi.org/) - the go-to source for Python packages (both good and bad),
- [GitHub](https://github.com), as above, but not specific to python, probably a large fraction of not-great things,
- The acknowledgements section of papers you read - some kind souls mention/cite their code.

> ## What are some of your go-to libraries?
> Let us know an not-yet mentioned library that you often use in your work.
> Give a 1 sentence description of what the library is designed for.
>
> Use the [collaborative notes]({{page.collaborative_notes}}) or the zoom chat to share.
>
{: .challenge}


Using existing libraries means that you'll be importing functions, but also data structures.
It is good practice to use the recommended data structures with the given library functions as this reduces the amount of type casting and conversion work that needs to be done.
Let's explore how this would work using an example from `numpy`.

For a basic example we'll consider performing an operation on two sets of data.
Supposed we have two lists of integers (A and B), and we want to add them together (C = A + B).

> ## Add two python lists
> Using `ipython` do the following and observe the output:
> ~~~
> A_list=list(range(10_000))
> B_list=list(range(10_000))
> 
> %timeit C_list = [ a+b for a,b in zip(A_list,B_list)]
> ~~~
> {: .language-python}
> > ## Output
> > Depending on the speed of your computer you'll get something like this:
> > ~~~
> > 295 μs ± 26.5 μs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

Now let us use the numpy data types.
These are numpy arrays rather than python lists.

> ## Add two numpy arrays
> Again using `ipython`, do the following and observe the output:
> ~~~
> # assuming the same session as before
> import numpy as np
> A = np.array(A_list)
> B = np.array(B_list)
> %timeit C = A+B
> ~~~
> {: .language-python}
> > ## Output
> > Depending on the speed of your computer you'll get something like this:
> > ~~~
> > 2.01 μs ± 71.7 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
> > ~~~
> > {: .output}
> > ![MindBlown](https://www.reactiongifs.us/wp-content/uploads/2017/07/Mind-Blow-2.gif)
> {: .solution}
{: .challenge}

So we have a speed up of about 100x (for that one operation), just by using `numpy` data types and leveraging the fast algebra that `numpy` provides.
`numpy` contains more than just basic math functions.
In fact many of the linear algebra operations that you would want to perform on arrays, vectors, or matrices (in the `numpy.linalg` module), call on powerful system level libraries such as OpenBLAS, MKL, and ATLAS.
These libraries, in turn, are multi-threaded or multi-core enabled, so in many cases you'll also be able to make use of multiple cores, without having to explicitly deal with the multiprocessing library, just by using `numpy` or `scipy` functions.
Some particularly useful examples are the `scipy.optimize` and `scipy.fft` modules.


Other examples of this vectorised approach include:
- `scipy`
    - Because it's a wrapper around `numpy` in many cases.
- `pandas`
    - Operations on columns are vectorised.
- `astropy`
    - Instead of an array of `SkyCoord` objects, create a single `SkyCoord` with arrays of coordinates. Operations on this object will be vectorised.
    - With two `SkyCoord` objects (catalogues) you can run a crossmatch between them. Astropy will do the matching using an algorith much smarter than your "minimum of the all to all comparison".


The main lesson here is that Python is slow but easy to code, and C is fast but hard(er) to code, but by using libraries such as `numpy` you can start to get the benefit of both worlds - easy to code, fast to use.
So, wherever possible, use already built libraries and avoid re-implementing things yourself.

## Scaling Up Your Resources

### Using faster hardware

In the 1980s and 1990s, the performance of computers improved significantly due to increasing CPU clock speeds.
Manufacturers were able to make processors faster by shrinking transistor sizes and improving fabrication techniques.
This trend, often referred to as "Moore's Law," led to a doubling of transistor density approximately every two years, which translated into faster CPUs.
Buying a new computer usually meant you were buying a faster CPU so your programs would run faster.

However, around the early 2000s, this trend began to slow down.
Increasing clock speeds further became challenging due to physical limitations such as heat dissipation and power consumption.
As a result, the focus shifted from making individual cores faster to adding more cores to processors.
This marked the beginning of the multi-core era.

Modern CPUs now often have multiple cores, allowing them to perform many tasks simultaneously.
While individual cores may not be significantly faster than those from the early 2000s, the ability to run multiple processes in parallel has led to substantial performance improvements for workloads that can take advantage of parallelism.
This shift has made understanding and utilizing parallel computing essential for researchers and developers.
Unless you are using a truly ancient piece of hardware, buying a "faster" computer isn't going to make your single CPU task take less time to run.
In fact, a new desktop computer may have 5GHz clockspeed, where as an HPC facility may have CPUs with only a 2.5GHz clockspeed, so running your single core job on an HCP may actually take **longer**.
(This is because HPC facilities provide many more CPU cores than your desktop: 64-128 vs 8-16).


However, if your task is running slow because it is being limited by disk read/writes, then swapping a spinning disk HDD for a SSD or nVME can make this go faster.
Similarly if your task is running slow becase it uses all your RAM, and has to start using disk storage instead ([swapping or paging](https://en.wikipedia.org/wiki/Memory_paging)), then expanding the RAM could make things faster.

### Using more cores

Most programs that you write will be executed on a single CPU core.
Some python libararies (like `numpy`) will use system libraries that can use multiple CPUs, but only for some operations.
While it can be difficult or impossible to rewrite your tasks to make use of multiple CPU cores at once, there is a much simpler option available to us if we look at the level of a workflow.
The solution is to simply run different tasks on different cores.

If we have even a modest desktop computer we could have 8 cores available to us.
If we were to divide our workflow among these 8 cores we could reduce the total execution time from 100 minutes, down to just 12.5 minutes.
The exact same calculations are being done, but because we have deployed 8x as much resources, we can get the job done in 1/8th of the time.
This is what we call task based parallelism.

> ## Not everything can be parallelized
> Some tasks are inherently serial and can't be sped up by applying extra workers.
>
> Two washing can't wash a single load of clothes in 1/2 the time.
> This is because the wash/rinse/spin tasks are sequential and rely on each other.
>
{: .callout}

- How to parallelize and existing workflow.
    - Driver script (xargs) and library (greet.sh)


### Job packing with `xargs`

The program `xargs` is standard on most Unix based systems and was created to "build and execute command lines from standard input".
At its most basic level, `xargs` will accept input from STDIN and convert this into commands which are then executed in the shell.
`xargs` is able to manage the execution of these sub processes that it spawns and thus can be used to run multiple programs in parallel.

We will again simulate a hard task by doing something simple and then sleeping.
In this case we have a script called `greet.sh` ([here]({{page.root}}{% link files/greet.sh %})) which is as follows:

> ## `greet.sh`
> ~~~
> #! /usr/bin/env bash
> 
> echo "$@ to you my friend!"
> sleep 1
> ~~~
> {: .language-bash}
{: .callout}

If we were to have a file which consisted of greetings (`greetings.txt`, [here]({{page.root}}{% link files/greetings.txt %})), one per line, we could use xargs to run our above script with the greeting as an argument:

```bash
xargs -a greetings.txt -L 1 -exec ./greet.sh
```

The `-L 1` instructs xargs to pass one line at a time as arguments to our `-exec` command, and `-a` indicates the input data file.
The above would eventually output the following:

```output
Hello to you my friend!
Gday to you my friend!
Kaya to you my friend!
Kiaora to you my friend!
Aloha to you my friend!
Yassas to you my friend!
Konnichiwa to you my friend!
Bonjour to you my friend!
Hola to you my friend!
Ni Hao to you my friend!
Ciao to you my friend!
Guten Tag to you my friend!
Ola to you my friend!
Anyoung haseyo to you my friend!
Asalaam alaikum to you my friend!
Goddag to you my friend!
Shikamoo to you my friend!
Namaste to you my friend!
Merhaba to you my friend!
Shalom to you my friend!
```

You'll see that the `sleep 1` command means that each greeting is followed by a pause, and that we only get one greeting at a time.
The code is being executed on a single CPU core sequentially.

![SerialHello]({{page.root}}{% link fig/SerialHello.png %})

If we want to work with 8 tasks in parallel we can do so using the `-P 8` argument to xargs:

```bash
xargs -a greetings.txt -L 1 -P 8 -exec ./greet.sh
```

You'll see that we get the same output as before (maybe in a different order) but that it occurs in batches of 8, with an approximately 1 second pause between them.
What is happening now is that the waiting time is happening in parallel rather than in serial.
If we replaced the `sleep 1` command with some actual work that needs to be done then we'd be making use of multiple cores in no time!

![ParallelHello]({{page.root}}{% link fig/ParallelHello.png %})

By using `xargs` we can create a single job file that will spawn multiple tasks (up to some maximum) that will run concurrently.
Moreover, if we have more tasks to complete than CPU cores available, `xargs` will wait for a task to complete before starting another.


## Planning your workflow for speed
- Planning a workflow
    - Map tasks
    - Map all dependencies
    - map-reduce
    - Note parallel execution opportunities
    - Ahmdahls' law again


### Amdahl's Law
Identify which parts of your code / workflow have to be done in serial, and which parts can be done in parallel.
Amdahl's law gives you an estimate of the speed up factor.

![Amdahls Law]({{page.root}}{% link fig/AmdahlFormula.png %})


## Using multiple cores the hard(er) way


- Concepts of shared memory vs distributed memory systems
    - multiprocessing in python
    - shared memory in python
    - MPI (hard to do examples since needs library)
    - hybrid workflows


## Using many-many-many more cores (HPC)
- How to make use of HPC for faster results
    - HPC infrastructure and scheduling
    - Using a "full node" to the best of your ability
    - Array jobs
    - Hybrid arrays jobs + job packing (eg xargs)


## Further discussion points