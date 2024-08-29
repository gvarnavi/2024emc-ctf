---
title: py4DSTEM Phase Retrieval
toc: false
style: css/custom.css
---

```js
const py4dstem_svg = FileAttachment(
  "data/py4dstem-phase-retrieval.svg",
).image();
```

# Open-Source Phase Retrieval

<div id="py4dstem-container"> ${py4dstem_svg} </div>

- Suite of phase retrieval algorithms, including iterative DPC, **ptychography**, and parallax (tc-BF)
- User-friendly, object-oriented code
  - Check out our tutorial notebooks[^1] and recent preprint[^2]
  - Dataset credit[^3]

:::card

```python
ptycho = py4DSTEM.process.phase.SingleslicePtychography(
    datacube=dataset,
    # device = 'gpu', # GPU acceleration
    energy = 80e3,
    semiangle_cutoff = 21.4, # mrad
).preprocess(
    plot_center_of_mass = False,
).reconstruct(
    num_iter = 8,
    step_size = 0.5,
    gaussian_filter_sigma = 0.2,
).visualize(
)
```

:::

[^1]: https://github.com/py4dstem/py4DSTEM_tutorials/tree/main/notebooks

[^2]: Iterative Phase Retrieval Algorithms for Scanning Transmission Electron Microscopy, [arXiv:2309.05250](https://arxiv.org/abs/2309.05250)

[^3]: 4D-STEM dataset used was recorded by Zhen Chen, at Cornell: [Electron ptychography of 2D materials to deep sub-ångström resolution](https://www.nature.com/articles/s41586-018-0298-5)
