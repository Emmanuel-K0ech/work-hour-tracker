const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000";

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

export async function getEntries() {
  const response = await fetch(`${API_URL}/entries`);

  if (!response.ok) {
    throw new Error("Failed to fetch entries");
  }

  return response.json();
}

export async function getSummary(
  startDate: string,
  endDate: string
) {
  const response = await fetch(
    `${API_URL}/summary?start_date=${startDate}&end_date=${endDate}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch summary");
  }

  return response.json();
}

export async function sendMessage(message: string) {
  const response = await fetch(`${API_URL}/agent`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
}
