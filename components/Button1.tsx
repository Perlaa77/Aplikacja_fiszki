// components/Button1.tsx
import React from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { View, StyleSheet, TouchableOpacity, Text, Image, GestureResponderEvent, Dimensions } from 'react-native';
import Svg, { Defs, LinearGradient, Stop, Rect } from 'react-native-svg';

interface Button1Props {
    title: string;
    description?: string;
    imageSource: any;
    onPress: (event: GestureResponderEvent) => void;
  }
  
  const screenWidth = Dimensions.get('window').width;
  const BUTTON_WIDTH = screenWidth * 0.8;
  const BUTTON_HEIGHT = 80;
  
  export const Button1: React.FC<Button1Props> = ({
    title,
    description,
    imageSource,
    onPress,
  }) => {
    return (
      <View style={styles.outerContainer}>
        <TouchableOpacity onPress={onPress} activeOpacity={0.9}>
          {/* Gradient background */}
          <View style={styles.gradientWrapper}>
            <Svg width={BUTTON_WIDTH} height={BUTTON_HEIGHT} style={styles.svg}>
              <Defs>
                <LinearGradient
                  id="buttonGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="0%"
                >
                  <Stop offset="0%" stopColor="#F545A0" stopOpacity="1" />
                  <Stop offset="100%" stopColor="#FFB6C1" stopOpacity="1" />
                </LinearGradient>
              </Defs>
              <Rect
                x="0"
                y="0"
                width={BUTTON_WIDTH}
                height={BUTTON_HEIGHT}
                rx="16"
                fill="url(#buttonGradient)"
              />
            </Svg>
  
            {/* Content */}
            <View style={styles.buttonContent}>
              <Image source={imageSource} style={styles.buttonImage} />
              <View style={styles.textContainer}>
                <Text style={styles.buttonTitle}>{title}</Text>
                {description && (
                  <Text style={styles.buttonDescription}>{description}</Text>
                )}
              </View>
            </View>
          </View>
        </TouchableOpacity>
      </View>
    );
  };
  
  const styles = StyleSheet.create({
    outerContainer: {
      alignItems: 'center',
      marginBottom: 18,
    },
    gradientWrapper: {
      width: BUTTON_WIDTH,
      height: BUTTON_HEIGHT,
      borderRadius: 16,
      overflow: 'hidden',
      justifyContent: 'center',
    },
    svg: {
      position: 'absolute',
      top: 0,
      left: 0,
    },
    buttonContent: {
      flexDirection: 'row',
      alignItems: 'center',
      paddingHorizontal: 16,
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
      color: '#fff',
    },
    buttonDescription: {
      fontSize: 14,
      color: '#fff',
    },
  });