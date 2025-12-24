# Random Matching Tool (GUI)

A simple, general-purpose random matching and pairing tool with a graphical user interface.

## Overview

This application provides an easy way to create random matches or assignments for various scenarios:

- 👥 Team pairing
- 🎯 Participant matching
- 📋 Random assignments
- 🎓 Classroom, event, or workshop grouping
- ✨ Any situation that requires fair and random matches

The application is built with Python and Tkinter and is provided as both source code and a standalone Windows executable (.exe).

## Features

- ✅ **Graphical User Interface (GUI)** – no terminal required
- 📂 Load names from any `.txt` file (one name per line)
- 🤖 **Automatic mode:**
  - Even number of names → pair matching
  - Odd number of names → one-to-one assignments
- ⚙️ **Manual modes:**
  - `pairs` (even number of names required)
  - `assignments` (no one is matched with themselves)
- ⏱️ Adjustable delay between results
- 💾 Save results to a `.txt` file
- 🚫 Prevents self-matching
- ⚠️ Prevents duplicate names

## Repository Structure

```
RandomMatching/
├── match_gui.py              # Source code (GUI application)
├── dist/
│   └── RandomMatching.exe    # Standalone Windows executable
├── names.txt                 # Example file (even number of names)
├── names2.txt                # Example file (odd number of names)
└── README.md                 # This file
```

## Example Input Files

This repository includes two example name lists:

- **`names.txt`**  
  Contains an even number of participants.  
  Demonstrates pair matching.

- **`names2.txt`**  
  Contains an odd number of participants.  
  Demonstrates one-to-one assignments.

## Input Format

Create a text file with one name per line (full name recommended):

```
Ahmet Yılmaz
Ayşe Demir
Mehmet Kaya
Zeynep Şahin
Ali Çelik
```

### Rules:
- At least **2 names** are required
- Names must be **unique**
- Empty lines are ignored

## How to Run

### Option 1: Run from source (Python required)

**Requirements:**
- Python 3.x

**Steps:**
1. Open the project folder
2. Run the following command:
   ```bash
   python match_gui.py
   ```
3. Click **"Browse"** and select a `.txt` file
4. Choose a mode (`auto`, `pairs`, or `assignments`)
5. Click **"Run"**

### Option 2: Run standalone EXE (no Python required)

1. Open the `dist` folder
2. Double-click `RandomMatching.exe`
3. Select a `.txt` file and start matching

> **Note:**  
> Windows SmartScreen may show an "unknown publisher" warning.  
> Click **"More info"** → **"Run anyway"** to continue.

## Matching Logic

### Pair matching (even number of names):
```
Ahmet Yılmaz <-> Ayşe Demir
Mehmet Kaya <-> Zeynep Şahin
```

### Assignments (odd number of names or manual mode):
```
Ahmet Yılmaz → Mehmet Kaya
Ayşe Demir   → Zeynep Şahin
Mehmet Kaya  → Ali Çelik
```

### Guarantees:
- ✅ No participant is matched with themselves
- ✅ Each participant appears exactly once per run

## Built With

- 🐍 Python 3
- 🖼️ Tkinter (standard Python GUI library)
- 📦 PyInstaller (for packaging the `.exe`)

## License

This project is provided for educational and general-purpose use.  
You are free to use, modify, and share it.

## Author

**Created by Emrehan Çetin**

---

### Quick Start

1. Download or clone this repository
2. Run `RandomMatching.exe` from the `dist` folder (Windows)
3. Or run `python match_gui.py` if you have Python installed
4. Load your `.txt` file with participant names
5. Click "Run" and watch the magic happen! ✨

---

**Need help?** Feel free to open an issue or contact the author.
