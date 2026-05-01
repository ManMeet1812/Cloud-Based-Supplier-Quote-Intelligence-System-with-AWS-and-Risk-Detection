const API_BASE_URL = "https://7p9n4zgxv4.execute-api.ca-central-1.amazonaws.com";

document.getElementById("quoteForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const quoteData = {
    supplierName: document.getElementById("supplierName").value,
    materialName: document.getElementById("materialName").value,
    unitPrice: Number(document.getElementById("unitPrice").value),
    quantity: Number(document.getElementById("quantity").value),
    deliveryDays: Number(document.getElementById("deliveryDays").value),
    region: document.getElementById("region").value,
    fileUrl: document.getElementById("fileUrl").value
  };

  try {
    const response = await fetch(`${API_BASE_URL}/submit-quote`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(quoteData)
    });

    const result = await response.json();
    const body = typeof result.body === "string" ? JSON.parse(result.body) : result;

    document.getElementById("submitMessage").textContent =
      `Quote submitted. Risk Status: ${body.riskStatus}`;

    document.getElementById("quoteForm").reset();

    loadQuotes();
  } catch (error) {
    document.getElementById("submitMessage").textContent =
      "Error submitting quote. Check console.";
    console.error(error);
  }
});

async function loadQuotes() {
  try {
    const response = await fetch(`${API_BASE_URL}/quotes`);
    const result = await response.json();

    const body = typeof result.body === "string" ? JSON.parse(result.body) : result;
    const quotes = body.quotes || [];

    const tableBody = document.getElementById("quotesTableBody");
    tableBody.innerHTML = "";

    let normalCount = 0;
    let anomalyCount = 0;

    quotes.forEach((quote) => {
      if (quote.riskStatus === "Normal") normalCount++;
      if (quote.riskStatus === "Anomaly") anomalyCount++;

      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${quote.supplierName || ""}</td>
        <td>${quote.materialName || ""}</td>
        <td>${quote.unitPrice || ""}</td>
        <td>${quote.quantity || ""}</td>
        <td>${quote.totalPrice || ""}</td>
        <td>${quote.deliveryDays || ""} days</td>
        <td class="${quote.riskStatus === "Anomaly" ? "risk-anomaly" : "risk-normal"}">
          ${quote.riskStatus || ""}
        </td>
        <td>${quote.riskReason || ""}</td>
      `;

      tableBody.appendChild(row);
    });

    document.getElementById("totalQuotes").textContent = quotes.length;
    document.getElementById("normalQuotes").textContent = normalCount;
    document.getElementById("anomalyQuotes").textContent = anomalyCount;

  } catch (error) {
    console.error("Error loading quotes:", error);
  }
}

loadQuotes();