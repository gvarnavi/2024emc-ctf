---
toc: false
style: css/index.css
---

```js
// IMAGES
const img_src_image = FileAttachment(
  "./data/demo_image_small.gif",
).href;
const img_src_movie = FileAttachment(
  "./data/demo_movie_smaller.gif",
).href;
const img_src_volume = FileAttachment(
  "./data/demo_3d_small.gif",
).href;

import { return_resized_img } from "./components/ImageUtilities.js";
```

:::hero

# Elemental Microscopy Demo

## [elementalmicroscopy.com](https://www.elementalmicroscopy.com)

:::

<div class="grid grid-cols-3" style="grid-auto-rows: auto;">
  <div class="img-container" style="min-height:300px;">
    Interactive Images
    ${resize((width,height)=> return_resized_img(img_src_image,width,"auto;"))}
  </div>
  <div class="img-container" style="min-height:300px;">
    Interactive Movies
    ${resize((width,height)=> return_resized_img(img_src_movie,width,"auto;"))}
  </div>
  <div class="img-container" style="min-height:300px;">
    Interactive Volumes
    ${resize((width,height)=> return_resized_img(img_src_volume,width,"auto;"))}
  </div>
</div>

