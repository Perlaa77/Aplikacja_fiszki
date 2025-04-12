// app/index.tsx
import React, { useEffect, useState } from 'react';
import { Image } from 'react-native';
import { useRouter, useFocusEffect } from 'expo-router';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Button1 } from '@/components/Button1';


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
      <Button1
        title="Edit"
        description="Go to edit"
        imageSource={require('@/assets/images/partial-react-logo.png')}
        onPress={() => router.push('/editFlashcards')}
      />
    </ParallaxScrollView>
  );
}
