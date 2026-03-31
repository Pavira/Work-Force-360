export default function PageHeader({ title, subtitle, action }) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 md:mb-8">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-gray-800">{title}</h1>
        {subtitle ? (
          <p className="text-sm md:text-base text-gray-500 mt-1">{subtitle}</p>
        ) : null}
      </div>
      {action || null}
    </div>
  );
}
