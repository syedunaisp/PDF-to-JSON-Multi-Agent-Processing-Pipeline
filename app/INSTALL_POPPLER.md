# Install Poppler on Windows (Manual Method)

## Step-by-Step Instructions

### 1. Download Poppler

Download the latest release from:
https://github.com/oschwartz10612/poppler-windows/releases/latest

Look for a file named: `Release-XX.XX.X-X.zip` (e.g., `Release-24.08.0-0.zip`)

### 2. Extract the ZIP

- Extract the downloaded ZIP file
- You'll see a folder structure like: `poppler-XX.XX.X/Library/bin/`

### 3. Move to Program Files

- Move the extracted `poppler-XX.XX.X` folder to `C:\Program Files\`
- Rename it to just `poppler` for simplicity
- Final path should be: `C:\Program Files\poppler\Library\bin\`

### 4. Add to PATH

**Option A: Using GUI**
1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find and select "Path"
5. Click "Edit"
6. Click "New"
7. Add: `C:\Program Files\poppler\Library\bin`
8. Click "OK" on all dialogs

**Option B: Using PowerShell (Run as Administrator)**
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\poppler\Library\bin", "Machine")
```

### 5. Verify Installation

Close and reopen your terminal, then run:
```bash
pdftoppm -v
```

You should see version information.

### 6. Test the API

Once Poppler is installed, upload your PDF at:
http://127.0.0.1:8000/docs

Click on `/pdf-to-markdown` endpoint and upload your JEE question bank PDF.

---

## Quick Alternative: Use Python Script Instead

If you don't want to install Poppler system-wide, I can create a simpler script that uses a different method.
