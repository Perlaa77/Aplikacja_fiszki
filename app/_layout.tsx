// app/_layout.tsx
import { Stack } from 'expo-router';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { View, StyleSheet } from 'react-native';
import Svg, { Text as SvgText, Defs, LinearGradient, Stop } from 'react-native-svg';

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <View style={styles.container}>
        <Stack>
          <Stack.Screen
            name="(tabs)"
            options={{
              headerTitle: () => (
                <View style={{ height: 60, width: 400 }}>
                  <Svg height="100%" width="100%">
                    <Defs>
                      <LinearGradient
                        id="textGradient"
                        x1="0%"
                        y1="0%"
                        x2="100%"
                        y2="0%"
                        gradientUnits="userSpaceOnUse"
                      >
                        <Stop offset="0%" stopColor="#F545A0" stopOpacity="1" />
                        <Stop offset="100%" stopColor="#FFB6C1" stopOpacity="1" />
                      </LinearGradient>
                    </Defs>
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
              headerTitleAlign: 'center',
            }}
          />
        </Stack>
      </View>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 16,
    paddingTop: 12,
    backgroundColor: '#F0F4FA',
  },
});
