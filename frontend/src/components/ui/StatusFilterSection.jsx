export default function StatusFilterSection({
  summaryLabel,
  summaryCount,
  options,
  activeValue,
  onChange,
}) {
  return (
    <div className="mb-6 relative">
      <div className="mb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <p className="text-sm md:text-base text-gray-700 font-medium">
          {summaryLabel}:{" "}
          <span className="font-bold text-gray-900">{summaryCount}</span>
        </p>
      </div>

      <div className="inline-flex items-center rounded-lg border border-gray-300 p-0.5 bg-gray-50 w-full sm:w-auto">
        {options.map((option, index) => (
          <div key={option.value} className="contents">
            {index > 0 ? (
              <div className="h-8 w-px bg-gray-300 mx-1 my-1"></div>
            ) : null}
            <button
              type="button"
              onClick={() => onChange(option.value)}
              className={`px-3 md:px-4 py-2 text-xs md:text-sm rounded-md font-medium transition w-1/2 sm:w-auto ${
                activeValue === option.value
                  ? "bg-purple-600 text-white"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              {option.label} ({option.count})
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
