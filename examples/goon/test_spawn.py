from monarch.actor import Actor, endpoint, this_host

# spawn trainer processes on this host
# training_procs = this_host().spawn_procs({"gpus": 2})
training_procs = this_host().spawn_procs({"workers": 20})

# define the actor to run on each process
class Trainer(Actor):
    @endpoint
    def train(self, step: int):
        print(f"Training {step=}")


# create the trainers
trainers = training_procs.spawn("trainers", Trainer)

# tell all the trainers to to take a step
for step in range(10):
    fut = trainers.train.call(step=step)
    # wait for all trainers to complete
    fut.get()
