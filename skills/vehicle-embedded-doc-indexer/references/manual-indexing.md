# Manual Indexing

Large chip manuals must be indexed hierarchically. Do not read them end-to-end on first pass.

Run `scripts/index_sources.py <project-root> <manual-file-or-folder>` first so every manual has a non-empty metadata/outline placeholder. Then deepen only the relevant manuals.

## First Pass Order

1. Extract PDF bookmarks if available.
2. Read title, revision, device family, package scope, and introductory pages.
3. Read table of contents pages.
4. Build an outline tree with chapter titles, levels, page ranges, and keywords.
5. Mark high-value entry points for future queries.

## High-Value Entry Points

Always try to identify:

- Device overview.
- Pin description and package/ball map.
- Port function and alternate function tables.
- Clock generation and clock tree.
- Reset and low-power modes.
- Interrupt controller.
- Memory map.
- Register notation conventions.
- GPIO/PORT.
- ADC.
- PWM/timer.
- SPI/CSI/DSPI.
- CAN/CAN FD.
- LIN/UART.
- Ethernet.
- Watchdog.
- Safety/security modules.
- Electrical characteristics.
- Errata/workarounds if included or linked.

## Section Entries

Use this shape:

```yaml
- section_id: can-fd
  title: "CAN FD Controller"
  level: 1
  pdf_page_start: 3201
  pdf_page_end: 3440
  keywords: [can, canfd, mailbox, baud rate, interrupt]
  inspected: false
```

Set `inspected: true` only after reading that section in detail.

## Beginner Notes

Keep beginner explanations out of first-pass indexes unless they help disambiguate terminology. The curator skill can add short explanations while answering.
