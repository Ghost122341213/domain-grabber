# Domain Grabber

A Python script to retrieve a list of **root domains** based on specific extensions (`.id`, `.co.id`, `.ac.id`, etc.) from the **Archive.org CDX API**.

[Readme_ID.md](https://github.com/bimantaraz/domain-grabber/blob/main/README.md)
## ✨ Features

* Fetch domain lists from [web.archive.org CDX API](https://archive.org/help/wayback_api.php).
* Supports multiple extensions at once (comma-separated).
* Configurable target number of root domains per extension.
* Automatically rotates User-Agent to avoid rate limits.
* Interactive, colorful CLI using **Rich**.
* Automatically saves results to `.txt` files with timestamps.

## 📦 Installation

Make sure Python **3.8+** is installed.

1. Clone this repository:

   ```bash
   git clone https://github.com/bimantaraz/domain-grabber.git
   cd domain-grabber
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run:

```bash
python grabber.py
```

Example input:

```
Extensions: id, co.id, ac.id
Number of root domains per extension: 50
Cautious mode (add small delay)? [Y/n]: y
```

The output will be saved as:

```
grab_id_20250812_153045.txt
grab_co.id_20250812_153045.txt
grab_ac.id_20250812_153045.txt
```

## 📄 Example Output File

```
abc.ac.id
def.ac.id
example.co.id
universitas.ac.id
```

### **📄 requirements.txt**

```
requests>=2.31.0
rich>=13.7.1
urllib3>=2.2.2
```

## ⚠ Notes

* Use specific extensions (`co.id`, `ac.id`, `go.id`) to reduce the risk of rate-limiting.
* If you encounter **403** or **429**, try again after a few minutes or lower the target number.
* Archive.org CDX API does not always return complete results, so output may vary between runs.
