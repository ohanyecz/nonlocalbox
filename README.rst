NonlocalBox
===========

**A friendly API for simulating nonlocal no-signalling correlations.**

Installation
------------

The easiest way to install ``NonlocalBox`` is to use the ``pip`` command:

.. code:: sh

    python -m pip install nonlocalbox

You may need to replace ``python`` with the correct Python interpreter, e.g., ``python3``.

Usage
-----
The following example illustrates a simple game between Alice and Bob. First, we
need to create two instances of ``NonlocalBox``, one for Alice and one for Bob:

.. code:: python

    from os import environ
    from nonlocalbox import NonlocalBox

    alice_game = NonlocalBox(environ["ALICE_API_KEY"])
    bob_game = NonlocalBox(environ["BOB_API_KEY"])

In the current state, neither of them are in any role. Suppose that Alice invites
Bob for a simulation, whose username is known by Alice (which is 'bob' in this case).
Alice wants to use Popescu-Rohrlich Box of box ID 1 and names it 'hellothere':

.. code:: python

    alice_game.invite("bob", 1, 'hellothere')
    print(alice_game.box_id)  # this is arbitrary
    4

In the server side, Bob is automatically added to this box. They both should
initialize the newly created box with ID 4. This will set the role 'Alice'
to Alice and 'Bob' to Bob (since there won't be any box in Bob's list with ID 4):

.. code:: python

    alice_game.initialize(4)
    bob_game.initialize(4)

They can use the nonlocal boxes to run a simulation.

Suppose Alice sends `x = 0` are her input to the box with transaction ID ``20220311001`` and
Bob sends `y = 0` with the same transaction ID. Note that for `x = y = 0` the results should
be correlated:

.. code:: python

    print(alice_game.use(0, "20220311001"))
    0
    print(bob_game.use(0, "20220311001"))
    0

Now suppose Bob will be the first to send `y = 1` with an incremented transaction ID, and
Alice also sends `x = 1`. The results should be anticorrelated:

.. code:: python

    print(bob_game.use(1, "20220311002"))
    1
    print(alice_game.use(1, "20220311002"))
    0

