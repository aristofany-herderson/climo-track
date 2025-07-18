const stateCustomSelect = NiceSelect.bind(
  document.getElementById("state-select"),
  {
    searchable: true,
    placeholder: "Selecione um estado",
    searchtext: "Procure por um estado",
  }
);

const cityCustomSelect = NiceSelect.bind(
  document.getElementById("city-select"),
  {
    searchable: true,
    placeholder: "Selecione um município",
    searchtext: "Procure por um município",
  }
);

const databaseUrl = "http://127.0.0.1:8000/";
const stateSelect = document.querySelector("#state-select");
const citySelect = document.querySelector("#city-select");
const form = document.querySelector("#form");
const cityData = document.querySelector("#cityData");
const dataShow = document.querySelector("#data-show");
const cityName = document.querySelector("#city-name");
const climaticSubtype = document.querySelector("#climatic-subtype");

const setHTMLCityDataOpen = () => {
  dataShow.setAttribute("data-has-data", "");
};

const setHTMLCityDataClosed = () => {
  dataShow.removeAttribute("data-has-data");
};

const setCityName = ({ name }) => {
  cityName.textContent = name;
};

const getCities = async () => {
  const cities = await fetch(`${databaseUrl}cities`).then((response) =>
    response.json()
  );
  return cities;
};

const getCity = async ({ id }) => {
  const city = await fetch(`${databaseUrl}cities/${id}`).then((response) =>
    response.json()
  );

  return city;
};

const getStates = async () => {
  const states = await fetch(`${databaseUrl}states`).then((response) =>
    response.json()
  );
  return states;
};

const getFields = async () => {
  const [cities, states] = await Promise.all([getCities(), getStates()]);

  return { cities, states };
};

const addFieldsToHTML = async () => {
  const { cities, states } = await getFields();

  for (const [index, state] of states.entries()) {
    const HTML = `<option value="${state.id}" ${index === 0 && "selected"}>${
      state.name
    }</option>`;

    stateSelect.innerHTML += HTML;
  }

  for (const [index, city] of cities.entries()) {
    const HTML = `<option value="${city.id}" ${index === 0 && "selected"}>${
      city.station
    }</option>`;

    citySelect.innerHTML += HTML;
  }

  stateCustomSelect.update();
  cityCustomSelect.update();
};

addFieldsToHTML();

const addCityDataToHTML = async ({ id }) => {
  const data = await getCity({ id });

  cityData.innerHTML = "";
  for (const city of data.monthly_data) {
    const HTML = `<tr><th>${city.name}</th><td>${Number(city.temp).toFixed(
      1
    )}°C</td><td>${Number(city.precip).toFixed(1)}mm</td><td>${
      city.condition
    }</td></tr>`;

    cityData.innerHTML += HTML;
  }

  const HTML = `<tr><th>Média</th><td>${Number(data.averages.avg_temp).toFixed(
    1
  )}°C</td><td>${Number(data.averages.avg_precip).toFixed(
    1
  )}mm</td><th>Meses secos: ${data.dry_months_count}</th></tr>`;

  cityData.innerHTML += HTML;

  const climaticHTML = `
      <figure class="figure">
        ${
          data.dry_months_count <= 3
            ? `<img src="/static/icons/storm.svg" alt="weather svg" />`
            : data.dry_months_count <= 6
            ? `<img src="/static/icons/rain.svg" alt="weather svg" />`
            : data.dry_months_count <= 10
            ? `<img src="/static/icons/sun-cloud.svg" alt="weather svg" />`
            : `<img src="/static/icons/sun.svg" alt="weather svg" />`
        }
      </figure>
      <p class="type">Subtipo Climático:</p>
      <span class="value">
        ${
          data.dry_months_count < 1
            ? "Super úmido"
            : data.dry_months_count <= 3
            ? "Úmido"
            : data.dry_months_count <= 5
            ? "Semi Úmido"
            : data.dry_months_count === 6
            ? "Semi Árido"
            : data.dry_months_count <= 8
            ? "Médio"
            : data.dry_months_count <= 10
            ? "Forte"
            : data.dry_months_count === 11
            ? "Muito Forte"
            : "Desértico"
        }
      </span>
    `;

  climaticSubtype.innerHTML = climaticHTML;
  climaticSubtype.setAttribute("data-show", "true")
};

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const selectedCityId = citySelect.value;
  const selectedCityName = document.querySelector(
    `option[value="${selectedCityId}"]`
  ).textContent;

  addCityDataToHTML({ id: selectedCityId });
  setHTMLCityDataOpen();
  setCityName({ name: selectedCityName });
});
