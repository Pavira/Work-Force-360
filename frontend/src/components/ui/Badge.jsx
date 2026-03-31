export default function Badge({ children, variant = "primary" }) {
  const variants = {
    primary: "bg-purple-100 text-purple-800",
    success: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    danger: "bg-red-100 text-red-800",
  };

  return (
    <span
      className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${variants[variant]}`}
    >
      {children}
    </span>
  );
}
