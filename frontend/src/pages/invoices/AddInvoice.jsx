import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { Plus, Trash2, Loader } from "lucide-react";
import toast from "react-hot-toast";
import { getAllCustomers } from "@/services/customer_service";
import { getAllItems } from "@/services/items_service";
import {
  getPreviewInvoiceNumber,
  createInvoice,
} from "@/services/invoice_service";

export default function AddInvoice() {
  const navigate = useNavigate();
  const dataLoadedRef = useRef(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    invoiceNumber: "",
    invoiceDate: "",
    poNumber: "",
    buyerName: "",
    buyerGstin: "",
    consigneeName: "",
    consigneeGstin: "",
  });

  const [items, setItems] = useState([
    { id: 1, itemName: "", hsn: "", gst: 0, quantity: "", rate: "", uom: "" },
  ]);

  const [totals, setTotals] = useState({
    subtotal: 0,
    sgst: 0,
    cgst: 0,
    roundOff: 0,
    amountInWords: "",
  });

  const [customers, setCustomers] = useState([]);
  const [allItems, setAllItems] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load customers, items, and preview invoice number when component mounts
  useEffect(() => {
    // Prevent double API calls in StrictMode (React dev mode)
    if (dataLoadedRef.current) {
      return;
    }
    dataLoadedRef.current = true;

    const loadData = async () => {
      try {
        const [customersResponse, itemsResponse, invoiceResponse] =
          await Promise.all([
            getAllCustomers(),
            getAllItems(),
            getPreviewInvoiceNumber(),
          ]);

        // Extract customers array from response
        let customersArray = [];
        if (Array.isArray(customersResponse)) {
          customersArray = customersResponse;
        } else if (
          customersResponse?.customers &&
          Array.isArray(customersResponse.customers)
        ) {
          customersArray = customersResponse.customers;
        } else if (
          customersResponse?.data &&
          Array.isArray(customersResponse.data)
        ) {
          customersArray = customersResponse.data;
        }

        // Extract items array from response
        let itemsArray = [];
        if (Array.isArray(itemsResponse)) {
          itemsArray = itemsResponse;
        } else if (itemsResponse?.items && Array.isArray(itemsResponse.items)) {
          itemsArray = itemsResponse.items;
        } else if (itemsResponse?.data && Array.isArray(itemsResponse.data)) {
          itemsArray = itemsResponse.data;
        }

        setCustomers(customersArray);
        setAllItems(itemsArray);

        // Set the preview invoice number
        if (invoiceResponse?.invoice_number) {
          setFormData((prev) => ({
            ...prev,
            invoiceNumber: invoiceResponse.invoice_number,
          }));
        }

        // console.log("Loaded Customers:", customersArray);
        // console.log("Loaded Items:", itemsArray);
        // console.log("Preview Invoice Number:", invoiceResponse);
      } catch (error) {
        console.error("Error loading data:", error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const updated = { ...prev, [name]: value };

      // Auto-fill GSTIN for buyer when buyer name is selected
      if (name === "buyerName" && value) {
        const selectedCustomer = customers.find((c) => c.name === value);
        if (selectedCustomer) {
          updated.buyerGstin = selectedCustomer.gstin || "";
        }
      }

      // Auto-fill GSTIN for consignee when consignee name is selected
      if (name === "consigneeName" && value) {
        const selectedCustomer = customers.find((c) => c.name === value);
        if (selectedCustomer) {
          updated.consigneeGstin = selectedCustomer.gstin || "";
        }
      }

      return updated;
    });
  };

  const handleItemChange = (id, field, value) => {
    setItems((prevItems) =>
      prevItems.map((item) => {
        let updatedItem = { ...item };
        if (item.id === id) {
          updatedItem[field] = value;

          // If item name changed, fetch and fill item details
          if (field === "itemName" && value) {
            const selectedItem = allItems.find(
              (i) => i.name === value || i.id === value,
            );
            if (selectedItem) {
              // Map API field names to form field names
              updatedItem.hsn = selectedItem.hsn_sac || "";
              updatedItem.gst = selectedItem.gst_percentage || 0;
              updatedItem.uom = selectedItem.uom || "";
              updatedItem.rate = selectedItem.rate || "";
              console.log(
                "Selected Item:",
                selectedItem,
                "Updated Item:",
                updatedItem,
              );
            }
          }
        }
        return updatedItem;
      }),
    );
  };

  const addItem = () => {
    const newId = Math.max(...items.map((item) => item.id), 0) + 1;
    setItems([
      ...items,
      {
        id: newId,
        itemName: "",
        hsn: "",
        gst: 0,
        quantity: "",
        rate: "",
        uom: "",
      },
    ]);
  };

  const removeItem = (id) => {
    if (items.length > 1) {
      setItems(items.filter((item) => item.id !== id));
    }
  };

  const calculateTotal = () => {
    let subtotal = 0;
    items.forEach((item) => {
      const amount =
        (parseFloat(item.quantity) || 0) * (parseFloat(item.rate) || 0);
      subtotal += amount;
    });

    const gstRate = parseFloat(items[0]?.gst) || 0;
    const sgst = (subtotal * gstRate) / 2 / 100;
    const cgst = (subtotal * gstRate) / 2 / 100;

    return {
      subtotal,
      sgst,
      cgst,
      total: subtotal + sgst + cgst,
    };
  };

  // Convert integer number to words (simple English, supports up to crores/millions)
  const numberToWords = (num) => {
    if (num === 0) return "Zero Rupees Only";
    const a = [
      "",
      "One",
      "Two",
      "Three",
      "Four",
      "Five",
      "Six",
      "Seven",
      "Eight",
      "Nine",
      "Ten",
      "Eleven",
      "Twelve",
      "Thirteen",
      "Fourteen",
      "Fifteen",
      "Sixteen",
      "Seventeen",
      "Eighteen",
      "Nineteen",
    ];
    const b = [
      "",
      "",
      "Twenty",
      "Thirty",
      "Forty",
      "Fifty",
      "Sixty",
      "Seventy",
      "Eighty",
      "Ninety",
    ];

    const inWords = (n) => {
      if (n < 20) return a[n];
      if (n < 100)
        return b[Math.floor(n / 10)] + (n % 10 ? " " + a[n % 10] : "");
      if (n < 1000)
        return (
          a[Math.floor(n / 100)] +
          " Hundred" +
          (n % 100 ? " " + inWords(n % 100) : "")
        );
      if (n < 100000)
        return (
          inWords(Math.floor(n / 1000)) +
          " Thousand" +
          (n % 1000 ? " " + inWords(n % 1000) : "")
        );
      if (n < 10000000)
        return (
          inWords(Math.floor(n / 100000)) +
          " Lakh" +
          (n % 100000 ? " " + inWords(n % 100000) : "")
        );
      return (
        inWords(Math.floor(n / 10000000)) +
        " Crore" +
        (n % 10000000 ? " " + inWords(n % 10000000) : "")
      );
    };

    return `${inWords(num)} Rupees Only`;
  };

  const buildInvoicePayload = () => {
    // Calculate totals once
    let subtotal = 0;
    items.forEach((item) => {
      const amount =
        (parseFloat(item.quantity) || 0) * (parseFloat(item.rate) || 0);
      subtotal += amount;
    });

    const gstRate = parseFloat(items[0]?.gst) || 0;
    const sgst = (subtotal * gstRate) / 2 / 100;
    const cgst = (subtotal * gstRate) / 2 / 100;
    const rawTotal = subtotal + sgst + cgst;

    // Compute rounded integer total per requirement: if fractional part > 0.5 -> ceil, else -> floor
    const fraction = rawTotal - Math.floor(rawTotal);
    const roundedTotal =
      fraction > 0.5 ? Math.ceil(rawTotal) : Math.floor(rawTotal);
    const roundOffDifference = parseFloat((roundedTotal - rawTotal).toFixed(2));

    // Find full buyer and consignee details
    const buyerDetails = customers.find((c) => c.name === formData.buyerName);
    const consigneeDetails = customers.find(
      (c) => c.name === formData.consigneeName,
    );

    // Format items for API
    const formattedItems = items.map((item) => ({
      // convert item_id to string
      item_id: String(item.id),
      name: item.itemName,
      hsn: item.hsn,
      uom: item.uom,
      quantity: item.quantity,
      rate: item.rate,
      gst_percentage: item.gst,
      amount: parseFloat(item.quantity) * parseFloat(item.rate),
    }));

    return {
      invoice_number: formData.invoiceNumber,
      invoice_date: formData.invoiceDate,
      po_number: formData.poNumber || "",
      buyer: {
        id: buyerDetails?.id || "",
        name: buyerDetails?.name || formData.buyerName,
        gstin: buyerDetails?.gstin || formData.buyerGstin || "",
        address: buyerDetails?.address || "",
        email: buyerDetails?.email || "",
        panNumber: buyerDetails?.panNumber || "",
        phone: buyerDetails?.phone || "",
      },
      consignee: {
        id: consigneeDetails?.id || "",
        name: consigneeDetails?.name || formData.consigneeName,
        gstin: consigneeDetails?.gstin || formData.consigneeGstin || "",
        address: consigneeDetails?.address || "",
        email: consigneeDetails?.email || "",
        panNumber: consigneeDetails?.panNumber || "",
        phone: consigneeDetails?.phone || "",
      },
      items: formattedItems,
      totals: {
        subtotal: subtotal,
        sgst: sgst,
        cgst: cgst,
        // store the round off difference and the adjusted integer total
        round_off: roundOffDifference,
        rounded_total: roundedTotal,
        total: roundedTotal,
        amount_in_words: numberToWords(roundedTotal),
      },
    };
  };

  const handlePreview = () => {
    if (!formData.buyerName || !formData.consigneeName) {
      toast.error("Please select both buyer and consignee");
      return;
    }

    if (items.some((item) => !item.itemName || !item.quantity || !item.rate)) {
      toast.error("Please fill all item details");
      return;
    }

    const previewData = buildInvoicePayload();
    sessionStorage.setItem("invoice_preview_data", JSON.stringify(previewData));
    window.open("/SPM_bill.html?preview=1", "_blank", "noopener");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    if (!formData.buyerName || !formData.consigneeName) {
      toast.error("Please select both buyer and consignee");
      return;
    }

    if (items.some((item) => !item.itemName || !item.quantity || !item.rate)) {
      toast.error("Please fill all item details");
      return;
    }

    setIsSubmitting(true);

    try {
      const invoicePayload = buildInvoicePayload();
      // backend create schema does not include invoice_number
      delete invoicePayload.invoice_number;
      console.log("Invoice Payload:", invoicePayload);

      // Call API to create invoice
      const response = await createInvoice(invoicePayload);

      if (response?.success) {
        toast.success("Invoice created successfully! 🎉");
        // Redirect to invoices list after 1.5 seconds
        // setTimeout(() => {
        navigate("/invoices");
        // }, 1500);
      } else {
        toast.error(response?.message || "Failed to create invoice");
      }
    } catch (error) {
      console.error("Error creating invoice:", error);
      toast.error(
        error?.response?.data?.detail ||
          error.message ||
          "Failed to create invoice",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="w-full">
          <div className="bg-white rounded-2xl shadow-lg p-8 min-h-[320px] flex items-center justify-center">
            <div className="flex flex-col items-center gap-3 text-purple-700">
              <Loader size={30} className="animate-spin" />
              <p className="text-sm font-medium text-gray-600">
                Loading invoice data...
              </p>
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      {isSubmitting && (
        <div className="fixed inset-0 z-[9999] bg-black/20 backdrop-blur-sm flex items-center justify-center">
          <div className="bg-white/90 rounded-2xl shadow-xl px-6 py-5 flex items-center gap-3">
            <Loader size={24} className="animate-spin text-purple-700" />
            <p className="text-sm font-semibold text-gray-700">
              Creating invoice...
            </p>
          </div>
        </div>
      )}

      <div className="w-full">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-8">
            <h1 className="flex items-center justify-center text-3xl font-bold text-gray-800">
              Create New Invoice
            </h1>
            {/* Invoice Header Section */}
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-200">
                Invoice Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Invoice Number - Disabled */}
                <div>
                  <label
                    htmlFor="invoiceNumber"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Invoice Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="invoiceNumber"
                    name="invoiceNumber"
                    value={formData.invoiceNumber}
                    onChange={handleChange}
                    placeholder="e.g., INV-001"
                    disabled
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100 text-gray-600 cursor-not-allowed transition"
                  />
                </div>

                {/* Invoice Date */}
                <div>
                  <label
                    htmlFor="invoiceDate"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Invoice Date <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="date"
                    id="invoiceDate"
                    name="invoiceDate"
                    value={formData.invoiceDate}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>

                {/* PO Number */}
                <div>
                  <label
                    htmlFor="poNumber"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    PO Number
                  </label>
                  <input
                    type="text"
                    id="poNumber"
                    name="poNumber"
                    value={formData.poNumber}
                    onChange={handleChange}
                    placeholder="Enter PO Number"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>
              </div>
            </div>

            {/* Buyer Section */}
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-200">
                Buyer
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Buyer Name - Dropdown */}
                <div>
                  <label
                    htmlFor="buyerName"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Customer Name <span className="text-red-500">*</span>
                  </label>
                  <select
                    id="buyerName"
                    name="buyerName"
                    value={formData.buyerName}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  >
                    <option value="">Select Customer</option>
                    {customers.map((customer) => (
                      <option key={customer.id} value={customer.name}>
                        {customer.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Buyer GSTIN - Disabled */}
                <div>
                  <label
                    htmlFor="buyerGstin"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    GSTIN
                  </label>
                  <input
                    type="text"
                    id="buyerGstin"
                    name="buyerGstin"
                    value={formData.buyerGstin}
                    disabled
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100 text-gray-600 cursor-not-allowed transition"
                  />
                </div>
              </div>
            </div>

            {/* Consignee Section */}
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-200">
                Consignee
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Consignee Name - Dropdown */}
                <div>
                  <label
                    htmlFor="consigneeName"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Customer Name <span className="text-red-500">*</span>
                  </label>
                  <select
                    id="consigneeName"
                    name="consigneeName"
                    value={formData.consigneeName}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  >
                    <option value="">Select Customer</option>
                    {customers.map((customer) => (
                      <option key={customer.id} value={customer.name}>
                        {customer.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Consignee GSTIN - Disabled */}
                <div>
                  <label
                    htmlFor="consigneeGstin"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    GSTIN
                  </label>
                  <input
                    type="text"
                    id="consigneeGstin"
                    name="consigneeGstin"
                    value={formData.consigneeGstin}
                    disabled
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100 text-gray-600 cursor-not-allowed transition"
                  />
                </div>
              </div>
            </div>

            {/* Items Section */}
            <div>
              <div className="flex items-center justify-between mb-4 pb-2 border-b-2 border-purple-200">
                <h2 className="text-xl font-bold text-gray-800">
                  Invoice Items
                </h2>
                <button
                  type="button"
                  onClick={addItem}
                  className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
                >
                  <Plus size={18} />
                  Add Item
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                        Item Name
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                        HSN/SAC
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                        Quantity
                      </th>

                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                        Rate
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                        GST %
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                        UOM
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                        Amount
                      </th>
                      <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">
                        Action
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {items.map((item) => {
                      const amount =
                        (parseFloat(item.quantity) || 0) *
                        (parseFloat(item.rate) || 0);

                      return (
                        <tr
                          key={item.id}
                          className="border-b border-gray-200 hover:bg-gray-50"
                        >
                          <td className="px-4 py-3">
                            <select
                              value={item.itemName}
                              onChange={(e) =>
                                handleItemChange(
                                  item.id,
                                  "itemName",
                                  e.target.value,
                                )
                              }
                              required
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            >
                              <option value="">Select Item</option>
                              {allItems.map((itemOption) => (
                                <option
                                  key={itemOption.id}
                                  value={itemOption.name}
                                >
                                  {itemOption.name}
                                </option>
                              ))}
                            </select>
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="text"
                              value={item.hsn}
                              disabled
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-600 cursor-not-allowed"
                            />
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="number"
                              min="0"
                              step="1"
                              value={item.quantity}
                              onChange={(e) =>
                                handleItemChange(
                                  item.id,
                                  "quantity",
                                  e.target.value,
                                )
                              }
                              placeholder="Qty"
                              required
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            />
                          </td>

                          <td className="px-4 py-3">
                            <input
                              type="number"
                              min="0"
                              step="1"
                              value={item.rate}
                              onChange={(e) =>
                                handleItemChange(
                                  item.id,
                                  "rate",
                                  e.target.value,
                                )
                              }
                              placeholder="Rate"
                              required
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            />
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="number"
                              min="0"
                              step="1"
                              value={item.gst}
                              disabled
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-600 cursor-not-allowed"
                            />
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="text"
                              value={item.uom}
                              disabled
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-600 cursor-not-allowed"
                            />
                          </td>

                          <td className="px-4 py-3 text-right font-semibold text-gray-800">
                            ₹{amount.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-center">
                            <button
                              type="button"
                              onClick={() => removeItem(item.id)}
                              disabled={items.length === 1}
                              className="text-red-600 hover:text-red-800 disabled:text-gray-300 transition"
                            >
                              <Trash2 size={18} />
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Total Section */}
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border border-purple-200">
              <div className="flex justify-end">
                <div className="w-full md:w-1/3">
                  {(() => {
                    const totalsCalc = calculateTotal();
                    const rawTotal = totalsCalc.total;
                    const fraction = rawTotal - Math.floor(rawTotal);
                    const roundedTotal =
                      fraction > 0.5
                        ? Math.ceil(rawTotal)
                        : Math.floor(rawTotal);
                    const roundOffDifference = parseFloat(
                      (roundedTotal - rawTotal).toFixed(2),
                    );
                    const finalTotal = roundedTotal;
                    return (
                      <>
                        <div className="flex justify-between mb-3 text-gray-700">
                          <span className="font-semibold">Subtotal:</span>
                          <span>₹{totalsCalc.subtotal.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between mb-3 text-gray-700">
                          <span className="font-semibold">
                            SGST (50% of GST):
                          </span>
                          <span>₹{totalsCalc.sgst.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between mb-4 text-gray-700 pb-4 border-b border-gray-300">
                          <span className="font-semibold">
                            CGST (50% of GST):
                          </span>
                          <span>₹{totalsCalc.cgst.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between mb-4 text-gray-700 pb-4 border-b border-gray-300">
                          <span className="font-semibold">Round Off:</span>
                          <input
                            type="text"
                            value={`${roundOffDifference >= 0 ? "+" : ""}${roundOffDifference.toFixed(2)}`}
                            disabled
                            className="w-24 px-2 py-1 border border-gray-300 rounded-lg bg-gray-100 text-right text-gray-700 cursor-not-allowed"
                          />
                        </div>
                        <div className="flex justify-between text-lg font-bold text-purple-700">
                          <span>Total Amount:</span>
                          <span>₹{finalTotal.toFixed(2)}</span>
                        </div>
                        <div className="mt-3 text-gray-700">
                          <span className="font-semibold">
                            Amount in Words:
                          </span>
                          <div className="mt-1 text-sm">
                            {numberToWords(finalTotal)}
                          </div>
                        </div>
                      </>
                    );
                  })()}
                </div>
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex gap-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={handlePreview}
                disabled={isSubmitting}
                className="flex-1 bg-white border border-purple-600 text-purple-700 hover:bg-purple-50 disabled:bg-gray-100 disabled:text-gray-400 disabled:border-gray-300 font-semibold py-3 rounded-lg transition duration-200"
              >
                Preview Invoice
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="flex-1 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold py-3 rounded-lg transition duration-200 shadow-md hover:shadow-lg disabled:shadow-none disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isSubmitting ? (
                  <>
                    <Loader size={20} className="animate-spin" />
                    Creating Invoice...
                  </>
                ) : (
                  "Create Invoice"
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
}
