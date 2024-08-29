---
title: Shifted Virtual BF Images
toc: false
style: css/custom.css
---

<script type="module" src="https://cdn.jsdelivr.net/npm/@marimo-team/islands@0.6.19/dist/main.js"></script>
<link
    href="https://cdn.jsdelivr.net/npm/@marimo-team/islands@0.6.19/dist/style.css"
    rel="stylesheet"
    crossorigin="anonymous"
/>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link
    rel="preconnect"
    href="https://fonts.gstatic.com"
    crossorigin
/>
<link href="https://fonts.googleapis.com/css2?family=Fira+Mono:wght@400;500;700&amp;family=Lora&amp;family=PT+Sans:wght@400;700&amp;display=swap" rel="stylesheet" />
<link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css"
    integrity="sha384-wcIxkf4k558AjM3Yz3BBFQUbk/zgIYC2R0QpeeYb+TwlBVMrlgLqwRjRtGZiK7ww"
    crossorigin="anonymous"
/>

```js
const marimo_html = await FileAttachment("data/bf-images-stack.html").html();
```

# Shifted Virtual BF Images

- Tilted plane-wave illumination &rarr; image shifts[^1]
  - Depends on the gradient of the aberration function -- notably defocus[^2]

<div class="card" style="background: var(--theme-foreground);">
  <div id="marimo-island"> ${marimo_html.body} </div>
</div>

[^1]: Dose-Efficient Cryo-Electron Microscopy for Thick Samples using Tilt-Corrected Scanning Transmission Electron Microscopy, Demonstrated on Cells and Single Particles, [bioRxiv 2024.04.22.590491](https://www.biorxiv.org/content/10.1101/2024.04.22.590491v1) 
[^2]: Iterative Phase Retrieval Algorithms for Scanning Transmission Electron Microscopy, [arXiv:2309.05250](https://arxiv.org/abs/2309.05250)
