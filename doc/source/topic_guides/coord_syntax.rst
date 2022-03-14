.. _coord_mini_language:

The Site/Coordinate Syntax
============================

In the atomistic kMC simulations pursued here
one defines processes in terms of sites
on some more or less fixed lattice.
This reflects the physical observation that
molecules on surfaces adsorb on very specific
locations above a solid.

To represent this in a computer program, we first need to
make a small but crucial differentiation: namely the difference
between the *sites* of a (surface) structure and the *coordinates*
of a process. The difference is that a given structure contains
each site defined exactly once, whereas a process may use the same
site several times however in a different unit cell. So this
differentation owes to the fact that we commonly simulate highly
periodic structures.


Ok, having this out of the way you start to define
and use sites and coordinates. The minimum constructor for a
site is ::

  site = Site(name='site_name')

where ``site_name`` can be a string without spaces and all names
should be unique within one layer. Usually it is reasonable to
add a position in relative coordinates right-away like so ::

  site = Site(name='hollow', pos='0.5 0.5 0.0')

which would place the site at the bottom center of the cell. A direct
benefit is that you can measure distances between coordinates
later on to, e.g. select all nearest neighbor or next-nearest neighbor
sites.

A site can have some more attributes. Some of them are only needed
in conjunction with GUI use. It is worth to know that each site
can have one or more tags. This way one create types of site and
conveniently select all sites with a one more tags. The syntax here
is as follows ::

  site = Site(name='hollow', pos='0.5 0.5 0.0', tags='tag1 tag2 ...')



The second part is to generate the coordinates that are
used in the process description.

.. _manual_coord_generation:

Manual generation
^^^^^^^^^^^^^^^^^
To quickly generate single coordinates you can generate it
from a Project like so ::

  kmc_model.lattice.generate_coord('hollow.(0,0,0).layer_name')

Let's look at the generation string. The general syntax is ::

  site_name.offset.layer_name

The ``site_name`` and the ``layer_name`` must have been defined before.
The offset is a tuple of three integer numbers `(0, 0, 1)` and specifies the
relative unit cell of this coordinate. Of course this only becomes meaningful
as soon as you use more than one coordinate in a process.

Missing values will be filled in from the back using default values,
such that ::
  
    site -> site.(0,0,0) -> site.(0,0,0).default_layer

Advanced Coordinate Techniques
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generating large process lists with a lot of similar or even
degenerate processes is a very boring task. So we should try
to use programming logic as much as possible. Here I will outline
a couple of idioms you can use here.

Often times it is handier (less typing) to generate a larger set
of coordinates at first and then select different subsets from it
in a process definition. For this purpose you can use ::

  pset = kmc_model.lattice.generate_coord_set(size=[x,y,z], layer_name='layer_name')


This collects all sites from the given layer and generates
all coordinates in the first unit cell (``offset=(1,1,1)``)
and all ``x``, ``y``, and ``z`` unit cells in the respective
direction.

To select subsets in a readable way I suggest you use list comprehensions,
like so ::

  [ x for x in pset if not x.offset.any() ]

which again selects all sites in the first unit cell. Or to select all
site tagged with ``foo`` you could use ::

  [ x for x in pset if 'foo' in x.tags.split() ]

or having defined a unit cell size and a site position your can measure
real-space distances between coordinate like so ::

  np.linalg.norm(x.pos-y.pos)

Or of course you can use any combination of the above.

Taking it home
^^^^^^^^^^^^^^

- *sites* belong to a *structure* while *coordinates* belong to a *process*
- coordinates are generated from sites
- coordinate sets can be selected and chopped using list comprehensions
  and tags
