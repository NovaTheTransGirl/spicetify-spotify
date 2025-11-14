# Spotify Downloader

![Spotify Downloader Banner](./assets/banner.png)  

**Spotify Downloader** is a custom Spotify client extension that allows you to download tracks directly from Spotify using a local server. This tool integrates with **Spicetify**, providing a seamless way to save music while maintaining the Spotify experience.

---

## Features

- Download individual tracks directly from Spotify.  
- Progress notifications with Unicode symbols:  
  - `✓ Download Started`  
  - `⟳ Download <percent>%`  
  - `↓ Download Complete`  
  - `✗ Download Failed`  
- Runs a local server using Python (`flask`) for handling downloads.  
- Automatic installation of required Python modules (`flask`, `requests`, `flask_cors`).  
- Adds a startup shortcut to run the downloader automatically.  
- Visual server status in Spotify’s top bar: `✔ Server running` / `✖ Server offline`.  

---

## Screenshots

**Spotify Downloader running**  

![Spotify Downloader](./assets/running.png)  

**Download notifications**  

![Download Notifications](./assets/notifications.png)  

**Server status in Spotify**  

![Server Status](./assets/server_status.png)  

---

## Installation

1. **Clone the repository**  

```bash
git clone https://github.com/yourusername/spotify-downloader.git
cd spotify-downloader
