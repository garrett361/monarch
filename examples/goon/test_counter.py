from monarch.actor import Actor, endpoint, this_host

# spawn trainer processes on this host
counting_procs = this_host().spawn_procs({"workers": 20})
# counting_procs = this_host().spawn_procs({"gpus": 2})


# define the actor to run on each process
class Counter(Actor):
    def __init__(self, count: int = 0) -> None:
        self.count = count

    @endpoint
    def increment(self) -> None:
        self.count += 1

    @endpoint
    def get_count(self) -> int:
        return self.count


# create the counters
counters = counting_procs.spawn("counters", Counter)

# Do some counting
for _ in range(10):
    # Don't need a return value, so broadcast instead of call
    counters.increment.broadcast()

# Get counts
counts = counters.get_count.call()
print(f"{counts.get()=}")
