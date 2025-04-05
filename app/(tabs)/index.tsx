import React from 'react';
import { Image, StyleSheet, Platform, View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useEffect, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useFocusEffect } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  // Sprawdź stan logowania przy starcie komponentu
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const token = await AsyncStorage.getItem('userToken');
        setIsLoggedIn(!!token);
      } catch (error) {
        console.error('Error checking login status:', error);
      }
    };

    checkLoginStatus();
  }, []);

  useFocusEffect(
    React.useCallback(() => {
      const checkLoginStatus = async () => {
        try {
          const token = await AsyncStorage.getItem('userToken');
          setIsLoggedIn(!!token);
        } catch (error) {
          console.error('Error checking login status:', error);
        }
      };
      checkLoginStatus();
    }, [])
  );

  const handleProfilePress = async () => {
  const token = await AsyncStorage.getItem('userToken');
  if (token) {
    router.push('/profile');
  } else {
    router.push('/login');
  }
};

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
        />
      }
    >
      <ThemedText type="title" style={styles.title}>Fistaszki</ThemedText>
      <ThemedView style={styles.space} />

      {/* Learn Button */}
      <TouchableOpacity
        style={[styles.button, { backgroundColor: '#FACFFF' }]}
        onPress={() => router.push('/explore')}
      >
        <View style={styles.buttonContent}>
          <Image
            source={require('@/assets/images/partial-react-logo.png')}
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
            source={require('@/assets/images/partial-react-logo.png')}
            style={styles.buttonImage}
          />
          <View style={styles.textContainer}>
            <Text style={styles.buttonTitle}>Edit</Text>
            <Text style={styles.buttonDescription}>Go to edit</Text>
          </View>
        </View>
      </TouchableOpacity>

      {/* Profile Button */}
      <TouchableOpacity
        style={[styles.button, { backgroundColor: '#FFDBA1' }]}
        onPress={handleProfilePress}
      >
        <View style={styles.buttonContent}>
          <Image
            source={require('@/assets/images/partial-react-logo.png')}
            style={styles.buttonImage}
          />
          <View style={styles.textContainer}>
            <Text style={styles.buttonTitle}>Profile</Text>
            <Text style={styles.buttonDescription}>
              {isLoggedIn ? 'Profile settings' : 'Login to your account'}
            </Text>
          </View>
        </View>
      </TouchableOpacity>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  title: {
    textAlign: 'center',
    fontSize: 24,
    fontWeight: 'bold',
  },
  space: {
    marginTop: 20,
  },
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