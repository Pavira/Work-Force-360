import { useState, useRef, useEffect } from "react";
import { loginWithPin } from "@/services/auth_service";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [pin, setPin] = useState(["", "", "", ""]);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const inputsRef = useRef([]);
  const navigate = useNavigate();

  useEffect(() => {
    inputsRef.current[0]?.focus();
  }, []);

  async function handleChange(value, index) {
    if (isSubmitting) return;
    if (!/^\d?$/.test(value)) return;

    const newPin = [...pin];
    newPin[index] = value;
    setPin(newPin);
    if (error) setError("");

    if (value && index < 3) {
      inputsRef.current[index + 1].focus();
    }

    if (value && index === 3) {
      const enteredPin = newPin.join("");
      setIsSubmitting(true);
      try {
        await loginWithPin(enteredPin);
        navigate("/dashboard");
      } catch (err) {
        setError("Invalid PIN");
        setPin(["", "", "", ""]);
        inputsRef.current[0].focus();
      } finally {
        setIsSubmitting(false);
      }
    }
  }

  function handleKeyDown(e, index) {
    if (isSubmitting) return;
    if (e.key === "Backspace") {
      e.preventDefault();
      const newPin = [...pin];
      if (newPin[index] !== "") {
        newPin[index] = "";
        setPin(newPin);
      } else if (index > 0) {
        inputsRef.current[index - 1].focus();
      }
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-200 via-purple-200 to-pink-200 px-3 sm:px-4 py-6">
      <div className="w-full max-w-md bg-white rounded-2xl sm:rounded-3xl shadow-2xl p-6 sm:p-8 md:p-12 text-center">
        <h1 className="text-xl sm:text-2xl md:text-3xl font-bold text-gray-900 mb-2 leading-tight">
          WorkForce360 AdminPanel
        </h1>
        <p className="text-sm sm:text-base text-gray-600 mb-5 sm:mb-6">
          Enter your secure 4-digit PIN
        </p>

        {/* change the text to lock icon */}
        <div className="text-5xl sm:text-6xl mb-5 sm:mb-6">🔒</div>

        <div className="flex justify-center gap-2 sm:gap-3 mb-6 sm:mb-8">
          {pin.map((digit, index) => (
            <input
              key={index}
              type="tel"
              inputMode="numeric"
              pattern="[0-9]*"
              autoComplete="one-time-code"
              maxLength="1"
              value={digit}
              disabled={isSubmitting}
              ref={(el) => (inputsRef.current[index] = el)}
              onChange={(e) => handleChange(e.target.value, index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
              className="
                w-12 h-12 sm:w-14 sm:h-14 md:w-20 md:h-20
                text-xl sm:text-2xl md:text-3xl font-semibold
                text-center border-2 border-gray-300 rounded-xl
                focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200
                transition transform focus:scale-105
                disabled:opacity-70 disabled:cursor-not-allowed
              "
            />
          ))}
        </div>

        {isSubmitting && (
          <div className="flex items-center justify-center gap-2 text-indigo-700 text-sm sm:text-base font-medium mb-2">
            <div className="w-4 h-4 border-2 border-indigo-300 border-t-indigo-700 rounded-full animate-spin" />
            Verifying PIN...
          </div>
        )}

        {error && (
          <div className="text-red-600 text-sm sm:text-base font-medium mt-2">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
