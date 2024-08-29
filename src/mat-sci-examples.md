---
title: Material Science Examples
toc: false
style: css/custom.css
---

```js
const img_Ti = FileAttachment("data/mat-sci-examples_Ti.png").href;
const img_hBN = FileAttachment("data/mat-sci-examples_hBN.png").href;
//const img_Au = FileAttachment("data/mat-sci-examples_Au-Carbon.png").href;
const img_cmos = FileAttachment("data/mat-sci-examples_cmos.png").href;
const img_STO_top = FileAttachment("data/mat-sci-examples_STO-top.png").href;
const img_STO_middle = FileAttachment(
  "data/mat-sci-examples_STO-middle.png",
).href;
const img_STO_bottom = FileAttachment(
  "data/mat-sci-examples_STO-bottom.png",
).href;
const img_coreshell_top = FileAttachment(
  "data/mat-sci-examples_core-shell-top.png",
).href;
const img_coreshell_middle = FileAttachment(
  "data/mat-sci-examples_core-shell-middle.png",
).href;
const img_coreshell_bottom = FileAttachment(
  "data/mat-sci-examples_core-shell-bottom.png",
).href;
const img_style = "object-fit:contain;";

import { return_resized_img } from "./components/ImageUtilities.js";
```

# Materials Science Reconstructions

- Reconstructions of a variety of materials classes[^1]
  - 2D materials as-well as "thick" objects (multislice)
- Reconstructions using a number of different detectors
  - low (4D Camera, K3) / high (EMPAD, Arina) dynamic range
  - even on a CMOS detector!

<div class="grid grid-cols-3" style="grid-auto-rows: auto;">
  <div class="img-container" style="min-height:300px;">
    Ti islands on graphene
    ${resize((width,height)=> return_resized_img(img_Ti,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    few-layer hBN
    ${resize((width,height)=> return_resized_img(img_hBN,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    low-voltage CMOS detector
    ${resize((width,height)=> return_resized_img(img_cmos,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    STO bottom-layer
    ${resize((width,height)=> return_resized_img(img_STO_bottom,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    STO middle-layer
    ${resize((width,height)=> return_resized_img(img_STO_middle,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    STO top-layer
    ${resize((width,height)=> return_resized_img(img_STO_top,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    Core-shell bottom-layer
    ${resize((width,height)=> return_resized_img(img_coreshell_bottom,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    Core-shell middle-layer
    ${resize((width,height)=> return_resized_img(img_coreshell_middle,width,height-16,img_style))}
  </div>
  <div class="img-container" style="min-height:300px;">
    Core-shell top-layer
    ${resize((width,height)=> return_resized_img(img_coreshell_top,width,height-16,img_style))}
  </div>
</div>

[^1]: Sample & Imaging credit: K.Reidy, D. Byrne, F. Allen, B. Cohen, H. Shih, E. Hoglund, D. Kepaptsoglou, C. Ophus, S. Ribet
