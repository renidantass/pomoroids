const container = document.querySelector('#blacklist ul');

const baseAddress = "http://127.0.0.1:8000";
const endpoint = "settings";

function drawSettings(settings) {
  const container = document.querySelector('#blacklist ul');
  const blocked_sites = settings.blacklist.sites;

  for(const site of blocked_sites) {
    const element = document.createElement('li');
    element.innerText = site;
    container.appendChild(element);
  }
}

fetch(`${baseAddress}/${endpoint}`)
  .then(res => {
    return res.json()
  })
  .then(data => {
    console.log(data);
    drawSettings(data);
  })
  .catch(err => console.log)
