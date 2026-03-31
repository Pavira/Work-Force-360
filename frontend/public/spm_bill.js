// -----------------------------
// Read invoice_id from URL
// -----------------------------
const params = new URLSearchParams(window.location.search);
const invoiceId = params.get("invoice_id");
const isPreviewMode =
  params.get("preview") === "1" || params.get("preview") === "true";
const apiBaseFromQuery = params.get("api_base");
const shouldPrint =
  params.get("print") === "1" || params.get("print") === "true";

// -----------------------------
// Config
// -----------------------------
const API_BASE_URL =
  (apiBaseFromQuery ? decodeURIComponent(apiBaseFromQuery) : "") ||
  window.API_BASE_URL ||
  window.location.origin;

function renderInvoice(invoice) {
  setText("company_name", "M/S SPM ENGINEERING");
  setText("company_address", "347, SANGANUR ROAD, GANAPATHY, COIMBATORE");
  setText("company_gstin", "33AFHPE4773N1Z6");
  setText("company_state", "TAMIL NADU");
  setText("company_state_code", "33");
  setText("seller_contact", "");
  setText("seller_email", "");

  setText("invoice_number", invoice.invoice_number);
  setText("invoice_date", invoice.invoice_date);
  setText("po_number", invoice.po_number || "-");
  setText("delivery_note", invoice.delivery_note || "");
  setText("po_date", invoice.po_date || "");

  setText("buyer_name", invoice.buyer?.name || "-");
  setText("buyer_address", invoice.buyer?.address || "-");
  setText("buyer_gstin", invoice.buyer?.gstin || "-");
  setText("buyer_pan", invoice.buyer?.panNumber || invoice.buyer?.pan_number || "-");
  setText("buyer_contact", invoice.delivery_contact || "-");
  setText("buyer_phone", invoice.buyer?.phone || "-");
  setText("buyer_email", invoice.buyer?.email || "-");

  setText("consignee_name", invoice.consignee?.name || "-");
  setText("consignee_address", invoice.consignee?.address || "-");
  setText("consignee_gstin", invoice.consignee?.gstin || "-");
  setText(
    "consignee_pan",
    invoice.consignee?.panNumber || invoice.consignee?.pan_number || "-",
  );
  setText("consignee_contact", invoice.consignee?.contact || "-");
  setText("consignee_phone", invoice.consignee?.phone || "-");
  setText("consignee_email", invoice.consignee?.email || "-");

  const itemsContainer = document.getElementById("invoice_items");
  if (itemsContainer) {
    itemsContainer.innerHTML = "";

    (invoice.items || []).forEach((item, index) => {
      const row = document.createElement("div");
      row.className = "table-row";

      row.innerHTML = `
        <div class="col si">${index + 1}</div>
        <div class="col desc">${escapeHtml(item.name)}</div>
        <div class="col hsn">${escapeHtml(item.hsn)}</div>
        <div class="col gst">${escapeHtml(item.gst_percentage || "-")}</div>
        <div class="col qty">${formatNumber(item.quantity)}</div>
        <div class="col rate">${formatNumber(item.rate)}</div>
        <div class="col per">${escapeHtml(item.uom || "")}</div>
        <div class="col amt">${formatNumber(item.amount)}</div>
      `;

      itemsContainer.appendChild(row);
    });
  }

  setText("subtotal", formatNumber(invoice.totals?.subtotal));
  setText("cgst", formatNumber(invoice.totals?.cgst));
  setText("sgst", formatNumber(invoice.totals?.sgst));
  setText("round_off", formatNumber(invoice.totals?.round_off));
  setText("grand_total", formatNumber(invoice.totals?.total));
  setText("amount_in_words", invoice.totals?.amount_in_words || "");

  if (shouldPrint) {
    setTimeout(() => {
      try {
        window.focus();
        window.print();
      } catch (printErr) {
        console.error("Print error:", printErr);
      }
    }, 300);

    window.onafterprint = () => {
      window.close();
    };
  }
}

if (isPreviewMode) {
  const previewRaw = sessionStorage.getItem("invoice_preview_data");
  if (!previewRaw) {
    alert("Preview data not found");
    throw new Error("Preview data missing");
  }
  renderInvoice(JSON.parse(previewRaw));
} else {
  if (!invoiceId) {
    alert("Invoice ID is missing");
    throw new Error("Invoice ID missing");
  }

  fetch(`${API_BASE_URL}/invoices/${invoiceId}`, {
    method: "GET",
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Failed to fetch invoice");
      }
      return res.json();
    })
    .then((res) => {
      if (!res.success) {
        throw new Error("Invoice fetch unsuccessful");
      }
      renderInvoice(res.data);
    })
    .catch((err) => {
      console.error("Invoice load error:", err);
      alert("Failed to load invoice details");
    });
}

// -----------------------------
// Helper function
// -----------------------------
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.innerText = value ?? "";
}

function formatNumber(value) {
  if (value === null || value === undefined || value === "") return "";
  const num = Number(value);
  if (Number.isNaN(num)) return value;
  return num.toFixed(2);
}

function escapeHtml(value) {
  if (value === null || value === undefined) return "";
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
