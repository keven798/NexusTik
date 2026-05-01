---
name: "minimalist-ui-design"
description: "Designs minimalist UI interfaces with clean layouts, ample whitespace, and focused content presentation. Invoke when user requests minimalist, clean, or simple UI designs for dashboards and data visualization."
---

# Minimalist UI Design Skill

## Design Philosophy
- **Less is more**: Remove all unnecessary elements
- **Content first**: Let data speak for itself
- **Whitespace is active**: Use space to create hierarchy
- **Typography as UI**: Use font weights and sizes to guide attention

## Color Palette
```
Background: #FFFFFF (pure white) or #FAFAFA (off-white)
Surface: #FFFFFF
Primary Text: #1A1A1A (near black)
Secondary Text: #666666 (medium gray)
Tertiary Text: #999999 (light gray)
Accent: #0066FF (clean blue) or #000000 (black)
Border: #E5E5E5 (light gray)
Divider: #F0F0F0
Hover: #F5F5F5
```

## Typography
- **Font Family**: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif
- **Headings**: Bold, tight letter-spacing (-0.02em)
- **Body**: Regular, comfortable line-height (1.6)
- **Data/Numbers**: Tabular figures, monospace for alignment
- **Scale**:
  - H1: 32px/40px
  - H2: 24px/32px
  - H3: 18px/24px
  - Body: 14px/22px
  - Caption: 12px/18px
  - Data: 28px/36px (KPI numbers)

## Layout Principles
- **Grid**: 12-column, 24px gutter
- **Spacing Scale**: 4px base (4, 8, 12, 16, 24, 32, 48, 64)
- **Cards**: No border-radius or 4px max, 1px border
- **Shadows**: None or very subtle (0 1px 3px rgba(0,0,0,0.04))
- **Borders**: 1px solid #E5E5E5

## Component Styles

### KPI Cards
- White background, 1px border
- Large number (28px, bold)
- Small label (12px, gray)
- No shadow, no gradient
- Subtle hover: background #FAFAFA

### Tables
- No vertical borders
- Horizontal dividers only (1px #F0F0F0)
- Header: 12px uppercase, gray, letter-spacing 0.05em
- Row height: 48px
- Hover: #FAFAFA

### Charts
- Clean lines, no background grid
- Minimal axes
- Direct labels where possible
- Color: Single hue or max 2 colors

### Buttons
- Text only or outlined
- No radius or 4px
- Hover: underline or background shift
- Active: opacity 0.8

### Sidebar
- White or light gray background
- Simple text links
- Active: bold text or left border accent
- No icons or minimal icons

## Data Visualization
- **Line charts**: 2px stroke, no fill
- **Bar charts**: No border-radius, single color
- **Pie charts**: Donut style, minimal segments
- **Colors**: #0066FF, #00C853, #FF1744, #FFD600 (max 4)

## Interaction Design
- **Hover**: Subtle background change
- **Click**: Immediate feedback (opacity)
- **Loading**: Skeleton screens, no spinners
- **Transitions**: 150ms ease

## Anti-patterns to Avoid
- No gradients
- No shadows (except minimal)
- No border-radius > 4px
- No decorative elements
- No multiple colors
- No animation beyond opacity/position
