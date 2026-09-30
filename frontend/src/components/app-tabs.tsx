import { NativeTabs } from "expo-router/unstable-native-tabs";
import { useColorScheme } from "react-native";

import { Colors } from "@/constants/theme";

export default function AppTabs() {
  const scheme = useColorScheme();
  const colors = Colors[scheme === "unspecified" ? "light" : scheme];

  return (
    <NativeTabs
      backgroundColor={colors.background}
      indicatorColor={colors.backgroundElement}
      labelVisibilityMode="labeled"
      labelStyle={{
        default: {
          color: colors.text,
          fontWeight: "600",
        },
        selected: {
          color: colors.text,
          fontWeight: "700",
        },
      }}
    >
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Icon md="home" />
        <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="entries">
        <NativeTabs.Trigger.Icon md="list" />
        <NativeTabs.Trigger.Label>Entries</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="summary">
        <NativeTabs.Trigger.Icon md="bar_chart" />
        <NativeTabs.Trigger.Label>Summary</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="assistant">
        <NativeTabs.Trigger.Icon md="chat" />
        <NativeTabs.Trigger.Label>Assistant</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
