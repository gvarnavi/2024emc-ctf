---
title: Life Sciences Examples
toc: false
style: css/custom.css
---

```js
const img_VLP = FileAttachment("data/yues-vlps.svg").href;
const img_Apo = FileAttachment("data/berks-apo.svg").href;
const img_TMV = FileAttachment("data/berks-tmv.svg").href;

const img_style = "object-fit:contain;";
import { return_resized_img } from "./components/ImageUtilities.js";
```

# Life Sciences Examples

- Dose-efficient phase-retrieval methods &rarr; detect weakly scattering signals
  - Image dose-sensitive materials &rarr; biological samples

<details open>
<summary> Virus-like particles (parallax) </summary>
<div class="card" style="background: white;">
  <div class="img-container">
    ${resize((width)=> return_resized_img(img_VLP,width,"auto;",img_style))}
    <div style="color: var(--theme-background);"> In collaboration with Dr. Y. Yu, CZII </div>
  </div>
</div>
</details>

<details open>
<summary> Apoferritin proteins (ptychography) </summary>
<div class="card" style="background: white;">
  <div class="img-container">
    ${resize((width)=> return_resized_img(img_Apo,width,"auto;",img_style))}
    <div style="color: var(--theme-background);"> In collaboration with B. Küçükoglu, EPFL </div>
  </div>
</div>
</details>

<details open>
<summary> Tobacco Mosaic virus (ptychography) </summary>
<div class="card" style="background: white;">
  <div class="img-container">
    ${resize((width)=> return_resized_img(img_TMV,width,"auto;",img_style))}
    <div style="color: var(--theme-background);"> In collaboration with B. Küçükoglu, EPFL </div>
  </div>
</div>
</details>
