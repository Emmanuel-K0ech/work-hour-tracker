import { useEffect, useState } from "react";
import { StyleSheet, Text, View, Pressable } from "react-native";
import { router } from "expo-router";

import { getEntries } from "@/services/api";

export default function HomeScreen() {
  const [entries, setEntries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    try {
      const response = await getEntries();
      setEntries(response.data);
    } catch (error) {
      console.error("Home entries error:", error);
    } finally {
      setLoading(false);
    }
  };

  const today = new Date().toISOString().split("T")[0];

  const todayEntries = entries.filter((entry) => entry.date === today);

  const hoursToday = todayEntries.reduce(
    (total, entry) => total + entry.hours_worked,
    0,
  );

  const earningsToday = todayEntries.reduce(
    (total, entry) => total + entry.hours_worked * entry.hourly_rate,
    0,
  );

  const recentEntries = [...entries]
    .sort((a, b) => b.date.localeCompare(a.date))
    .slice(0, 2);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Work Hour Tracker</Text>

      <Text style={styles.subtitle}>Welcome back</Text>

      <View style={styles.cardsContainer}>
        <View style={styles.card}>
          <Text style={styles.cardValue}>{loading ? "..." : hoursToday}</Text>
          <Text style={styles.cardLabel}>Hours Today</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardValue}>
            {loading ? "..." : `$${earningsToday.toFixed(2)}`}
          </Text>
          <Text style={styles.cardLabel}>Earnings Today</Text>
        </View>
      </View>

      <Pressable
        style={styles.addButton}
        onPress={() => router.push("/add-entry")}
      >
        <Text style={styles.addButtonText}>+ Add Work Entry</Text>
      </Pressable>

      <Text style={styles.sectionTitle}>Recent Entries</Text>

      {!loading && recentEntries.length === 0 && (
        <Text>No work entries yet.</Text>
      )}

      {recentEntries.map((entry) => (
        <View key={entry.id} style={styles.entry}>
          <View>
            <Text style={styles.entryDate}>{entry.date}</Text>

            <Text style={styles.entryDetails}>
              {entry.hours_worked} hours × ${entry.hourly_rate}/hour
            </Text>
          </View>

          <Text style={styles.entryAmount}>
            ${(entry.hours_worked * entry.hourly_rate).toFixed(2)}
          </Text>
        </View>
      ))}
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
  },

  subtitle: {
    fontSize: 16,
    marginTop: 8,
    marginBottom: 24,
  },

  cardsContainer: {
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

  addButton: {
    marginTop: 24,
    padding: 16,
    borderRadius: 10,
    backgroundColor: "#222",
    alignItems: "center",
  },

  addButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },

  sectionTitle: {
    marginTop: 32,
    marginBottom: 12,
    fontSize: 20,
    fontWeight: "700",
  },

  entry: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#ddd",
  },

  entryDate: {
    fontSize: 16,
    fontWeight: "600",
  },

  entryDetails: {
    marginTop: 4,
    fontSize: 14,
  },

  entryAmount: {
    fontSize: 16,
    fontWeight: "600",
  },
});
