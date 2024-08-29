---
toc: false
style: css/index.css
---

```js
import { raster_plot } from "./components/rasterPlot.js";
const reconstructions = new Float64Array(
  await FileAttachment(
    "./data/scaled_reconstructions_2x3x256x256.npy",
  ).arrayBuffer(),
);
const n = 256 ** 2;
```

:::hero

# Transfer of Information in (Iterative) Phase Retrieval Methods

:::

<div class="grid grid-cols-3" style="grid-auto-rows: auto;">
  <div class="img-container" style="min-height:200px;">
    ground truth potential
    ${resize((width,height)=> raster_plot(reconstructions.slice(0 * n, 1 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    Zernike phase plate
    ${resize((width,height)=> raster_plot(reconstructions.slice(1 * n, 2 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    "complex" ptychography
    ${resize((width,height)=> raster_plot(reconstructions.slice(2 * n, 3 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    tilt-corrected BF-STEM
    ${resize((width,height)=> raster_plot(reconstructions.slice(3 * n, 4 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    regular ptychography
    ${resize((width,height)=> raster_plot(reconstructions.slice(4 * n, 5 * n ),Math.min(width,height-26), null, false))}
  </div>
  <div class="img-container" style="min-height:200px;">
    STEM-H ptychography
    ${resize((width,height)=> raster_plot(reconstructions.slice(5 * n, 6 * n ),Math.min(width,height-26), null, false))}
  </div>
</div>

::: hero

Georgios Varnavides | National Center for Electron Microscopy  
Follow along! https://gvarnavides.com/2024emc-ctf/

:::
