---
title: Proximal Gradient Methods
toc: false
style: css/custom.css
---

```js
import * as nj from "npm:numjs";
import {
  region_nearest_convex_red,
  region_nearest_convex_blue,
  region_nearest_nonconvex_red,
  region_nearest_nonconvex_blue,
  region_nearest_flower_green,
  generalized_projection,
  generalized_projection_multiple,
} from "./components/ProjectionSetsHelperFunctions.js";
```

```js
// CONSTANTS

const named_projection_parameters = {
  AP: { a: 0, b: 1, c: 1 },
  DM: { a: -1, b: 1, c: 2 },
  RRR: {
    a: -projection_inputs_a.projection_gamma,
    b: projection_inputs_a.projection_gamma,
    c: 2,
  },
  RAAR: {
    a: 1 - 2 * projection_inputs_a.projection_gamma,
    b: projection_inputs_a.projection_gamma,
    c: 2,
  },
};

function return_flower_values() {
  const theta = nj.arange(0, 2 * Math.PI, Math.PI / 512);
  const origin = [
    (-5 / 4) * Math.cos(Math.PI / 8),
    (-5 / 4) * Math.sin(Math.PI / 8),
  ];

  const radius = nj.sin(theta.multiply(4)).divide(4).add(1);
  const x_values = radius.multiply(nj.cos(theta)).subtract(origin[0]).divide(3);
  const y_values = radius.multiply(nj.sin(theta)).subtract(origin[1]).divide(3);

  return nj.stack([x_values, y_values], -1);
}

const flower_values = return_flower_values();
```

```js
// PROJECTION FUNCTIONS

const two_convex_sets = generalized_projection(
  region_nearest_convex_red,
  region_nearest_convex_blue,
  [
    projection_inputs_b.projection_a,
    projection_inputs_b.projection_b,
    projection_inputs_b.projection_c,
  ],
);

const two_nonconvex_sets = generalized_projection(
  region_nearest_nonconvex_red,
  region_nearest_nonconvex_blue,
  [
    projection_inputs_b.projection_a,
    projection_inputs_b.projection_b,
    projection_inputs_b.projection_c,
  ],
);

const three_nonconvex_sets = generalized_projection_multiple(
  region_nearest_nonconvex_red,
  region_nearest_nonconvex_blue,
  region_nearest_flower_green,
  [
    projection_inputs_b.projection_a,
    projection_inputs_b.projection_b,
    projection_inputs_b.projection_c,
  ],
);
```

```js
// MUTABLE VALUES

const default_values = [
  [
    [1, 0.3],
    [1, 0.3],
    [1, 0.3],
  ],
];

const iteration_pts_convex = Mutable(default_values);
const iteration_pts_nonconvex = Mutable(default_values);
const iteration_pts_flower = Mutable(default_values);

const append_convex_pts = (val) =>
  (iteration_pts_convex.value = [...iteration_pts_convex.value, val]);
const append_nonconvex_pts = (val) =>
  (iteration_pts_nonconvex.value = [...iteration_pts_nonconvex.value, val]);
const append_flower_pts = (val) =>
  (iteration_pts_flower.value = [...iteration_pts_flower.value, val]);

const reset_convex_pts = () => (iteration_pts_convex.value = default_values);
const reset_nonconvex_pts = () =>
  (iteration_pts_nonconvex.value = default_values);
const reset_flower_pts = () => (iteration_pts_flower.value = default_values);
```

