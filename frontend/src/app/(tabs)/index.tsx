import { StyleSheet, Text, View, Pressable } from "react-native";
import { router } from "expo-router";

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Work Hour Tracker</Text>

      <Text style={styles.subtitle}>Welcome back</Text>

      <View style={styles.cardsContainer}>
        <View style={styles.card}>
          <Text style={styles.cardValue}>8.5</Text>
          <Text style={styles.cardLabel}>Hours Today</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardValue}>$68.00</Text>
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

      <View style={styles.entry}>
        <View>
          <Text style={styles.entryDate}>July 04, 2026</Text>
          <Text style={styles.entryDetails}>10 hours × $8/hour</Text>
        </View>

        <Text style={styles.entryAmount}>$80.00</Text>
      </View>

      <View style={styles.entry}>
        <View>
          <Text style={styles.entryDate}>June 24, 2026</Text>
          <Text style={styles.entryDetails}>8.52 hours × $7/hour</Text>
        </View>

        <Text style={styles.entryAmount}>$59.64</Text>
      </View>
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
