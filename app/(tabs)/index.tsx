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

      {/* Learn */}
      <TouchableOpacity
        style={[styles.button, { backgroundColor: '#FACFFF' }]}
        onPress={() => router.push('/explore')}
      >
        <View style={styles.buttonContent}>
          <Image
            source={require('@/assets/images/partial-react-logo.png')} // Zmieniamy na odpowiednią ikonę
            style={styles.buttonImage}
          />
          <View style={styles.textContainer}>
            <Text style={styles.buttonTitle}>Learn</Text>
            <Text style={styles.buttonDescription}>Go learn!</Text>
          </View>
        </View>
      </TouchableOpacity>

      {/* Edit */}
      <TouchableOpacity
        style={[styles.button, { backgroundColor: '#BACDFF' }]}
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
  //Basic container
  container: {
    padding: 16,
  },
  //Navigation button
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 16,
    paddingHorizontal: 16,
    paddingVertical: 14,
    marginBottom: 18,
    width: '100%',
  },
    buttonContent: {
      flexDirection: 'row',
      alignItems: 'center',
      width: '100%',
    },
    buttonImage: {
      width: 50,
      height: 50,
      marginRight: 16,
    },
    textContainer: {
      flex: 1,
    },
    buttonTitle: {
      fontSize: 18,
      fontWeight: 'bold',
      color: '#000000',
    },
    buttonDescription: {
      fontSize: 14,
      color: '#111111',
    },
});
