let authors = [];
let chartInstance = null;

const authorIdInput = document.getElementById("authorIdInput");
const searchButton = document.getElementById("searchButton");
const authorResult = document.getElementById("authorResult");
const placeholder = document.getElementById("placeholder");
const errorMessage = document.getElementById("errorMessage");
const loading = document.getElementById("loading");

// CSV load #TEMPORARY SOLUTION
Papa.parse("researcher_domains_sample.csv", {
  download: true,
  header: true,
  complete: function (results) {
    authors = results.data;
    console.log("CSV loaded:", authors);
  },
});

// Show the info of the researcher
function displayAuthor(author) {
  if (!author) return;

  let domains = {};
  try {
    domains = JSON.parse(author.domain_affinity.replace(/'/g, '"'));
  } catch (e) {
    console.error("Failed to parse domain_affinity:", e);
  }

  let domainList = Object.entries(domains)
    .map(([field, score]) => `<li>${field}: ${score}</li>`)
    .join("");

  authorResult.innerHTML = `
    <h2>${author.Fname || ""} ${author.Gname || ""}</h2>
    <p><strong>ORCID:</strong> ${author.OID}</p>
    <p><strong>Role:</strong> ${author.Role || "N/A"}</p>
    <p><strong>Organization:</strong> ${author.Org || "N/A"}</p>
    <p><strong>Domains:</strong></p>
    <ul>${domainList}</ul>
  `;

  placeholder.style.display = "none";
  authorResult.style.display = "block";
  errorMessage.style.display = "none";

  displayChart(author);
}

// Draw chart magic
function displayChart(author) {
  if (!author.domain_affinity) return;

  let domains = {};
  try {
    domains = JSON.parse(author.domain_affinity.replace(/'/g, '"'));
  } catch (e) {
    console.error("Failed to parse domain_affinity:", e);
    return;
  }

  const labels = Object.keys(domains);
  const values = Object.values(domains).map((v) => parseFloat(v));

  const ctx = document.getElementById("domainChart").getContext("2d");

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Domain Affinity",
          data: values,
          backgroundColor: "rgba(54, 162, 235, 0.7)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: `Scientific Domains of ${author.Fname} ${author.Gname} (${author.OID})`,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 1,
        },
        x: {
          ticks: {
            autoSkip: false,
            maxRotation: 45,
            minRotation: 30,
          },
        },
      },
    },
  });

  document.getElementById("chartContainer").style.display = "block";
}

// Search the author
function handleSearch() {
  const authorId = authorIdInput.value.trim();

  if (!authorId) {
    showError("Please enter an ORCID ID");
    return;
  }

  loading.style.display = "block";
  authorResult.style.display = "none";
  errorMessage.style.display = "none";

  const author = authors.find((a) => String(a.OID) === authorId);

  if (author) {
    displayAuthor(author);
  } else {
    showError(`No researcher found with ORCID: ${authorId}`);
    document.getElementById("chartContainer").style.display = "none";
  }

  loading.style.display = "none";
}

// Show error
function showError(message) {
  errorMessage.textContent = message;
  errorMessage.style.display = "block";
  authorResult.style.display = "none";
  document.getElementById("chartContainer").style.display = "none";
}

// Enter key
searchButton.addEventListener("click", handleSearch);
authorIdInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    handleSearch();
  }
});
