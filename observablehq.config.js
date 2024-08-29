// See https://observablehq.com/framework/config for documentation.
import MarkdownItContainer from "markdown-it-container";
import MarkdownItFootnote from "markdown-it-footnote";

const head = `
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16x16.png">
<link rel="manifest" href="/assets/site.webmanifest">
`;

export default {
  title: "2024 EMC, Transfer of Information",
  head: head,
  root: "src",
  theme: "dark",
  typographer: true,
  markdownIt: (md) =>
    md
      .use(MarkdownItContainer, "card") // ::: card
      .use(MarkdownItContainer, "hero") // ::: hero
      .use(MarkdownItFootnote), // [^1] or [^longnote],
  pages: [
    {
      name: "Phase-Retrieval Background",
      open: false,
      collapsible: true,
      pages: [
        { name: "4D-STEM Measurements", path: "4dstem-measurements" },
        { name: "Phase Problem", path: "phase-problem" },
      ],
    },
    {
      name: "Electron Ptychography",
      open: false,
      collapsible: true,
      pages: [
        {
          name: "Proximal Gradient Methods",
          path: "proximal-gradient-methods",
        },
        { name: "Electron Ptychography", path: "electron-ptychography" },
      ],
    },
    {
      name: "Tilt-Corrected BF-STEM",
      open: false,
      collapsible: true,
      pages: [
        {
          name: "STEM-CTEM Reciprocity",
          path: "stem-ctem-reciprocity",
        },
        { name: "Shifted Virtual BF Images", path: "bf-images-stack" },
      ],
    },
    {
      name: "Open Source Phase Retrieval",
      open: false,
      collapsible: true,
      pages: [
        {
          name: "py4DSTEM Phase Retrieval",
          path: "py4dstem-phase-retrieval",
        },
        { name: "Materials Science Examples", path: "mat-sci-examples" },
        { name: "Life Science Examples", path: "bio-examples" },
      ],
    },
    {
      name: "Transfer of Information",
      open: false,
      collapsible: true,
      pages: [
        {
          name: "Experimental SNR Observations",
          path: "ctf-exp",
        },
        { name: "Transfer of Information in PCI", path: "ctf-models" },
        { name: "Ultimate Dose Efficiency Limits?", path: "ctf-limits" },
      ],
    },
    {
      name: "Conclusions",
      open: false,
      collapsible: true,
      pages: [
        { name: "Acknowledgments", path: "acknowledgments" },
        { name: "About This Presentation", path: "about" },
      ],
    },
  ],
};
