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
import { Svg, Text as SvgText, LinearGradient, Stop } from 'react-native-svg';
import { View } from 'react-native';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
    GaramondBold: require('../assets/fonts/EBGaramond-VariableFont_wght.ttf'),
  });

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
      <View style={{ height: 60, width: 400 }}>
        <Svg height="100%" width="100%">
          <LinearGradient 
            id="textGradient"
            x1="0%" 
            y1="0%"
            x2="100%"
            y2="0%"
            gradientUnits="userSpaceOnUse"
          >
            <Stop offset="0%" stopColor="#FFB6C1" stopOpacity="1" />
            <Stop offset="100%" stopColor="#FF1493" stopOpacity="1" />
          </LinearGradient>
          <SvgText
            x="50%"
            y="50%"
            fill="url(#textGradient)"
            fontSize="45"
            fontWeight="bold"
            fontFamily="GaramondBold"
            textAnchor="middle"
            alignmentBaseline="middle"
            letterSpacing="5"
          >
            FISTASZKI
          </SvgText>
        </Svg>
      </View>
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