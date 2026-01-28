# learn_monarch Branch

Branch purpose: Write small standalone examples and learn the Monarch codebase.

## Response Style
- Short answers with direct file:line pointers
- Prefer pointing to existing code over lengthy explanations
- Reference tests as usage examples

## What is Monarch?
Distributed PyTorch framework using actor messaging. Core concepts:
- **Actors**: Isolated computation units with `@endpoint` methods for remote calls
- **Meshes**: Multidimensional actor collections (HostMesh → ProcMesh → ActorMesh)
- **Futures**: Async results from endpoint calls
- **Supervision**: Fault tolerance via parent-child actor trees

## Key Files

### Python Core
- `python/monarch/_src/actor/actor_mesh.py` — Actor/ActorMesh implementation
- `python/monarch/_src/actor/endpoint.py` — `@endpoint` decorator, `call`/`broadcast`/`choose`
- `python/monarch/_src/actor/proc_mesh.py` — ProcMesh, spawning actors
- `python/monarch/_src/actor/host_mesh.py` — HostMesh, spawning processes
- `python/monarch/_src/actor/future.py` — Future class
- `python/monarch/_src/actor/supervision.py` — Fault handling

### Public API
- `python/monarch/__init__.py:68-167` — All public exports
- `python/monarch/actor/__init__.py` — Actor subsystem exports

### Documentation
- `docs/source/actors.md` — Actor lifecycle, messaging patterns
- `docs/source/examples/getting_started.py` — Introductory tutorial
- `MONARCH_INFO.md` — Dev guide, build info

### Tests (good usage examples)
- `python/tests/test_python_actors.py` — Actor/endpoint patterns
- `python/tests/_monarch/` — Main API tests

### Rust Core
- `hyperactor/src/lib.rs:1-56` — Actor model overview
- `hyperactor_mesh/` — Mesh topology, multicast

## Common Patterns

### Minimal Actor
```python
from monarch.actor import Actor, endpoint, this_proc

class Counter(Actor):
    def __init__(self):
        self.value = 0

    @endpoint
    def incr(self) -> None:
        self.value += 1

    @endpoint
    def get(self) -> int:
        return self.value
```

### Endpoint Call Types
- `actor.method.call()` → `Future[ValueMesh[R]]` (broadcast, collect all)
- `actor.method.broadcast()` → `None` (fire-and-forget)
- `actor.method.call_one()` → `Future[R]` (single actor)
- `actor.method.choose()` → `Future[R]` (load-balanced pick)

### Spawning
```python
proc = this_proc()                    # Get current process
actor = proc.spawn("name", MyActor)   # Spawn actor in proc
```

## Build & Test
```bash
uv sync
uv run pytest python/tests/test_python_actors.py -v -m "not oss_skip"
```

## Examples Directory
`examples/goon/` — Simple standalone examples for this learning branch
