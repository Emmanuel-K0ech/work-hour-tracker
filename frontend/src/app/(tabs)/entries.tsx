import { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";

import { getEntries } from "@/services/api";

export default function EntriesScreen() {
  const [entries, setEntries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    try {
      const response = await getEntries();
      setEntries(response.data);
    } catch (error) {
      console.error("Get entries error:", error);
      setError("Failed to load entries.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <Text>Loading entries...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        <Text>{error}</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>My Entries</Text>

      {entries.map((entry) => (
        <View key={entry.id} style={styles.entry}>
          <View>
            <Text style={styles.date}>{entry.date}</Text>

            <Text style={styles.details}>
              {entry.hours_worked} hours × ${entry.hourly_rate}/hour
            </Text>
          </View>

          <Text style={styles.amount}>
            ${(entry.hours_worked * entry.hourly_rate).toFixed(2)}
          </Text>
        </View>
      ))}
    </ScrollView>
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

  entry: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#ddd",
  },

  date: {
    fontSize: 16,
    fontWeight: "600",
  },

  details: {
    marginTop: 4,
    fontSize: 14,
  },

  amount: {
    fontSize: 16,
    fontWeight: "600",
  },
});
