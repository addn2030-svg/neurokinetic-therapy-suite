# VS Code Quick Start & Installation Guide for NKT® Suite

This guide walks you step-by-step through installing, running, and using the **NeuroKinetic Therapy (NKT®) Master Clinical Suite** inside **Visual Studio Code (VS Code)**.

---

## 🛠️ Step 1: Open or Clone in VS Code

### Method A: If You Cloned from GitHub
1. Open VS Code.
2. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on Mac) to open the Command Palette.
3. Type `Git: Clone` and paste your GitHub repository URL:
   ```bash
   https://github.com/YOUR_USERNAME/neurokinetic-therapy-suite.git
   ```
4. Select a local folder to clone into, then click **Open Repository**.

### Method B: If You Downloaded the ZIP / Project Folder
1. Extract the folder on your computer.
2. Open VS Code.
3. Go to **File > Open Folder...** (or `Ctrl + K Ctrl + O` / `Cmd + O` on Mac) and select the `neurokinetic-therapy-suite` folder.

---

## 🔌 Step 2: Install Recommended VS Code Extensions

When you open this folder, VS Code will prompt you: *"This repository has recommended extensions."* Click **Install All**.

If you want to install them manually:
1. Open the **Extensions** tab (`Ctrl + Shift + X` or `Cmd + Shift + X`).
2. Search and install:
   * **Live Server** (by *Ritwick Dey*) — One-click local live reloading server for the HTML interactive modules.
   * **Live Preview** (by *Microsoft*) — View the HTML tools inside an embedded VS Code tab.
   * **Markdown All in One** (by *Yu Zhang*) — Rich preview for `SKILL.md` and `README.md`.

---

## 🚀 Step 3: Run & View the Interactive Suite in 1 Click

### Option 1: Using Live Server (Browser View)
1. In the VS Code File Explorer (left sidebar), **right-click `index.html`**.
2. Select **"Open with Live Server"**.
3. Your default browser will automatically launch at `http://127.0.0.1:5500/index.html`.
4. You can now navigate through all 5 interactive modules, test your knowledge with the 10 MSQs, view the visual atlas, and review practical protocols.

### Option 2: Using Microsoft Live Preview (Embedded inside VS Code)
1. Right-click `index.html`.
2. Select **"Show Preview"**.
3. The complete interactive suite will render directly in an editor pane next to your code!

---

## 🤖 Step 4: How to Use `SKILL.md` in VS Code AI Assistants

The `SKILL.md` file contains the standardized clinical reasoning instructions for NKT. You can load it into any AI extension in VS Code:

### 1. With GitHub Copilot
* In VS Code, open the Copilot Chat window (`Ctrl + Alt + I` or `Cmd + Alt + I`).
* Reference the skill file in your prompt:
  ```text
  @workspace #file:SKILL.md Given a patient with right IT band pain and a weak glute medius, what is the NKT diagnostic protocol?
  ```

### 2. With Cline / Roo-Code / Cursor / Windsurf / Claude Dev
* Copy the contents of `SKILL.md` into your custom system instructions or `.cursorrules` / `.clinerules` file.
* The AI will act as an NKT Master Clinical Specialist, validating reactive pairs, MMT vectors, and corrective sequences.

---

## 🔄 Step 5: Sync & Push Changes to GitHub from VS Code

1. Click the **Source Control** icon in the left activity bar (`Ctrl + Shift + G`).
2. Type your commit message in the text box (e.g., `update clinical protocols`).
3. Click **Commit**, then click **Sync Changes** (or **Publish Branch**).
