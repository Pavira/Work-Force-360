import { useEffect } from "react";
import { HashRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/auth/Login";
import Dashboard from "../pages/dashboard/Dashboard";
import ListInvoices from "../pages/invoices/ListInvoices";
import AddInvoice from "../pages/invoices/AddInvoice";
import UpdateInvoice from "../pages/invoices/UpdateInvoice";
import ListCustomers from "../pages/customers/ListCustomers";
import ListCompanies from "../pages/companies/ListCompanies";
import ViewCompany from "../pages/companies/ViewCompany";
import AddCustomer from "../pages/customers/AddCustomer";
import UpdateCustomer from "../pages/customers/UpdateCustomer";
import ListItems from "../pages/items/ListItems";
import AddItem from "../pages/items/AddItem";
import UpdateItem from "../pages/items/UpdateItem";

function LogoutRedirect() {
  useEffect(() => {
    localStorage.removeItem("authToken");
    sessionStorage.clear();
  }, []);

  return <Navigate to="/" replace />;
}

export default function AppRouter() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/logout" element={<LogoutRedirect />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/invoices" element={<ListInvoices />} />
        <Route path="/invoices/add" element={<AddInvoice />} />
        <Route path="/invoices/:invoiceId" element={<UpdateInvoice />} />
        <Route path="/customers" element={<ListCustomers />} />
        <Route path="/customers/add" element={<AddCustomer />} />
        <Route path="/companies" element={<ListCompanies />} />
        <Route path="/companies/:companyId" element={<ViewCompany />} />
        <Route path="/customers/:customerId" element={<UpdateCustomer />} />
        <Route path="/items" element={<ListItems />} />
        <Route path="/items/add" element={<AddItem />} />
        <Route path="/items/:itemId" element={<UpdateItem />} />
      </Routes>
    </HashRouter>
  );
}
