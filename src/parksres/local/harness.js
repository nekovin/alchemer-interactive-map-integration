const MAP_BOX = "../alchemer-html/map-box.html";
const STORE = "alchemer-harness";

const FIELD_CONSTS = [
  ["ALCHEMER_HIDDEN_FIELD_ID", "names"],
  ["ALCHEMER_PIN_FIELD_ID", "pins"],
  ["ALCHEMER_CATEGORY_FIELD_ID", "categories"],
  ["ALCHEMER_ERROR_FIELD_ID", "errors"]
];

function saved() {
  try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { return {}; }
}

function save() {
  localStorage.setItem(STORE, JSON.stringify({
    url: document.getElementById("payload-url").value,
    key: document.getElementById("maps-key").value,
    action: document.getElementById("action").value
  }));
}

function substitute(source) {
  const url = document.getElementById("payload-url").value;
  const key = document.getElementById("maps-key").value;
  return source
    .replace(/\[question\("value"\),\s*id="182"\]/g, url)
    .replace(/\[question\("value"\),\s*id="181"\]/g, key)
    .replace(/\[question\("value"\),\s*id="\w+"\]/g, "")
    .replace(/\[question\("option value"\),[^\]]*\]/g, "")
    .replace(/\[survey\("id"\)\]/g, "0");
}

function fieldsIn(source) {
  return FIELD_CONSTS
    .map(function (pair) {
      const m = source.match(new RegExp('const\\s+' + pair[0] + '\\s*=\\s*"([^"]+)"'));
      return m ? { id: m[1], label: pair[1] } : null;
    })
    .filter(Boolean);
}

function buildFields(fields, omit) {
  const holder = document.getElementById("hidden-fields");
  const rows = document.querySelector("#fields tbody");
  holder.innerHTML = "";
  rows.innerHTML = "";

  fields.forEach(function (field) {
    if (!omit) {
      const input = document.createElement("input");
      input.type = "text";
      input.id = field.id;
      holder.appendChild(input);
    }
    const tr = document.createElement("tr");
    tr.innerHTML = "<td>" + field.label + "</td><td>" + field.id + "</td>"
      + '<td class="val" data-for="' + field.id + '"><span class="empty">'
      + (omit ? "field not on page" : "(empty)") + "</span></td>";
    rows.appendChild(tr);
  });
}

function watch(fields) {
  setInterval(function () {
    fields.forEach(function (field) {
      const input = document.getElementById(field.id);
      const cell = document.querySelector('[data-for="' + field.id + '"]');
      if (!input || !cell) return;
      cell.textContent = input.value || "";
      if (!input.value) cell.innerHTML = '<span class="empty">(empty)</span>';
    });
  }, 400);
}

async function run(omit) {
  save();
  const path = document.getElementById("action").value;

  const bust = "?t=" + Date.now();
  document.getElementById("box").innerHTML = await (await fetch(MAP_BOX + bust)).text();

  const source = await (await fetch(path + bust)).text();
  const fields = fieldsIn(source);
  buildFields(fields, omit);
  watch(fields);

  const script = document.createElement("script");
  script.textContent = substitute(source);
  document.body.appendChild(script);

  console.log("[HARNESS] ran", path, "| fields:", fields.map(f => f.id));
}

function watchBar() {
  console.log("Confirm bar");
  setInterval(function () {
    const bar = document.querySelector(".sg-button-bar");
    const confirm = document.getElementById("confirm");
    document.getElementById("bar-state").textContent =
      "button bar: " + (bar && bar.style.display !== "none" ? "visible" : "hidden")
      + " | confirm button: " + (confirm ? "present" : "not created");
  }, 400);
}

window.addEventListener("DOMContentLoaded", function () {
  watchBar();
  document.getElementById("sg_NextButton").addEventListener("click", function () {
    console.log("[HARNESS] Next clicked");
  });
  document.getElementById("sg_BackButton").addEventListener("click", function () {
    console.log("[HARNESS] Back clicked");
  });
  const prev = saved();
  if (prev.url) document.getElementById("payload-url").value = prev.url;
  if (prev.key) document.getElementById("maps-key").value = prev.key;
  if (prev.action) document.getElementById("action").value = prev.action;

  document.getElementById("run").addEventListener("click", function () { run(false); });
  document.getElementById("omit").addEventListener("click", function () { run(true); });
});