```js
// VISUALIZATION

function return_two_convex_sets_plot(include_traces) {
  let convex_lines = [
    { x: -1 / 2, y: -1 / 4, set: 1, col: "#F994FF" },
    { x: 9 / 8, y: 9 / 16, set: 1, col: "#F994FF" },
    { x: -1 / 2, y: -1 / 16, set: 2, col: "#94FFF9" },
    { x: 9 / 8, y: 9 / 64, set: 2, col: "#94FFF9" },
  ];

  let projections = include_traces
    ? d3.merge(iteration_pts_convex.map((d) => [d[0], d[1]]))
    : [];
  let trace = iteration_pts_convex.map((d) => d[2]);

  return Plot.plot({
    x: { axis: false, domain: [-1 / 2, 9 / 8] },
    y: { axis: false, domain: [-1 / 4, 1 / 2] },
    aspectRatio: 1,
    style: { background: "none" },
    marks: [
      Plot.line(convex_lines, { x: "x", y: "y", z: "set", stroke: "col" }),
      Plot.line(trace, { stroke: "#FFF994" }),
      Plot.line(projections, { stroke: "gray", strokeDasharray: "4 4" }),
      Plot.dot(trace, {
        fill: "#FFF994",
        fillOpacity: 0.5,
        r: 10,
      }),
    ],
  });
}

function return_two_nonconvex_sets_plot(include_traces) {
  let non_convex_lines = [
    { x: -1 / 2, y: -1 / 4, set: 1, col: "#F994FF" },
    { x: 1 / 4, y: 1 / 8, set: 1, col: "#F994FF" },
    { x: 1 / 2, y: 1 / 4, set: 2, col: "#F994FF" },
    { x: 9 / 8, y: 9 / 16, set: 2, col: "#F994FF" },

    { x: -1 / 2, y: -1 / 16, set: 3, col: "#94FFF9" },
    { x: 1 / 4, y: 1 / 32, set: 3, col: "#94FFF9" },
    { x: 1 / 2, y: 1 / 16, set: 4, col: "#94FFF9" },
    { x: 9 / 8, y: 9 / 64, set: 4, col: "#94FFF9" },
  ];

  let projections = include_traces
    ? d3.merge(iteration_pts_nonconvex.map((d) => [d[0], d[1]]))
    : [];
  let trace = iteration_pts_nonconvex.map((d) => d[2]);

  return Plot.plot({
    x: { axis: false, domain: [-1 / 2, 9 / 8] },
    y: { axis: false, domain: [-1 / 4, 1 / 2] },
    aspectRatio: 1,
    style: { background: "none" },
    marks: [
      Plot.line(non_convex_lines, { x: "x", y: "y", z: "set", stroke: "col" }),
      Plot.line(trace, { stroke: "#FFF994" }),
      Plot.line(projections, { stroke: "gray", strokeDasharray: "4 4" }),
      Plot.dot(trace, {
        fill: "#FFF994",
        fillOpacity: 0.5,
        r: 10,
      }),
    ],
  });
}

function return_multiple_nonconvex_sets_plot(include_traces) {
  let non_convex_lines = [
    { x: -1 / 2, y: -1 / 4, set: 1, col: "#F994FF" },
    { x: 1 / 4, y: 1 / 8, set: 1, col: "#F994FF" },
    { x: 1 / 2, y: 1 / 4, set: 2, col: "#F994FF" },
    { x: 9 / 8, y: 9 / 16, set: 2, col: "#F994FF" },

    { x: -1 / 2, y: -1 / 16, set: 3, col: "#94FFF9" },
    { x: 1 / 4, y: 1 / 32, set: 3, col: "#94FFF9" },
    { x: 1 / 2, y: 1 / 16, set: 4, col: "#94FFF9" },
    { x: 9 / 8, y: 9 / 64, set: 4, col: "#94FFF9" },
  ];

  let flower = [...Array(flower_values.shape[0])].map((d, i) => ({
    x: flower_values.get(i, 0),
    y: flower_values.get(i, 1),
    set: 5,
    col: "#949AFF",
  }));

  let mean_points = iteration_pts_flower.map((d) =>
    d.reduce((a, b) => [a[0] + b[0], a[1] + b[1]]).map((m) => m / d.length),
  );

  let trace_red = include_traces ? iteration_pts_flower.map((d) => d[0]) : [];
  let trace_blue = include_traces ? iteration_pts_flower.map((d) => d[1]) : [];
  let trace_green = include_traces ? iteration_pts_flower.map((d) => d[2]) : [];

  return Plot.plot({
    x: { axis: false, domain: [-1 / 2, 9 / 8] },
    y: { axis: false, domain: [-1 / 4, 1 / 2] },
    aspectRatio: 1,
    style: { background: "none" },
    marks: [
      Plot.line([...non_convex_lines, ...flower], {
        x: "x",
        y: "y",
        z: "set",
        stroke: "col",
      }),
      Plot.line(mean_points, {
        stroke: "#FFF994",
      }),
      Plot.line(trace_red, {
        stroke: "#F994FF",
        strokeDasharray: "4 4",
      }),
      Plot.line(trace_blue, {
        stroke: "#94FFF9",
        strokeDasharray: "4 4",
      }),
      Plot.line(trace_green, {
        stroke: "#949AFF",
        strokeDasharray: "4 4",
      }),
      Plot.dot(mean_points, {
        fill: "#FFF994",
        fillOpacity: 0.5,
        r: 10,
      }),
    ],
  });
}

function return_plot(geometry, include_traces) {
  if (geometry == "Two Convex Sets") {
    return return_two_convex_sets_plot(include_traces);
  } else if (geometry == "Two Nonconvex Sets") {
    return return_two_nonconvex_sets_plot(include_traces);
  } else {
    return return_multiple_nonconvex_sets_plot(include_traces);
  }
}
```

