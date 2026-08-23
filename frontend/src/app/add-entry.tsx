import { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Pressable,
  Platform,
} from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";
import { saveEntry } from "@/services/api";

export default function AddEntryScreen() {
  const [date, setDate] = useState(new Date());
  const [showDatePicker, setShowDatePicker] = useState(false);

  const [hoursWorked, setHoursWorked] = useState("");
  const [hourlyRate, setHourlyRate] = useState("");

  const handleSave = async () => {
    const hours = Number(hoursWorked);
    const rate = Number(hourlyRate);

    if (!hoursWorked || !hourlyRate) {
      alert("Please enter hours worked and hourly rate.");
      return;
    }

    if (hours <= 0) {
      alert("Hours worked must be greater than 0.");
      return;
    }

    if (rate <= 0) {
      alert("Hourly rate must be greater than 0.");
      return;
    }

    console.log({
      date: formatDateForInput(date),
      hours_worked: hours,
      hourly_rate: rate,
    });

    try {
      await saveEntry({
        date: formatDateForInput(date),
        hours_worked: hours,
        hourly_rate: rate,
      });

      alert("Entry saved successfully!");
    } catch (error) {
      console.error("Save entry error:", error);
      alert("Failed to save entry.");
    }
  };

  const formatDateForInput = (value: Date) => {
    return value.toISOString().split("T")[0];
  };

  const handleDateChange = (event: any, selectedDate?: Date) => {
    setShowDatePicker(false);

    if (selectedDate) {
      setDate(selectedDate);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Add Work Entry</Text>

      {/* Date */}
      <Text style={styles.label}>Date</Text>

      {Platform.OS === "web" ? (
        <input
          type="date"
          value={formatDateForInput(date)}
          onChange={(event) => {
            setDate(new Date(event.target.value));
          }}
          style={styles.webDateInput}
        />
      ) : (
        <>
          <Pressable
            style={styles.input}
            onPress={() => setShowDatePicker(true)}
          >
            <Text>{date.toLocaleDateString()}</Text>
          </Pressable>

          {showDatePicker && (
            <DateTimePicker
              value={date}
              mode="date"
              display="default"
              onChange={handleDateChange}
            />
          )}
        </>
      )}

      {/* Hours */}
      <Text style={styles.label}>Hours Worked</Text>

      <TextInput
        style={styles.input}
        value={hoursWorked}
        onChangeText={setHoursWorked}
        placeholder="e.g. 8.5"
        keyboardType="decimal-pad"
      />

      {/* Hourly Rate */}
      <Text style={styles.label}>Hourly Rate</Text>

      <TextInput
        style={styles.input}
        value={hourlyRate}
        onChangeText={setHourlyRate}
        placeholder="e.g. 10"
        keyboardType="decimal-pad"
      />

      {/* Save */}
      <Pressable style={styles.saveButton} onPress={handleSave}>
        <Text style={styles.saveButtonText}>Save Entry</Text>
      </Pressable>
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
    marginBottom: 32,
  },

  label: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 8,
    marginTop: 16,
  },

  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 14,
    fontSize: 16,
  },

  webDateInput: {
    width: "100%",
    padding: 14,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    fontSize: 16,
    boxSizing: "border-box",
  },

  saveButton: {
    marginTop: 32,
    padding: 16,
    borderRadius: 10,
    backgroundColor: "#222",
    alignItems: "center",
  },

  saveButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});
