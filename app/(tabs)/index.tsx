import React from 'react';
import { Image, StyleSheet, Platform, View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';

import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function HomeScreen() {
  const router = useRouter(); // Inicjalizacja routera

  return (
    <ThemedView style={styles.container}>
      <ThemedText type="title">Welcome!</ThemedText>
      
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">Step 1: Try it</ThemedText>
        <ThemedText>
          Edit <ThemedText type="defaultSemiBold">app/(tabs)/index.tsx</ThemedText> to see changes.
          Press{' '}
          <ThemedText type="defaultSemiBold">
            {Platform.select({
              ios: 'cmd + d',
              android: 'cmd + m',
              web: 'F12'
            })}
          </ThemedText>{' '}
          to open developer tools.
        </ThemedText>
      </ThemedView>

      {/* Przycisk Explore */}
      <TouchableOpacity
        style={styles.button}
        onPress={() => router.push('/explore')}
      >
        <View style={styles.buttonContent}>
          <Image
            source={require('@/assets/images/partial-react-logo.png')} // Zmieniamy na odpowiednią ikonę
            style={styles.buttonImage}
          />
          <View style={styles.textContainer}>
            <Text style={styles.buttonTitle}>Explore</Text>
            <Text style={styles.buttonDescription}>Go to explore</Text>
          </View>
        </View>
      </TouchableOpacity>

      {/* Przycisk Edit */}
      <TouchableOpacity
        style={styles.button}
        onPress={() => router.push('/editFlashcards')}
      >
        <View style={styles.buttonContent}>
          <Image
            source={require('@/assets/images/partial-react-logo.png')} // Zmieniamy na odpowiednią ikonę
            style={styles.buttonImage}
          />
          <View style={styles.textContainer}>
            <Text style={styles.buttonTitle}>Edit</Text>
            <Text style={styles.buttonDescription}>Go to edit</Text>
          </View>
        </View>
      </TouchableOpacity>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#A1CEDC', // Kolor tła przycisku
    borderRadius: 15, // Zaokrąglone rogi
    paddingHorizontal: 16, // Odstępy od brzegów
    paddingVertical: 12, // Wysokość przycisku
    marginBottom: 16, // Odstęp między przyciskami
    width: '100%', // Pełna szerokość
  },
  buttonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
  },
  buttonImage: {
    width: 50, // Szerokość obrazu
    height: 50, // Wysokość obrazu
    marginRight: 16, // Odstęp między obrazem a tekstem
  },
  textContainer: {
    flex: 1,
  },
  buttonTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff', // Kolor tekstu
  },
  buttonDescription: {
    fontSize: 14,
    color: '#ffffff', // Kolor tekstu
  },
});