# Proximal Gradient Methods

- Proximal gradient methods are a powerful technique to solve non-convex inverse problems
- Problem: find the intersection of multiple (non-convex) sets (e.g. points on geometric curves)
  - Catch: Only allowed to "operate" on one set at a time

```js
const projection_inputs_c = view(
  Inputs.form({
    geometry: Inputs.radio(
      ["Two Convex Sets", "Two Nonconvex Sets", "Multiple Nonconvex Sets"],
      {
        value: "Two Convex Sets",
      },
    ),

    iterate: Inputs.checkbox(["iterate", "reset", "traces"], {
      value: ["traces"],
    }),
  }),
);
```

```js
display(
  return_plot(
    projection_inputs_c.geometry,
    projection_inputs_c.iterate.includes("traces"),
  ),
);
```

```js
const projection_inputs_a = view(
  Inputs.form({
    projection_name: Inputs.radio(["AP", "DM", "RRR", "RAAR", "Generalized"], {
      value: "AP",
      label: "projection",
    }),

    projection_gamma: Inputs.range([0, 1], {
      value: 0.875,
      step: 0.001,
      label: "relaxation γ",
    }),
  }),
);
```

```js
const projection_inputs_b = view(
  Inputs.form({
    projection_a: Inputs.range([-1, 1], {
      value: `${
        projection_inputs_a.projection_name == "Generalized"
          ? 0
          : named_projection_parameters[projection_inputs_a.projection_name].a
      }`,
      step: 0.001,
      label: "parameter a",
    }),

    projection_b: Inputs.range([0, 2], {
      value: `${
        projection_inputs_a.projection_name == "Generalized"
          ? 1
          : named_projection_parameters[projection_inputs_a.projection_name].b
      }`,
      step: 0.001,
      label: "parameter b",
    }),

    projection_c: Inputs.range([0, 2], {
      value: `${
        projection_inputs_a.projection_name == "Generalized"
          ? 1
          : named_projection_parameters[projection_inputs_a.projection_name].c
      }`,
      step: 0.001,
      label: "parameter c",
    }),
  }),
);
```

```js
const j = (async function* () {
  if (projection_inputs_c.iterate.includes("iterate")) {
    for (let j = 0; true; ++j) {
      yield j;
      await new Promise((resolve) => setTimeout(resolve, 200));
      if (projection_inputs_c.geometry == "Two Convex Sets") {
        let l = iteration_pts_convex.length;
        append_convex_pts(two_convex_sets(iteration_pts_convex[l - 1][2]));
      } else if (projection_inputs_c.geometry == "Two Nonconvex Sets") {
        let l = iteration_pts_nonconvex.length;
        append_nonconvex_pts(
          two_nonconvex_sets(iteration_pts_nonconvex[l - 1][2]),
        );
      } else {
        let l = iteration_pts_flower.length;
        append_flower_pts(three_nonconvex_sets(iteration_pts_flower[l - 1]));
      }
    }
  }
})();
```

```js
{
  if (projection_inputs_c.iterate.includes("reset")) {
    if (projection_inputs_c.geometry == "Two Convex Sets") {
      reset_convex_pts();
    } else if (projection_inputs_c.geometry == "Two Nonconvex Sets") {
      reset_nonconvex_pts();
    } else {
      reset_flower_pts();
    }
  }
}
```
