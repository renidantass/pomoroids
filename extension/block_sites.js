const url = new URL(window.location);
const currentDomain = url.hostname;

const baseAddress = "http://127.0.0.1:8000";
const endpoints = {
  settings: "settings",
  status: "status",
};

const blockSites = (sites) => {
  let site = "";

  for (let i = 0; i < sites.length; i++) {
    site = sites[i];

    if (currentDomain == site) {
      const imageUrl = chrome.runtime.getURL("bloqueado.png");
      window.location.href = imageUrl;
    }
  }
};

const updateBlockedSites = () => {
  fetch(`${baseAddress}/${endpoints.settings}`)
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      blockSites(data.blacklist.sites);
    })
    .catch((err) => console.log);
};

const isInSession = () => {
  fetch(`${baseAddress}/${endpoints.status}`)
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      const status = data.status;
      if (status) {
        updateBlockedSites();
      }
    })
    .catch((err) => console.log);
};

isInSession();
