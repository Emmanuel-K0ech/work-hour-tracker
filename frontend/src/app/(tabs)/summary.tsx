import { useState } from "react";
import { View, Text, StyleSheet, Pressable, Platform } from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";

import { getSummary } from "@/services/api";

function formatDate(date: Date) {
  return date.toISOString().split("T")[0];
}

export default function SummaryScreen() {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());

  const [showStartPicker, setShowStartPicker] = useState(false);
  const [showEndPicker, setShowEndPicker] = useState(false);

  const [totalHours, setTotalHours] = useState<number | null>(null);
  const [totalEarnings, setTotalEarnings] = useState<number | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerateSummary = async () => {
    const start = formatDate(startDate);
    const end = formatDate(endDate);

    if (start > end) {
      setError("Start date cannot be after end date.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await getSummary(start, end);

      setTotalHours(response.data.total_hours);
      setTotalEarnings(response.data.total_earnings);
    } catch (error) {
      console.error("Summary error:", error);
      setError("Failed to load summary.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Summary</Text>

      <Text style={styles.label}>Start Date</Text>

      {Platform.OS === "web" ? (
        <input
          type="date"
          value={formatDate(startDate)}
          onChange={(event) => {
            setStartDate(new Date(`${event.target.value}T00:00:00`));
          }}
          style={styles.webDateInput}
        />
      ) : (
        <>
          <Pressable
            style={styles.dateButton}
            onPress={() => setShowStartPicker(true)}
          >
            <Text style={styles.dateText}>{formatDate(startDate)}</Text>
          </Pressable>

          {showStartPicker && (
            <DateTimePicker
              value={startDate}
              mode="date"
              onChange={(event, selectedDate) => {
                setShowStartPicker(false);

                if (selectedDate) {
                  setStartDate(selectedDate);
                }
              }}
            />
          )}
        </>
      )}
      <Text style={styles.label}>End Date</Text>

      {Platform.OS === "web" ? (
        <input
          type="date"
          value={formatDate(endDate)}
          onChange={(event) => {
            setEndDate(new Date(`${event.target.value}T00:00:00`));
          }}
          style={styles.webDateInput}
        />
      ) : (
        <>
          <Pressable
            style={styles.dateButton}
            onPress={() => setShowEndPicker(true)}
          >
            <Text style={styles.dateText}>{formatDate(endDate)}</Text>
          </Pressable>

          {showEndPicker && (
            <DateTimePicker
              value={endDate}
              mode="date"
              onChange={(event, selectedDate) => {
                setShowEndPicker(false);

                if (selectedDate) {
                  setEndDate(selectedDate);
                }
              }}
            />
          )}
        </>
      )}

      <Pressable
        style={styles.summaryButton}
        onPress={handleGenerateSummary}
        disabled={loading}
      >
        <Text style={styles.summaryButtonText}>
          {loading ? "Loading..." : "Generate Summary"}
        </Text>
      </Pressable>

      {error !== "" && <Text style={styles.error}>{error}</Text>}

      {totalHours !== null && totalEarnings !== null && (
        <View style={styles.results}>
          <View style={styles.card}>
            <Text style={styles.cardValue}>{totalHours.toFixed(2)}</Text>
            <Text style={styles.cardLabel}>Total Hours</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.cardValue}>${totalEarnings.toFixed(2)}</Text>
            <Text style={styles.cardLabel}>Total Earnings</Text>
          </View>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
  },

  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 24,
  },

  label: {
    fontSize: 16,
    fontWeight: "600",
    marginTop: 16,
    marginBottom: 8,
  },

  dateButton: {
    padding: 16,
    borderRadius: 10,
    backgroundColor: "#f0f0f0",
  },

  dateText: {
    fontSize: 16,
  },

  summaryButton: {
    marginTop: 24,
    padding: 16,
    borderRadius: 10,
    backgroundColor: "#222",
    alignItems: "center",
  },

  summaryButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },

  error: {
    marginTop: 16,
    color: "red",
    fontSize: 14,
  },

  results: {
    marginTop: 32,
    flexDirection: "row",
    gap: 12,
  },

  card: {
    flex: 1,
    padding: 20,
    borderRadius: 12,
    backgroundColor: "#f0f0f0",
  },

  cardValue: {
    fontSize: 24,
    fontWeight: "700",
  },

  cardLabel: {
    marginTop: 6,
    fontSize: 14,
  },

  webDateInput: {
  padding: 12,
  borderRadius: 10,
  borderWidth: 1,
  borderColor: "#ddd",
  fontSize: 16,
  width: "100%",
},
});
