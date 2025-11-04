# ⚡ Blink Fetch Download Manager

<div align="center">

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**A lightning-fast, multi-threaded download manager with a beautiful modern GUI** ✨

*Download faster. Download smarter. Download with style.* 🚀

</div>

---

## 🌟 Features

### ⚡ **Lightning Fast**
- Multi-threaded downloads split files into chunks for maximum speed
- Efficient bandwidth management and optimization
- Real-time progress tracking with smooth UI updates

### 🎨 **Beautiful Interface**
- Modern dark-themed GUI built with CustomTkinter
- Smooth animations and hover effects
- Clean, intuitive single-panel design
- Color-coded status indicators

### 🧠 **Smart Detection**
- **Auto-detects** filename from URLs and Content-Disposition headers
- **Auto-detects** file size before downloading
- **Auto-categorizes** files by type (Documents, Videos, Music, Code, etc.)
- Supports RFC 2047 encoded filenames

### 📁 **Intelligent Organization**
- Automatic file categorization into folders:
  - 🗜️ Compressed files (.zip, .rar, .7z, etc.)
  - 🖼️ Pictures (.jpg, .png, .gif, etc.)
  - 🎬 Videos (.mp4, .mkv, .avi, etc.)
  - 🎵 Music (.mp3, .wav, .flac, etc.)
  - 📄 Documents (.pdf, .docx, .txt, etc.)
  - ⚙️ Executables (.exe, .msi, .apk, etc.)
  - 💻 Code (.py, .js, .html, etc.)
  - 📦 Others (everything else)

### 🛠️ **User Control**
- Customizable download location
- Optional category-based organization
- Manual filename editing before download
- Browse and select custom folders
- Default path remembers your preferences

### 🔒 **Robust & Reliable**
- Comprehensive error handling with user-friendly messages
- Supports HTTP redirects and various header formats
- Thread-safe concurrent downloads
- Validates URLs and file paths

---

## 📸 Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────┐
│  Add Download                               ✨  │
│  ┌──────────────────────────────────────────┐  │
│  │ Paste download URL here...               │  │
│  └──────────────────────────────────────────┘  │
│  ☑ Use Category  🗜️ Compressed  📏 164 GB    │
│  Save to: C:\Downloads\Compressed            │
│  Filename: flutter_windows_3.35.2-stable.zip │
│           [  Download  ]                      │
│  Progress: ████████████░░░░ 75%              │
│  Status: Downloading... 75% ✓                │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- Windows OS (primary support)

### Installation

1. **Clone the repository**
```powershell
git clone https://github.com/udaygiri/Blink-Fetch-Download-Manager.git
cd Blink-Fetch-Download-Manager
```

2. **Install dependencies**
```powershell
pip install -r requirements.txt
```

Or with UV package manager:
```powershell
uv pip install -r requirements.txt
```

3. **Run the application**
```powershell
python -m gui.app
```

Or run the main entry point:
```powershell
python main.py
```

---

## 💻 Usage

### GUI Mode (Recommended)

1. **Launch the application**
   ```powershell
   python -m gui.app
   ```

2. **Paste your download URL**
   - The app automatically detects the filename and file size
   - Category is auto-selected based on file type

3. **Customize settings** (optional)
   - Toggle "Use Category" to organize by file type
   - Change the save location using "Browse"
   - Edit the filename if needed

4. **Click "Download"**
   - Watch the progress bar fill up
   - Get notified when download completes

### CLI Mode

```python
from function.Downloads import download_file

# Simple download
download_file("https://example.com/file.zip")

# Custom settings
download_file(
    url="https://example.com/file.zip",
    num_threads=8,
    filepath="C:/Downloads/myfile.zip"
)
```

---

## 📂 Project Structure

```
Blink Fetch Download Manager/
│
├── 📁 gui/
│   ├── app.py                 # Main GUI application
│   └── download_backend.py    # Threading bridge for downloads
│
├── 📁 function/
│   ├── Downloads.py           # Core download logic with multi-threading
│   └── File_path.py           # File categorization and path handling
│
├── 📁 Downloads/              # Default download directory
│   ├── 🗜️ Compressed/
│   ├── 🖼️ Pictures/
│   ├── 🎬 Videos/
│   ├── 🎵 Music/
│   ├── 📄 Documents/
│   ├── ⚙️ Executables/
│   ├── 💻 Code/
│   └── 📦 Others/
│
├── main.py                    # Entry point
├── pyproject.toml             # Project metadata
└── README.md                  # You are here! 📍
```

---

## 🎯 Key Technologies

| Technology | Purpose |
|-----------|---------|
| **Python 3.13+** | Core language |
| **CustomTkinter** | Modern GUI framework |
| **Requests** | HTTP operations |
| **Threading** | Multi-threaded downloads |
| **TQDM** | Progress bars for CLI |
| **Re (Regex)** | Header parsing |

---

## 🔧 Configuration

### Default Download Path
The app remembers your last selected folder. First time default: `./Downloads/`

### Number of Threads
Default: 4 threads per download. Can be customized in code:
```python
download_file(url, num_threads=8)
```

### Category Mappings
Edit `function/File_path.py` to customize file type categories and extensions.

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'gui'"
**Solution:** Run from project root using `python -m gui.app`

### Issue: Filename contains invalid characters
**Solution:** The app automatically decodes RFC 2047 encoded filenames. If issues persist, manually edit the filename field.

### Issue: Download fails with network error
**Solution:** 
- Check your internet connection
- Verify the URL is a direct download link
- Some sites require authentication or cookies

### Issue: Progress bar not updating
**Solution:** The GUI updates every chunk. For very fast downloads, updates may appear instant.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. ✍️ Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 Open a Pull Request

### Ideas for Contributions
- 🔄 Pause/Resume functionality
- 📊 Download history and statistics
- 🌐 Browser extension integration
- 🎨 Theme customization options
- 📱 Mobile companion app
- 🔗 Batch download support

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ using Python
- GUI powered by [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Icon support from emoji standards

---

## 📞 Contact & Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/udaygiri/Blink-Fetch-Download-Manager/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/udaygiri/Blink-Fetch-Download-Manager/discussions)
- ⭐ **Star this repo** if you find it useful!

---

<div align="center">

### Made with ⚡ by the Blink Fetch Team

**Download at the speed of light!** 🚀

[⬆ Back to Top](#-blink-fetch-download-manager)

</div>
