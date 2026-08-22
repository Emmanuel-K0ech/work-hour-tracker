const API_URL = "http://localhost:8000";

export async function saveEntry(data: {
  date: string;
  hours_worked: number;
  hourly_rate: number;
}) {
  const response = await fetch(`${API_URL}/entries`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to save entry");
  }

  return response.json();
}