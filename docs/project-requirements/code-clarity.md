# Code clarity

Choose the simplest implementation that meets the requirement and makes the
behavior easy for another developer to trace. Keep the domain rules visible,
especially when manipulating or analyzing football data.

- Use domain names that identify what a value represents. For calculations,
  make units, denominators, and time windows explicit where they matter.
- Keep filtering, joining, normalization, aggregation, and scoring steps
  readable in the order they run. Name intermediate results when the names
  help explain the calculation.
- Prefer straightforward control flow. Extract a helper when it gives a
  meaningful operation a name, improves reuse, or makes the caller easier to
  follow. Keep abstractions grounded in current requirements.
- Make assumptions and edge-case handling explicit where they affect results,
  such as missing data, duplicate records, empty groups, or zero denominators.
  Use comments to explain domain decisions that the code alone cannot convey.
- When a requirement or a measured performance need calls for a more complex
  implementation, explain the reason and how the logic was verified in the
  [change record](change-template.md).
