// app/index.tsx
import React, { useEffect, useState } from 'react';
import { Image, TouchableOpacity, Text, StyleSheet, View } from 'react-native';
import { useRouter, useFocusEffect } from 'expo-router';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function HomeScreen() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    checkLoginStatus();
  }, []);

  useFocusEffect(
    React.useCallback(() => {
      checkLoginStatus();
    }, [])
  );

  const checkLoginStatus = async () => {
    try {
      const token = await AsyncStorage.getItem('userToken');
      setIsLoggedIn(!!token);
    } catch (error) {
      console.error('Error checking login status:', error);
    }
  };

  const handleProfilePress = () => {
    router.push(isLoggedIn ? '/profile' : '/login');
  };

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image source={require('@/assets/images/partial-react-logo.png')} />
      }
    >
      <View style={styles.buttonContainer}>
        {/* Edit Button */}
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.push('/editFlashcards')}
        >
          <Text style={styles.buttonText}>Edit Flashcards</Text>
        </TouchableOpacity>
      </View>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  buttonContainer: {
    alignItems: 'center',
    padding: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 10,
    width: '80%',
    alignItems: 'center',
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  }
});