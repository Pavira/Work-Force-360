export default function InvoiceTemplate({ invoiceData = null }) {
  // Format currency helper
  const formatCurrency = (value) => {
    if (!value) return "0.00";
    return parseFloat(value)
      .toFixed(2)
      .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  // Mock company details
  const companyDetails = {
    name: "SPM ENGINEERING",
    address: "347, SANGANUR ROAD, GANAPATHY, COIMBATORE",
    gstin: "33AFHPE4773N1Z6",
    state: "Tamil Nadu",
    stateCode: "33",
  };

  // Mock invoice items data for table rows
  const getInvoiceItems = () => {
    if (invoiceData?.items && Array.isArray(invoiceData.items)) {
      return invoiceData.items;
    }
    return [];
  };

  const items = getInvoiceItems();
  const maxRows = 15;
  const itemRows = Array(Math.max(maxRows - items.length, 0)).fill(null);

  return (
    <div className="min-h-screen flex justify-center bg-gray-200 py-2">
      {/* A4 Page */}
      <div className="w-[210mm] h-[297mm] bg-white text-black flex flex-col items-center">
        {/* TOP HEADING (Outside Box) */}
        <div className="h-[10mm] flex items-center justify-center">
          <h1 className="text-[14px] font-bold tracking-wide">TAX INVOICE</h1>
        </div>

        {/* MAIN OUTER BOX */}
        <div className="w-[190mm] h-[270mm] border border-black text-[9pt] leading-tight flex flex-col">
          {/* SECTION 1: CONSIGNEE DETAILS (30%) */}
          {/* SECTION 1: CONSIGNEE DETAILS (78mm) */}
          <div className="h-[78mm] border-b border-black flex">
            {/* LEFT 60% — 3 equal horizontal sections */}
            <div className="w-[114mm] border-r border-black flex flex-col">
              <div className="h-[26mm] border-b border-black pl-[1mm]">
                <p className="text-[10pt] font-semibold">
                  {companyDetails.name}
                </p>
                <p>{companyDetails.address}</p>
                <p>GSTIN/UIN : {companyDetails.gstin}</p>
                <p>
                  State Name : {companyDetails.state}, Code :{" "}
                  {companyDetails.stateCode}
                </p>
                <p>Contact : {invoiceData?.seller_contact || ""}</p>
                <p>E-Mail : {invoiceData?.seller_email || ""}</p>
              </div>
              <div className="h-[26mm] border-b border-black pl-[1mm]">
                {/* Consignee / Buyer Details */}
                <p className="text-[8pt] pb-[1mm]">Consignee (Ship to)</p>
                <p className="text-[10pt] font-semibold">
                  {invoiceData?.consignee.name || "Consignee name"}
                </p>
                <p>GSTIN/UIN : {invoiceData?.consignee.gstin || ""}</p>
                <p>PAN/IT No : {invoiceData?.consignee.panNumber || ""}</p>
                <p>Contact person : {invoiceData?.consignee.contact || ""}</p>
                <p>Contact : {invoiceData?.consignee.phone || ""}</p>
              </div>
              <div className="h-[26mm] pl-[1mm]">
                {/* Shipping / GST / Address */}
                <p className="text-[8pt] pb-[1mm]">Buyer (Bill to)</p>
                <p className="text-[10pt] font-semibold">
                  {invoiceData?.buyer_name || "Buyer name"}
                </p>
                <p>GSTIN/UIN : {invoiceData?.buyer.gstin || ""}</p>
                <p>PAN/IT No : {invoiceData?.buyer.panNumber || ""}</p>
                <p>
                  Delivery Contact person :{" "}
                  {invoiceData?.delivery_contact || ""}
                </p>
                <p>Mobile : {invoiceData?.buyer.phone || ""}</p>
              </div>
            </div>

            {/* RIGHT 40% — 50:50 horizontal split */}
            <div className="w-[76mm] flex flex-col">
              {/* TOP SECTION — Invoice Meta */}
              <div className="h-[39mm] border-b border-black">
                {/* ROW 1 */}
                <div className="h-[7.8mm] flex border-b border-black">
                  <div className="w-[38mm] border-r border-black pl-[1mm] text-[8pt]">
                    {/* Invoice No */}
                    <div className="flex justify-between">
                      <p>Invoice No</p>
                      <p className="pr-[1mm]">e-Way Bill No</p>
                    </div>
                    <p className="font-semibold text-[9pt]">
                      {invoiceData?.invoice_number || ""}
                    </p>
                  </div>
                  <div className="w-[38mm] pl-[1mm] text-[8pt]">
                    {/* Date */}
                    <p>Dated</p>
                    <p className="font-semibold text-[9pt]">
                      {invoiceData?.invoice_date || ""}
                    </p>
                  </div>
                </div>

                {/* ROW 2 */}
                <div className="h-[7.8mm] flex border-b border-black">
                  <div className="w-[38mm] border-r border-black pl-[1mm] text-[8pt]">
                    {/* Delivery Note */}
                    <p>Delivery Note</p>
                  </div>
                  <div className="w-[38mm] pl-[1mm] text-[8pt]">
                    {invoiceData?.delivery_note || ""}
                  </div>
                </div>

                {/* ROW 3 */}
                <div className="h-[7.8mm] flex border-b border-black">
                  <div className="w-[38mm] border-r border-black pl-[1mm] text-[8pt]">
                    {/* Buyer Order No */}
                    <p>Buyer's Order No.</p>
                    <p className="font-semibold text-[9pt]">
                      {invoiceData?.po_number || ""}
                    </p>
                  </div>
                  <div className="w-[38mm] pl-[1mm] text-[8pt]">
                    {/* Dated */}
                    <p>Dated</p>
                    <p className="font-semibold"></p>
                  </div>
                </div>

                {/* ROW 4 */}
                <div className="h-[7.8mm] flex border-b border-black">
                  <div className="w-[38mm] border-r border-black pl-[1mm] text-[8pt]">
                    {/* Dispatch Doc No */}
                    <p>Dispatch Doc No</p>
                  </div>
                  <div className="w-[38mm] pl-[1mm] text-[8pt]">
                    {/* Delivery Note Date */}
                    {invoiceData?.dispatch_doc_no || ""}
                  </div>
                </div>

                {/* ROW 5 */}
                <div className="h-[7.8mm] flex">
                  <div className="w-[38mm] border-r border-black pl-[1mm] text-[8pt]">
                    <p>Order Cutting</p>
                  </div>
                  <div className="w-[38mm] pl-[1mm] text-[8pt]">
                    <p>Destination</p>
                  </div>
                </div>
              </div>

              {/* BOTTOM SECTION — Transport / Place of Supply */}
              <div className="h-[39mm] p-[3mm] text-[9pt]">
                {/* Transport Name, LR No, Place of Supply */}
              </div>
            </div>
          </div>

          {/* SECTION 2: ITEM TABLE (130mm) */}
          <div className="h-[130mm] border-b border-black flex flex-col">
            {/* TABLE HEADER */}
            <div className="h-[10mm] flex border-b border-black text-[9pt] font-semibold text-center">
              <div className="w-[5mm] border-r border-black flex items-center justify-center">
                SI
              </div>
              <div className="w-[80mm] border-r border-black flex items-center justify-center">
                Description of Goods
              </div>
              <div className="w-[15mm] border-r border-black flex items-center justify-center">
                HSN / SAC
              </div>
              <div className="w-[15mm] border-r border-black flex items-center justify-center">
                GST %
              </div>
              <div className="w-[15mm] border-r border-black flex items-center justify-center">
                Qty
              </div>
              <div className="w-[20mm] border-r border-black flex items-center justify-center">
                Rate
              </div>
              <div className="w-[10mm] border-r border-black flex items-center justify-center">
                Per
              </div>
              <div className="w-[30mm] flex items-center justify-center">
                Amount
              </div>
            </div>

            {/* ITEM ROWS TABLE AREA */}
            <div className="h-[120mm] border-b border-black flex flex-col overflow-hidden">
              {/* Display actual items */}
              {items.map((item, index) => (
                <div
                  key={index}
                  className="h-[8mm] flex border-b border-black text-[8pt]"
                >
                  <div className="w-[5mm] border-r border-black flex items-center justify-center">
                    {index + 1}
                  </div>
                  <div className="w-[80mm] border-r border-black pl-[1mm] flex items-center">
                    {item.description || item.name || ""}
                  </div>
                  <div className="w-[15mm] border-r border-black flex items-center justify-center">
                    {item.hsn || ""}
                  </div>
                  <div className="w-[15mm] border-r border-black flex items-center justify-center">
                    {item.gst_percentage || ""}%
                  </div>
                  <div className="w-[15mm] border-r border-black flex items-center justify-center">
                    {item.quantity || ""}
                  </div>
                  <div className="w-[20mm] border-r border-black flex items-center justify-end pr-[1mm]">
                    {formatCurrency(item.rate)}
                  </div>
                  <div className="w-[10mm] border-r border-black flex items-center justify-center">
                    {item.uom || ""}
                  </div>
                  <div className="w-[30mm] flex items-center justify-end pr-[2mm]">
                    {formatCurrency((item.quantity || 0) * (item.rate || 0))}
                  </div>
                </div>
              ))}

              {/* Empty rows for spacing */}
              {itemRows.map((_, index) => (
                <div key={`empty-${index}`} className="h-[8mm] flex text-[8pt]">
                  <div className="w-[5mm]  flex items-center justify-center"></div>
                  <div className="w-[80mm] border-r border-black pl-[1mm]"></div>
                  <div className="w-[15mm] border-r border-black"></div>
                  <div className="w-[15mm] border-r border-black"></div>
                  <div className="w-[15mm] border-r border-black"></div>
                  <div className="w-[20mm] border-r border-black"></div>
                  <div className="w-[10mm] border-r border-black"></div>
                  <div className="w-[30mm]"></div>
                </div>
              ))}
            </div>

            {/* TAX & TOTAL SECTION */}
            {/* TAX SECTION */}
            <div className="h-[15mm] flex text-[9pt] ">
              {/* LEFT 40% — TAX LABELS */}
              <div className="w-[85mm] border-r border-black flex flex-col font-bold">
                <div className="h-[5mm] flex items-center justify-end pr-[2mm]">
                  SGST 9% TAX
                </div>

                <div className="h-[5mm] flex items-center justify-end pr-[2mm]">
                  CGST 9% TAX
                </div>

                <div className="h-[5mm] flex items-center justify-end pr-[2mm]">
                  Round Off
                </div>
              </div>

              {/* RIGHT 60% — TAX AMOUNTS */}
              <div className="w-[114mm] flex flex-col font-bold">
                <div className="h-[5mm] flex items-center justify-end pr-[3mm]">
                  {formatCurrency(invoiceData?.totals.sgst || 0)}
                </div>

                <div className="h-[5mm] flex items-center justify-end pr-[3mm]">
                  {formatCurrency(invoiceData?.totals.cgst || 0)}
                </div>

                <div className="h-[5mm] flex items-center justify-end pr-[3mm]">
                  {formatCurrency(invoiceData?.totals.round_off || 0)}
                </div>
              </div>
            </div>

            {/* TOTAL SECTION */}
            <div className="h-[5mm] flex text-[9pt] border-t border-black font-bold">
              {/* LEFT 40% — TAX LABELS */}
              <div className="w-[85mm] border-r border-black flex flex-col">
                <div className="h-[5mm] flex items-center justify-end pr-[2mm]">
                  Total
                </div>
              </div>

              {/* RIGHT 60% — TAX AMOUNTS */}
              <div className="w-[114mm] flex flex-col">
                <div className="h-[5mm] flex items-center justify-end pr-[3mm]">
                  {formatCurrency(invoiceData?.totals.total || 0)}
                </div>
              </div>
            </div>
          </div>

          {/* SECTION 3: TERMS & TOTALS (15%) */}
          <div className="h-[51mm] border-b border-black">
            {/* Terms, tax summary, amount in words */}
            <div className="pl-[1mm] text-[8pt]">
              {/* Amount Chargeable (in words) */}
              <p className="font-semibold">Amount Chargeable (in words)</p>
              <p className="font-bold text-[9pt] mt-[1mm]">
                {invoiceData?.totals.amount_in_words || " "} Only
              </p>
              {invoiceData?.notes && (
                <>
                  <p className="font-semibold mt-[3mm]">Notes:</p>
                  <p>{invoiceData.notes}</p>
                </>
              )}
            </div>
          </div>

          {/* SECTION 4: SIGNATURE (5%) */}
          <div className="h-[11mm] flex text-[9pt]">
            {/* LEFT 40% — TAX LABELS */}
            <div className="w-[100mm] border-r border-black flex flex-col">
              <div className="pl-[1mm] text-[8pt]">
                {/* Customer's Seal and Signature */}
                <p>Customer's Seal and Signature</p>
              </div>
            </div>

            {/* RIGHT 60% — TAX AMOUNTS */}
            <div className="w-[100mm] flex flex-col">
              <div className="pl-[1mm] pr-[1mm] text-[8pt] flex justify-end">
                {/* for SPM ENGINEERING */}
                <p>for SPM ENGINEERING</p>
              </div>
            </div>
          </div>
        </div>

        {/* FOOTER (Outside Box) */}
        <div className="h-[10mm] flex items-center justify-center">
          <p className="text-[10px] tracking-wide">
            THIS IS COMPUTER GENERATED INVOICE
          </p>
        </div>
      </div>
    </div>
  );
}
