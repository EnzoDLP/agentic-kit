# MUI Joy

## Content appearing inside a centered modal

- `ModalDialog` is vertically centered: any block that appears or changes height (validation
  alert, error message) grows the modal and moves **all** its content, including the thumb of a
  `Slider` being dragged, which slips away from the pointer.
- Reserve the space: always render the block at a **fixed height** (`height`, not `minHeight`, or
  a longer message changes it again), with a neutral or success state when all is well. A button
  only used in the error state stays rendered with `visibility: hidden` (plus `tabIndex={-1}`,
  `aria-hidden`) to keep its place.

## `Select` inside a clickable row

- A `Select`'s options render in a portal, but React events bubble up the **component** tree: a
  click on an option fires the `onClick` of the table row holding the `Select` (e.g. expanding the
  row). Put `onClick={(e) => e.stopPropagation()}` on a wrapper around the `Select`; a
  `stopPropagation` on the `Select` alone does not cover the options.
- A clickable row (`onClick` on `tr`) ignores clicks coming from a link or button in the row
  (`closest('a, button, …')`) **and** from a portal (`!event.currentTarget.contains(target)`),
  otherwise a `Select` or menu option opens the row.

## Menu of a colored `Select`

- The listbox and the `Option`s inherit `variant` / `color` from the `Select`: a `soft success`
  trigger gives an all-green menu. For a colored trigger and a white menu:
  `slotProps={{ listbox: { variant: 'outlined', color: 'neutral' } }}` on the `Select`, and
  `variant="plain"` on each `Option` (a per-option `color` then only colors its text).

## Container query in `sx`

- A layout that must follow the actual available width (sidebar collapsed or not) rather than the
  screen: `containerType: 'inline-size'` + `containerName` on a parent, then the key
  `` [`@container ${name} (min-width: 640px)`]: { … } `` in the descendants' `sx` (Emotion passes
  it through). Joy has no breakpoint for this.
- An element **cannot query its own size**: a `@container` rule set on the container itself never
  applies. The container is an outer box; the flex rules go on a child.

## `body-sm` / `body-xs` are gray by default

- Joy colors `body-sm` and `body-xs` with `text.tertiary` unasked (only `body-md`, `title-*` and
  `h*` use `text.primary`). A `body-xs` label and a `body-sm` value therefore come out in the same
  gray and blur together. Give the value an explicit `textColor="text.primary"` (and an `md`
  weight); the label stays `text.tertiary`, uppercase if the page already uses it.

## Grid list inside a bounded scroll area

- **The rows of a CSS grid collapse to a couple of pixels instead of scrolling.** In a grid with
  a bounded height (flex child with `minHeight: 0`, `overflowY: 'auto'`), items that clip their
  overflow (`Typography noWrap` sets `overflow: hidden`) get an automatic minimum size of 0, so
  the `auto` rows shrink to fit the container and the text disappears. Give the rows their content
  height: `gridAutoRows: 'max-content'`. Checked in Chromium through a Storybook browser test
  (row height 2px before, one text line after).

## Dialog parts inside a `Drawer`

- **A `DialogTitle` in a padded `Drawer` sits further right than the fields under it** (Joy
  5.0.0-beta.52): `Drawer` gives a direct `DialogTitle` child `--unstable_DialogTitle-margin:
  var(--Drawer-titleMargin)` (0.75rem at the default size), added to the content's own padding.
  Set `'--Drawer-titleMargin': '0px'` in the `content` slot's `sx` when the content is padded.
- **The drawer's buttons are hand-placed instead of Joy's dialog actions**: use `DialogActions`
  (`row-reverse`: the primary action written first shows on the right, as in a `ModalDialog`).
  Inside a `Drawer` it has no gap between buttons: add `sx={{ gap: 1 }}`.

## Scrollable table frame

- **The page stops scrolling while the pointer is over a table** with its own scroll
  (`maxHeight` + `overflow: auto` on the `Sheet` around a sticky-header `Table`): an
  `overscrollBehavior: 'none'` on that frame blocks scroll chaining, so at the table's top or
  bottom the wheel no longer reaches the page. Leave the default (`auto`); a story can check
  `getComputedStyle(frame).overscrollBehaviorY === 'auto'`.
