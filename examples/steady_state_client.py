#!/usr/bin/env python
"""An example script that shows how to use the initial bias detection
and sample steady-state data.
"""

import kmcos.run
import kmcos.run.steady_state
with kmcos.run.KMC_Model(banner=False, print_rates=False) as model:
    hist = kmcos.run.steady_state.sample_steady_state(
        model, 100000, tof_method='integ', show_progress=True, make_plots=True)
print(model.get_std_header())
print(hist)
