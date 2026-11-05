/* Vedanshee eats — a multi-city Stars Hollow-style food diary */

const CATEGORY_STYLE = {
  "Restaurant":   { color: "#b5502a", emoji: "🍽️" },
  "Cafe":         { color: "#8c6239", emoji: "🥐" },
  "Coffee":       { color: "#5b3a1e", emoji: "☕" },
  "Bakery":       { color: "#d98136", emoji: "🥖" },
  "Bagels":       { color: "#c9a227", emoji: "🥯" },
  "Pizza":        { color: "#a3322b", emoji: "🍕" },
  "Diner":        { color: "#33506b", emoji: "🍳" },
  "Fast Casual":  { color: "#4f5d3f", emoji: "🥗" },
  "Bubble Tea":   { color: "#9a5ea7", emoji: "🧋" },
  "Dessert":      { color: "#c25b8a", emoji: "🍩" },
  "Market":       { color: "#6b7f5a", emoji: "🧺" },
  "Street Food":  { color: "#c77f2e", emoji: "🌯" },
  "Food Truck":   { color: "#d06b35", emoji: "🚚" },
  "Bar / Pub":    { color: "#54402d", emoji: "🍺" },
  "Wine Tasting": { color: "#7b3f61", emoji: "🍷" },
};

const QUOTES = [
  "\u201CI need coffee in an IV.\u201D \u2014 Lorelai Gilmore",
  "\u201CCoffee, coffee, coffee!\u201D \u2014 Lorelai Gilmore",
  "\u201CI'm attracted to pie. It doesn't mean I need to date pie.\u201D \u2014 Lorelai Gilmore",
  "\u201CEverything's magical when it snows.\u201D \u2014 Lorelai Gilmore",
  "\u201CLuke can waltz!\u201D \u2014 Lorelai Gilmore",
  "\u201CIf you're gonna throw your life away, he'd better have a motorcycle!\u201D \u2014 Lorelai Gilmore",
  "\u201CI live in two worlds. One is a world of books.\u201D \u2014 Rory Gilmore",
  "\u201CPeople are particularly stupid today.\u201D \u2014 Michel Gerard",
  "\u201CWho ate my pop-tart?\u201D \u2014 Lorelai Gilmore",
  "\u201COy with the poodles already!\u201D \u2014 Lorelai Gilmore",
];

const QUIPS = [
  "Lorelai would order two of everything here.",
  "Rory would bring a book. And a backup book.",
  "Sookie is somewhere in the kitchen, panicking beautifully.",
  "Luke would say it's too fancy. He'd still eat it.",
  "Approved by the Stars Hollow town meeting.",
  "Kirk has definitely worked here at some point.",
  "Emily Gilmore would request a different table. Twice.",
  "Perfect for a Friday night dinner (minus the drama).",
  "Michel would rate it: \u201Cadequate.\u201D High praise.",
  "Paris Geller efficiency rating: acceptable.",
  "Worth monologuing about at 90 words per minute.",
  "Taylor Doose would try to put it in a festival.",
];

const map = L.map("map", { zoomControl: true }).setView([40.745, -73.985], 12.5);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom: 19,
}).addTo(map);

const state = { search: "", category: "All", region: "All" };
const markers = new Map();

function styleFor(cat) {
  return CATEGORY_STYLE[cat] || { color: "#b5502a", emoji: "🍽️" };
}

