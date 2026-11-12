# React web — generated API code

Applies when the project generates its API client from an OpenAPI spec (`openapi-ts`) into
`src/generated/**`.

## Never modify

- Never edit a file under `src/generated/`.
- Never transform or extend the types defined there.

These files are generated from the OpenAPI spec (e.g. `swagger.yml`) and are overwritten on the
next codegen run.

## To change the API surface

1. Edit the spec.
2. Regenerate with the project's codegen script (e.g. `npm run openapi-ts`).

## Using generated types

- Always use the types from `src/generated/api-client/types.gen.ts` for API interactions; never
  hand-roll parallel types.
- When the UI needs a simplified shape:
  - define the UI-facing type in `src/types/`;
  - write a pure mapper in `src/utils/mappers/` from the generated API type to the UI type;
  - a mapping used by a single hook stays internal to that hook instead of moving to
    `src/utils/mappers/`.
