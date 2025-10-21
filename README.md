# website
Website source code (https://mattcompton.dev)

## Theme configuration

The site now supports multiple color themes. Visitors can toggle themes from the header; the selection is stored in the browser so the preference persists between visits.

To change the default theme when building the site, set the `PUBLIC_DEFAULT_THEME` environment variable to one of:

- `terminal`
- `halloween`
- `holiday`
- `pain`

For example:

```bash
PUBLIC_DEFAULT_THEME=holiday npm run build
```

If the provided value is not recognized, the build falls back to the `terminal` theme.

> Note: the theme selector is intentionally hidden beneath the `sys/online` status indicator—click it to reveal the options.

Running `make build` or `make dev` automatically chooses a seasonal theme:

- March 31 – April 1: `pain`
- October: `halloween`
- November & December: `holiday`
- Otherwise the default theme is used.

Each theme can use an optional tiled background; see the `--bg-tile-image` variables in `src/styles/global.css` if you want to swap in your own bitmaps.
