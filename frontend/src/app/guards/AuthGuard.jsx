import { ReactNode } from "react";

export default function AuthGuard({ children, isAuthed }) {
  if (!isAuthed) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-600">Please log in to continue</p>
      </div>
    );
  }

  return children;
}
