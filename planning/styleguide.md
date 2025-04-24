# 🎨 Procrastinatircs Styling Guide

A comprehensive style guide for maintaining design consistency across all views and components of the **Procrastinatircs** web application.

---

## Color Palette

| Role                    | Color Name           | HEX Code   | Notes                            |
|-------------------------|----------------------|------------|----------------------------------|
| Primary Background      | Charcoal Black       | #1B1B1B   | Main background color            |
| Secondary Background    | Gray-Black           | #292929   | Used in cards/forms              |
| Accent 1                | Mint Green           | #D9FFE7   | Used in login/log views          |
| Accent 2                | Pastel Pink          | #FFD6DA   | Used in signup view              |
| Accent 3                | Soft Yellow          | #FFF2C5   | Used in receipts/share page      |
| Accent 4                | Aqua Teal            | #7FFFD4   | Toggles and highlights           |
| Text Primary            | White                | #FAFAFA   | Default text color               |
| Text Secondary          | Light Gray           | #BFBFBF   | Muted/placeholder text           |
| Borders/Dividers        | Dark Gray            | #2E2E2E   | Border and section lines         |

---

## Typography

| Element         | Font      | Size     | Weight  | Notes               |
|-----------------|-----------|----------|---------|---------------------|
| Headings (H1–H3)| Poppins   | 24–32px  | 600–700 | Upper or lowercase  |
| Body Text       | Inter     | 14–16px  | 400–500 | Standard UI text    |
| Labels/Inputs   | Inter     | 12–14px  | 500     | All caps optional   |
| Navigation      | Inter     | 16px     | 600     | Bold + high contrast|
| Mood Emojis     | System    | 16–20px  | N/A     | Center-aligned      |

for future ones we would use it like this 

<head>
  <!-- Google Fonts: Poppins -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/global.css') }}">
</head>

---

## Layout & Spacing

| Property             | Value               |
|----------------------|---------------------|
| Grid system          | 12-column / Flexbox |
| Section padding      | 24–40px             |
| Card/form padding    | 16–24px             |
| Element margin       | 20px                |
| Border-radius        | 8px (standard)      |
| Button height        | 40–48px             |

---

## Components

### Buttons

- Primary: Mint or Pink background, bold text
- Secondary: Transparent with colored border
- Disabled: Lower opacity, no hover effects
- Transitions: 0.2s ease on hover

### Cards / Panels
Used for dashboard boxes, share receipts, profile panels

.card {
  background-color: #FFD6DA;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

## External Libraries Used

- [Chart.js](https://www.chartjs.org/) — used to display visual graphs and stats in the dashboard view



/* global.css */
for when we have global ones 
body {
  font-family: 'Poppins', sans-serif;
  font-weight: 400;
  background-color: #1B1B1B;
  color: #FAFAFA;
  margin: 0;
  padding: 0;
}

idk if bootstrap would be very effective for this project as there are repeated times where we would have to override it. Might do for some buttons or grid layouts but in the end not entirely sure if it would be the most effective.