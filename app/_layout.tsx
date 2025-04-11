import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import 'react-native-reanimated';
import { useColorScheme } from '@/hooks/useColorScheme';
import { useAuth } from '@/hooks/useAuth';
import { Text, TextStyle } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Mask, Rect, Svg } from 'react-native-svg';
import { View } from 'react-native';


// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
    GaramondBold: require('../assets/fonts/EBGaramond-VariableFont_wght.ttf'),
  });

  // Add null check while fonts are loading
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded || isLoggedIn === null) {
    return null;
  }

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
      <Stack.Screen 
          name="(tabs)" 
          options={{ 
            headerTitle: () => (
              
              <Text style={{
                fontFamily: 'GaramondBold',
                fontSize: 45,
                fontWeight: 'bold',
                color: '#FFB6C1',
                letterSpacing: 5,
                textTransform: 'uppercase',
              }}>
                Fistaszki
              </Text>
            ),
            headerTitleAlign: 'center'
          }} 
        />
        <Stack.Screen 
          name="index" 
          options={{ headerShown: false }}
          redirect={!isLoggedIn && isLoggedIn !== null}
        />
        <Stack.Screen 
          name="profile" 
          options={{ headerShown: false }}
          redirect={!isLoggedIn && isLoggedIn !== null}
        />
        <Stack.Screen 
          name="login" 
          options={{ headerShown: false }}
          redirect={isLoggedIn}
        />
        {/* Public routes */}
        <Stack.Screen name="register" options={{ headerShown: false }} />
      </Stack>
      <StatusBar style="auto" />
    </ThemeProvider>
  );
}