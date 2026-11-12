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
