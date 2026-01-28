from monarch.actor import Actor, endpoint, this_host

# spawn trainer processes on this host
num_workers = 8
counting_procs = this_host().spawn_procs({"workers": num_workers})


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

first_counters = counters.slice(workers=slice(0, num_workers // 2))
last_counters = counters.slice(workers=slice(num_workers // 2, num_workers))

# Do some counting
for _ in range(10):
    # Don't need a return value, so broadcast instead of call
    first_counters.increment.broadcast()
    last_counters.increment.broadcast()

# More counting, only on the second set of counters
for _ in range(10):
    last_counters.increment.broadcast()

# Get counts
counts = counters.get_count.call()
print(f"{counts.get()=}")
