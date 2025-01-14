# Billboard Top Ten MOTD 🎵🎉

A Python-based script that dynamically scrapes the top 10 songs from the Billboard Hot 100 chart and sets it as the Message of the Day (MOTD) on your Linux system. 🎶✨ This is a fun and creative way to greet users logging into their terminal with the latest music hits. 🖥️🎧

## Features ✨
- Scrapes real-time Billboard Top 100 data. 🌐
- Displays the top 10 songs in a formatted MOTD. 📜
- Automatically updates on each terminal login. 🔄

## Prerequisites ⚙️
1. **Python 3.6 or later** 🐍
2. **Required Python Libraries**:
   - `requests` 📡
   - `beautifulsoup4` 🍲
3. A Linux-based system that supports dynamic MOTD (`/etc/update-motd.d`). 🐧

## Installation 🚀

### Step 1: Clone the Repository 📂
```bash
git clone https://github.com/but-i-am-dominator/billboard-motd.git
cd billboard-motd
```

### Step 2: Install Python Dependencies 🛠️
Install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Install Script 🏗️
Run the provided installation script to set up the MOTD:
```bash
chmod +x install_motd.sh
sudo ./install_motd.sh
```
This script will:
- Copy the `billboard_motd.py` script to `/usr/local/bin`. 📁
- Configure the MOTD system to run the script dynamically. ⚙️

### Step 4: Verify Installation ✅
Log out and log back into your terminal to see the Billboard Hot Ten displayed as your MOTD. 🎤

## Usage 📖
The MOTD will automatically update every time you log in. To manually test the script, you can run:
```bash
python3 billboard_motd.py
```

## Uninstallation ❌
To remove the Billboard Hot Ten MOTD:
1. Delete the MOTD script from `/usr/local/bin`:
   ```bash
   sudo rm /usr/local/bin/billboard_motd.py
   ```
2. Remove the dynamic MOTD configuration:
   ```bash
   sudo rm /etc/update-motd.d/10-billboard
   ```

## Troubleshooting 🛠️
- **Issue: MOTD does not display as expected**:
  - Ensure your Linux distribution supports dynamic MOTD (`/etc/update-motd.d`). 🐧
  - Verify that Python 3 and the required libraries are installed. ✅
- **Issue: Script fails to scrape Billboard data**:
  - The Billboard website structure may have changed. Update the scraping logic in `billboard_motd.py` as needed. 📝

## Contributing 🤝
Contributions are welcome! Feel free to fork this repository, make improvements, and submit a pull request. 💻✨

## License 📜
This project is licensed under the MIT License. See the `LICENSE` file for more details. 🖊️

## Acknowledgments 🙌
- Billboard Hot 100: [billboard.com](https://www.billboard.com) 🎵
- Python Libraries: `requests`, `beautifulsoup4` 🐍🍲

---

Get ready to log in and rock out—your terminal is charting new territory with the Billboard Hot Ten! 🎸🎤