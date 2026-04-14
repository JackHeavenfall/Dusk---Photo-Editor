# Installation and Running

## Prerequisites

- Python 3.10 or newer
- pip (Python package manager)

## Step 1: Create the Project Structure

Place all Python files in the exact directory tree described in `01_overview.md`. The root folder must contain `main.py` and the `components/` subdirectory.

## Step 2: Install Dependencies

Open a terminal in the project root and run:

```bash
pip install Pillow numpy

```

### Optional (for drag‑and‑drop on macOS/Linux):

#### macOS
```bash
brew install tkdnd

```

#### Linux (Ubuntu/Debian)
```bash
sudo apt install tkdnd

```

## Step 3: Run the Application

### Windows (no console window)
```bash
pythonw main.py

```

### macOS / Linux
```bash
python3 main.py

```

## First Launch Checklist

- The main window appears (1320×840, minimum 1000×660).
- Left panel shows three import buttons and a drop zone.
- Right panel shows adjustment sliders.
- Bottom status bar says "ready — use the buttons on the left to add images".

## Testing Basic Functionality

- Add one image (file, folder, or drag‑and‑drop).
- A thumbnail appears in the queue; click it to load into preview.
- Move any slider – the preview updates after 200 ms.
- Switch between before/split/after modes.
- Click "export all" – the export dialog opens, process the single image.
- Check the output folder (default: ~/Pictures/dusk_output).

## Running from Source (with console)
For debugging, run with python main.py (instead of pythonw). The console will show log messages and any unhandled exceptions.

## Building a Standalone Executable (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name Dusk main.py

```
The executable will be in the dist/ folder. Copy it to any location; it does not need Python installed.

