import React from 'react';
import { Image, StyleSheet, Platform, View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function HomeScreen() {
  const router = useRouter(); // Initialize router

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
        />
      }
    >
      {/* Title */}
      <ThemedText type="title" style={styles.title}>Fistaszki</ThemedText>

      {/* Space between title and buttons */}
      <ThemedView style={styles.space} />

      {/* Learn Button */}
      <TouchableOpacity
        style={[styles.button, { backgroundColor: '#FACFFF' }]}
        onPress={() => router.push('/explore')}
      >
        <View style={styles.buttonContent}>
          <Image
            source={require('@/assets/images/partial-react-logo.png')} // Replace with the correct icon
            style={styles.buttonImage}
          />
          <View style={styles.textContainer}>
            <Text style={styles.buttonTitle}>Learn</Text>
            <Text style={styles.buttonDescription}>Go learn!</Text>
          </View>
        </View>
      </TouchableOpacity>

      {/* Edit Button */}
      <TouchableOpacity
        style={[styles.button, { backgroundColor: '#BACDFF' }]}
        onPress={() => router.push('/editFlashcards')}
      >
        <View style={styles.buttonContent}>
          <Image
            source={require('@/assets/images/partial-react-logo.png')} // Replace with the correct icon
            style={styles.buttonImage}
          />
          <View style={styles.textContainer}>
            <Text style={styles.buttonTitle}>Edit</Text>
            <Text style={styles.buttonDescription}>Go to edit</Text>
          </View>
        </View>
      </TouchableOpacity>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  // Basic container
  container: {
    padding: 16,
  },
  // Title text style, centered
  title: {
    textAlign: 'center',
    fontSize: 24,
    fontWeight: 'bold',
  },
  // Space between title and buttons
  space: {
    marginTop: 20,
  },
  // Button style
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
