(function init() {
    const wait = (selector, timeout = 10000) =>
        new Promise((resolve, reject) => {
            const start = Date.now();
            const check = () => {
                const el = document.querySelector(selector);
                if (el) return resolve(el);
                if (Date.now() - start >= timeout) return reject("Timeout");
                requestAnimationFrame(check);
            };
            check();
        });

    wait(".Root__main-view").then(() => {
        console.log("Initializing Spotify Downloader v1.0");
        console.log("Loaded Spotify Downloader Extension");

        let serverIcon;

        const addServerIcon = () => {
            const topBar = document.querySelector(".Root__now-playing-bar");
            if (!topBar) return;

            serverIcon = document.createElement("span");
            serverIcon.style.margin = "0 10px";
            serverIcon.style.fontWeight = "bold";
            serverIcon.textContent = "✖ Download Server offline";
            topBar.appendChild(serverIcon);
        };

        const updateServerIcon = (running) => {
            if (!serverIcon) return;
            serverIcon.textContent = running ? "✔ Download Server running" : "✖ Download Server offline";
        };


        addServerIcon();

        const pingServer = async () => {
            try {
                const controller = new AbortController();
                setTimeout(() => controller.abort(), 2000);
                const res = await fetch("http://localhost:8080/status", { signal: controller.signal });
                updateServerIcon(res.ok);
                return await res.json();
            } catch {
                updateServerIcon(false);
                return null;
            }
        };

        pingServer();
        setInterval(pingServer, 10000);

        const isTrack = (uris) => {
            if (!uris || uris.length === 0) return false;
            const obj = Spicetify.URI.fromString(uris[0]);
            return obj.type === Spicetify.URI.Type.TRACK;
        };

        const activeNotifs = {};

        const showNotification = (id, message) => {
            Spicetify.showNotification(message)
        };

        const downloadTrack = async (uris) => {
            if (!uris || uris.length === 0) return;

            const trackUri = uris[0];
            let title = "Unknown";
            let artists = "Unknown";

            try {
                const id = trackUri.split(":")[2];
                const trackData = await Spicetify.CosmosAsync.get(`https://api.spotify.com/v1/tracks/${id}`);
                title = trackData.name;
                artists = trackData.artists.map(a => a.name).join(", ");
            } catch {}

            const url = `https://open.spotify.com/track/${trackUri.split(":")[2]}`;
            const status = await pingServer();
            if (!status) {
                showNotification(trackUri, "✗ Download Failed (Server offline)");
                return;
            }

            // Start download
            await fetch(`http://localhost:8080/download?uri=${encodeURIComponent(url)}`);
            const notifId = trackUri;
            let lastStage = "";
            let lastProgress = -1;

            showNotification(notifId, `✓ Download Started: ${title} - ${artists}`);

            const interval = setInterval(async () => {
                const s = await pingServer();
                const downloads = s?.downloads ?? {};
                const outputs = s?.output_paths ?? {};

                if (!(url in downloads)) {
                    // Download complete
                    clearInterval(interval);
                    showNotification(notifId, `↓ Download Complete: ${title} - ${artists}\nFolder: ${outputs[url] || "Unknown"}`);
                    return;
                }

                const prog = downloads[url];

                let stage = "";
                if (prog === 0) stage = "Initializing";
                else if (prog > 0 && prog < 10) stage = "Processing";
                else stage = "Downloading";

                // Only update notification if stage or progress changed
                if (stage !== lastStage || prog !== lastProgress) {
                    lastStage = stage;
                    lastProgress = prog;

                    let message = "";
                    if (stage === "Initializing") message = `⟳ ${stage}: ${title} - ${artists}`;
                    else if (stage === "Processing") message = `⟳ ${stage}: ${title} - ${artists}`;
                    else {
                        const bars = 10;
                        const filled = Math.floor(prog / 100 * bars);
                        const bar = "█".repeat(filled) + "░".repeat(bars - filled);
                        message = `⟳ Download ${prog}%: ${title} - ${artists}\n[${bar}]\nFolder: ${outputs[url] || "Unknown"}`;
                    }
                    showNotification(notifId, message);
                }
            }, 1000);
        };


        const downloadMenuItem = new Spicetify.ContextMenu.Item(
            "Download",
            (uris) => downloadTrack(uris),
            isTrack,
            Spicetify.SVGIcons["download"],
            false
        );
        downloadMenuItem.register();
    });
})();
