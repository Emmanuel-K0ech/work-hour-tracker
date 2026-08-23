import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from "react-native";

import { sendMessage } from "@/services/api";

type Message = {
  id: string;
  text: string;
  sender: "user" | "assistant";
};

export default function AssistantScreen() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! How can I help you with your work hours?",
      sender: "assistant",
    },
  ]);

  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) {
      return;
    }

    const messageText = input.trim();

    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      sender: "user",
    };

    setMessages((currentMessages) => [...currentMessages, userMessage]);

    setInput("");

    try {
      const result = await sendMessage(messageText);

      const assistantMessage: Message = {
        id: `${Date.now()}-assistant`,
        text: result.response.message,
        sender: "assistant",
      };

      setMessages((currentMessages) => [...currentMessages, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: `${Date.now()}-error`,
        text: "Sorry, I couldn't connect to the assistant.",
        sender: "assistant",
      };

      setMessages((currentMessages) => [...currentMessages, errorMessage]);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <Text style={styles.title}>AI Assistant</Text>

      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        style={styles.messageList}
        contentContainerStyle={styles.messageContent}
        renderItem={({ item }) => (
          <View
            style={[
              styles.messageBubble,
              item.sender === "user"
                ? styles.userMessage
                : styles.assistantMessage,
            ]}
          >
            <Text
              style={
                item.sender === "user" ? styles.userText : styles.assistantText
              }
            >
              {item.text}
            </Text>
          </View>
        )}
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Ask something..."
          placeholderTextColor="#888"
          multiline
        />

        <Pressable style={styles.sendButton} onPress={handleSend}>
          <Text style={styles.sendButtonText}>Send</Text>
        </Pressable>
      </View>
    </KeyboardAvoidingView>
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
    marginBottom: 16,
  },

  messageList: {
    flex: 1,
  },

  messageContent: {
    paddingVertical: 12,
    gap: 12,
  },

  messageBubble: {
    maxWidth: "80%",
    padding: 14,
    borderRadius: 14,
  },

  userMessage: {
    alignSelf: "flex-end",
    backgroundColor: "#222",
  },

  assistantMessage: {
    alignSelf: "flex-start",
    backgroundColor: "#f0f0f0",
  },

  userText: {
    color: "#fff",
    fontSize: 16,
  },

  assistantText: {
    color: "#222",
    fontSize: 16,
  },

  inputContainer: {
    flexDirection: "row",
    alignItems: "flex-end",
    gap: 8,
    paddingTop: 12,
  },

  input: {
    flex: 1,
    minHeight: 48,
    maxHeight: 120,
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 12,
    fontSize: 16,
  },

  sendButton: {
    paddingHorizontal: 18,
    paddingVertical: 14,
    borderRadius: 12,
    backgroundColor: "#222",
  },

  sendButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});
