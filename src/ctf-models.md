---
title: Transfer of Information in PCI
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
const marimo_html = await FileAttachment("data/ctf-models.html").html();

const ctf_00_img = FileAttachment("data/ctf_00.svg").href;
const ctf_01_img = FileAttachment("data/ctf_01.svg").href;

import { return_resized_img } from "./components/ImageUtilities.js";
```

```js
function return_schematics_tab() {
  return html`
    <details open>
      <summary> Error schematics </summary>
      ${tab_input}
      <div class="card" style="background: var(--theme-foreground);">
        <div class="img-container">
          ${resize((width) =>
            return_resized_img(ctf_00_img, width, "auto;"),
          )}
        </div>
      </div>
    </details>
  `;
}

function return_phase_diagram_tab() {
  return html`
    <details open>
      <summary> Error schematics </summary>
      ${tab_input}
      <div class="card" style="background: var(--theme-foreground);">
        <div class="img-container">
          ${resize((width) =>
            return_resized_img(ctf_01_img, width, "auto;"),
          )}
        </div>
      </div>
    </details>
  `;
}
```

# Transfer of Information in PCI

```js
const tab_input = Inputs.radio(
  [
    "schematics",
    "phase diagram",
  ],
  { value: "schematics" },
);
const tab = Generators.input(tab_input);
```

```js
if (tab == "schematics") {
  display(return_schematics_tab());
} else if (tab == "phase diagram") {
  display(return_phase_diagram_tab());
}
```

<details>
<summary> SNR Models </summary>
<div class="card" style="background: var(--theme-foreground);">
  <div id="marimo-island"> ${marimo_html.body} </div>
</div>
</details>
