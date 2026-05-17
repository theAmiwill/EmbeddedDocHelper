# Schematic Indexing

Index schematics for later engineering location, not for aesthetic summary.

## First Pass

For each page/sheet, capture:

- PDF page number.
- Printed drawing sheet number if visible.
- Sheet title.
- Major modules.
- Main ICs and connectors.
- Key nets.
- Power rails.
- Clock/reset signals.
- Communication buses.
- MCU pins when visible.
- Test points and debug connectors.

## Important Embedded Signals

Prioritize these because they affect BSW, driver, board bring-up, or MCAL work:

- Power rails: VBAT, VCC, VDD, 5V, 3V3, core supplies, analog supplies.
- Resets: POR, nRESET, watchdog reset, transceiver standby/reset.
- Clocks: crystal, oscillator, PLL inputs, external clock pins.
- Buses: CAN, LIN, SPI, I2C, UART, Ethernet, FlexRay.
- Analog: ADC inputs, sensor supplies, references, filters.
- Actuation: PWM outputs, high-side/low-side drivers, motor drivers.
- Safety/debug: JTAG, SWD, trace, boot mode pins, test points.

## Evidence

Always keep both PDF page and printed sheet ID when possible:

```yaml
evidence:
  - file: docs/main_board.pdf
    pdf_page: 12
    drawing_sheet: "12/42"
```

## Limits

Do not infer software configuration directly from a schematic alone. A schematic can show connectivity, but MCAL/BSW impact also needs pin mux, clock/reset, peripheral, interrupt, and sometimes electrical characteristics evidence.
