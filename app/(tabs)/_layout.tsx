import { Tabs } from 'expo-router';
import React from 'react';
import { Platform } from 'react-native';
import { AntDesign, MaterialIcons, FontAwesome, Ionicons } from '@expo/vector-icons';
import { HapticTab } from '@/components/HapticTab';
import { IconSymbol } from '@/components/ui/IconSymbol';
import TabBarBackground from '@/components/ui/TabBarBackground';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';

export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        // Configure global tab bar styles and behavior
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        tabBarButton: HapticTab, // Custom tab button with haptic feedback
        headerShown: false, // Hide headers globally
        tabBarBackground: TabBarBackground, // Custom background component
        tabBarStyle: Platform.select({
          ios: {
            position: 'absolute', // iOS-specific styling
          },
          default: {}, // Default styling for other platforms
        }),
      }}>
      {/* Visible tabs that appear in the navigation bar */}
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          headerShown: false,
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="house.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="learn"
        options={{
          title: 'Learn',
          headerShown: false,
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="book.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => (
            <FontAwesome name="user" size={28} color={color} />
          ),
        }}
      />

      {/* Hidden screens - accessible via navigation but not shown in tab bar */}
      <Tabs.Screen
        name="editFlashcards"
        options={{
          tabBarItemStyle: { display: 'none' }, // Removes space in tab bar
          tabBarButton: () => null, // Prevents rendering the tab button
        }}
      />
      <Tabs.Screen
        name="login"
        options={{
          tabBarItemStyle: { display: 'none' }, // Removes space in tab bar
          tabBarButton: () => null, // Prevents rendering the tab button
        }}
      />
      <Tabs.Screen
        name="register"
        options={{
          tabBarItemStyle: { display: 'none' }, // Removes space in tab bar
          tabBarButton: () => null, // Prevents rendering the tab button
        }}
      />
    </Tabs>
  );
}