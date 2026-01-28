from monarch.actor import Actor, MeshFailure, endpoint, this_host

# spawn trainer processes on this host
procs = this_host().spawn_procs({"workers": 2})


# define the actor to run on each process
class SupervisingActor(Actor):
    @endpoint
    def error(self):
        raise ValueError("I don't want to be here")

    def __supervise__(self, failure: MeshFailure):
        print(f"Catching {failure=}")
        # Return something truthy to indicate the error was handled
        return True


# create the trainers
supervisors = procs.spawn("supervisors", SupervisingActor)

# tell all the trainers to to take a step
fut = supervisors.error.call()
# wait for all trainers to complete
fut.get()