function makeIcon(place) {
  const s = styleFor(place.category);
  return L.divIcon({
    className: "",
    html: `<div class="gg-marker" style="background:${s.color}"><span>${s.emoji}</span></div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 28],
    popupAnchor: [0, -26],
  });
}

const MICHELIN_ROSETTE = `<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="currentColor">${
  [0, 60, 120, 180, 240, 300].map((a) => `<circle cx="12" cy="5.6" r="4.4" transform="rotate(${a} 12 12)"/>`).join("")
}</g><path fill="#fff" d="M12 8.2l1.1 2.3 2.5.3-1.8 1.7.5 2.5-2.3-1.2-2.3 1.2.5-2.5-1.8-1.7 2.5-.3z"/></svg>`;

function michelinLabel(place) {
  return `${place.michelin} Michelin Star${place.michelin > 1 ? "s" : ""}`;
}

function michelinBadge(place) {
  if (!place.michelin) return "";
  const label = michelinLabel(place);
  return `<span class="michelin-badge" title="${label}" aria-label="${label}">${MICHELIN_ROSETTE.repeat(place.michelin)}</span>`;
}

function isCompactLayout() {
  return window.matchMedia("(max-width: 860px), (max-height: 520px)").matches;
}

function popupHtml(place) {
  const s = styleFor(place.category);
  const quip = QUIPS[place.id % QUIPS.length];
  const gmaps = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place.mapQuery || `${place.name}, ${place.location}`)}`;
  return `<div class="popup-inner">
    <div class="popup-cat">${s.emoji} ${place.category}</div>
    <h3>${place.name}${michelinBadge(place)}</h3>
    ${place.michelin ? `<div class="popup-michelin">${michelinLabel(place)}</div>` : ""}
    <div class="popup-cuisine">${place.cuisine}${place.approx ? " · pin location approximate" : ""}</div>
    <div class="popup-location">${place.location}</div>
    <div class="popup-quip">${quip}</div>
    <a class="popup-link" href="${gmaps}" target="_blank" rel="noopener">Open in Google Maps →</a>
    <button type="button" class="popup-back-list">↓ Back to list</button>
  </div>`;
}

let pendingReturnId = null;
let suppressReturnScroll = false;

function scrollMapIntoView() {
  document.querySelector(".map-wrap")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function scrollCardIntoView(id) {
  const card = listEl.querySelector(`[data-id="${id}"]`);
  if (!card) return;
  card.classList.add("active");
  card.scrollIntoView({ block: "center", behavior: "smooth" });
}

function focusPlace(place, { fromList = false } = {}) {
  const marker = markers.get(place.id);
  if (!marker) return;

  pendingReturnId = place.id;
  highlightCard(place.id, { scroll: !isCompactLayout() });

  const showOnMap = () => {
    map.invalidateSize();
    map.flyTo(marker.getLatLng(), 16, { duration: 0.8 });
    suppressReturnScroll = true;
    marker.openPopup();
    setTimeout(() => {
      suppressReturnScroll = false;
    }, 150);
  };

  if (isCompactLayout() && fromList) {
    scrollMapIntoView();
    setTimeout(showOnMap, 420);
  } else {
    showOnMap();
  }
}

PLACES.forEach((place) => {
  const marker = L.marker([place.lat, place.lng], { icon: makeIcon(place) })
    .bindPopup(popupHtml(place));
  marker.on("click", () => {
    pendingReturnId = place.id;
    highlightCard(place.id, { scroll: !isCompactLayout() });
  });
  markers.set(place.id, marker);
});

map.on("popupclose", () => {
  if (suppressReturnScroll || pendingReturnId == null || !isCompactLayout()) return;
  const id = pendingReturnId;
  pendingReturnId = null;
  setTimeout(() => scrollCardIntoView(id), 60);
});

map.getContainer().addEventListener("click", (e) => {
  const back = e.target.closest(".popup-back-list");
  if (!back) return;
  e.preventDefault();
  map.closePopup();
});

map.getContainer().addEventListener("click", (e) => {
  const link = e.target.closest(".popup-link");
  if (!link || !isCompactLayout() || pendingReturnId == null) return;
  const id = pendingReturnId;
  // After opening Google Maps, drop back to the list so browsing can continue
  setTimeout(() => {
    if (pendingReturnId === id) {
      pendingReturnId = null;
      map.closePopup();
      scrollCardIntoView(id);
    }
  }, 350);
});

/* — Filters — */
const regions = [
  { id: "All", label: "Everywhere", emoji: "🗺️" },
  { id: "nyc", label: "New York City", emoji: "🗽" },
  { id: "mcminnville", label: "McMinnville", emoji: "🌲" },
  { id: "sf", label: "San Francisco Bay Area", emoji: "🌉" },
  { id: "la", label: "Los Angeles Area", emoji: "🌴" },
  { id: "sd", label: "San Diego Area", emoji: "☀️" },
  { id: "dc", label: "Washington, DC", emoji: "🏛️" },
  { id: "tampa", label: "Tampa", emoji: "🍊" },
  { id: "indiana", label: "Indiana", emoji: "🌽" },
  { id: "texas", label: "Texas", emoji: "🤠" },
];
const locationFiltersEl = document.getElementById("location-filters");

regions.forEach((region) => {
  const count = region.id === "All"
    ? PLACES.length
    : PLACES.filter((place) => place.region === region.id).length;
  const btn = document.createElement("button");
  btn.className = "location-chip" + (region.id === "All" ? " active" : "");
  btn.textContent = `${region.emoji} ${region.label} (${count})`;
  btn.addEventListener("click", () => {
    state.region = region.id;
    state.category = "All";
    locationFiltersEl.querySelectorAll(".location-chip").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    filtersEl.querySelectorAll(".filter-chip").forEach((b) => b.classList.remove("active"));
    filtersEl.querySelector(".filter-chip")?.classList.add("active");
    render();
    fitVisiblePlaces();
  });
  locationFiltersEl.appendChild(btn);
});

const categories = ["All", ...Object.keys(CATEGORY_STYLE).filter((c) => PLACES.some((p) => p.category === c))];
const filtersEl = document.getElementById("filters");

categories.forEach((cat) => {
  const btn = document.createElement("button");
  btn.className = "filter-chip" + (cat === "All" ? " active" : "");
  btn.textContent = cat === "All" ? "All the food" : `${styleFor(cat).emoji} ${cat}`;
  btn.addEventListener("click", () => {
    state.category = cat;
    filtersEl.querySelectorAll(".filter-chip").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    render();
    fitVisiblePlaces();
  });
  filtersEl.appendChild(btn);
});

document.getElementById("search").addEventListener("input", (e) => {
  state.search = e.target.value.trim().toLowerCase();
  render();
});

/* — List rendering — */
const listEl = document.getElementById("place-list");
const countEl = document.getElementById("results-count");

function visiblePlaces() {
  return PLACES.filter((p) => {
    const matchesRegion = state.region === "All" || p.region === state.region;
    const matchesCat = state.category === "All" || p.category === state.category;
    const matchesSearch =
      !state.search ||
      p.name.toLowerCase().includes(state.search) ||
      p.cuisine.toLowerCase().includes(state.search) ||
      p.location.toLowerCase().includes(state.search);
    return matchesRegion && matchesCat && matchesSearch;
  });
}

function render() {
  const visible = visiblePlaces();
  const visibleIds = new Set(visible.map((p) => p.id));

  markers.forEach((marker, id) => {
    const shouldShow = visibleIds.has(id);
    const onMap = map.hasLayer(marker);
    if (shouldShow && !onMap) marker.addTo(map);
    if (!shouldShow && onMap) map.removeLayer(marker);
  });

  const regionPlaces = state.region === "All"
    ? PLACES
    : PLACES.filter((place) => place.region === state.region);
  const regionLabel = regions.find((region) => region.id === state.region)?.label || "Everywhere";
  const regionPhrase = state.region === "All" ? "across the map" : `in ${regionLabel}`;
  countEl.textContent =
    visible.length === regionPlaces.length && state.category === "All" && !state.search
      ? `All ${visible.length} stops ${regionPhrase}`
      : `${visible.length} of ${regionPlaces.length} places ${regionPhrase}`;

  listEl.innerHTML = "";
  visible.forEach((place) => {
    const s = styleFor(place.category);
    const li = document.createElement("li");
    li.className = "place-card";
    li.dataset.id = place.id;
    li.innerHTML = `
      <div class="place-num">No. ${place.id}</div>
      <h3>${place.name}${michelinBadge(place)}</h3>
      <div class="place-meta"><span class="cat-dot" style="background:${s.color}"></span>${s.emoji} ${place.cuisine}</div>
      <div class="place-location">${place.location}</div>`;
    li.addEventListener("click", () => focusPlace(place, { fromList: true }));
    listEl.appendChild(li);
  });
}

function fitVisiblePlaces() {
  const visible = visiblePlaces();
  if (!visible.length) return;
  if (visible.length === 1) {
    map.flyTo([visible[0].lat, visible[0].lng], 15, { duration: 0.8 });
    return;
  }
  map.fitBounds(
    L.latLngBounds(visible.map((place) => [place.lat, place.lng])).pad(0.08),
    { animate: true }
  );
}

function highlightCard(id, { scroll = true } = {}) {
  listEl.querySelectorAll(".place-card").forEach((c) => c.classList.remove("active"));
  const card = listEl.querySelector(`[data-id="${id}"]`);
  if (!card) return;
  card.classList.add("active");
  if (scroll) card.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

/* — Rotating quotes — */
const quoteEl = document.getElementById("quote");
let quoteIdx = 0;
setInterval(() => {
  quoteIdx = (quoteIdx + 1) % QUOTES.length;
  quoteEl.style.opacity = 0;
  setTimeout(() => {
    quoteEl.innerHTML = QUOTES[quoteIdx];
    quoteEl.style.opacity = 1;
  }, 400);
}, 6000);

render();
fitVisiblePlaces();
