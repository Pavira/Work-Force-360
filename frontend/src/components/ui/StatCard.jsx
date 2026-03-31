export default function StatCard({ title, value, isLoading = false }) {
  return (
    <div className="bg-white rounded-2xl shadow p-4 md:p-6 hover:shadow-lg transition">
      <p className="text-gray-500 font-semibold text-xs md:text-sm">{title}</p>
      {isLoading ? (
        <div className="mt-4 flex items-center justify-center">
          <div className="h-7 w-7 rounded-full border-4 border-gray-200 border-t-purple-700 animate-spin" />
        </div>
      ) : (
        <h2 className="text-3xl md:text-5xl font-bold text-purple-700 mt-2">
          {value}
        </h2>
      )}
    </div>
  );
}
