# Refactor Code Duplication in Tab Rendering Logic

## Completed Tasks
- [x] Analyzed the code duplication in app.py tabs 1, 2, and 3
- [x] Created a `render_tab` function to handle common rendering logic
- [x] Refactored tab1 (Main Stats) to use `render_tab`
- [x] Refactored tab2 (Languages) to use `render_tab`
- [x] Refactored tab3 (Contributions) to use `render_tab`

## Testing
- [x] Attempted to run the Streamlit app (streamlit not installed in environment)

## Summary
The code duplication has been eliminated by introducing a reusable `render_tab` function that handles:
- Column setup (col1, col2)
- SVG rendering and base64 encoding
- URL parameter construction
- Code area display

This follows the DRY principle and makes the code more maintainable.
