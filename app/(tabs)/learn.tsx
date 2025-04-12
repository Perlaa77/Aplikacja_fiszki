import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Switch, ScrollView } from 'react-native';
import { router } from 'expo-router';

export default function LearnScreen() {
  // State variables for form controls
  const [mode, setMode] = useState<'classic' | 'test'>('classic');
  const [timerEnabled, setTimerEnabled] = useState(false);

  // Start learning session
  const startSession = () => {
    router.push('/session');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Learn Mode</Text>
      </View>

      {/* Mode Selection */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Choose Mode</Text>
        <View style={styles.radioGroup}>
          <TouchableOpacity 
            style={styles.radioOption} 
            onPress={() => setMode('classic')}
          >
            <View style={[styles.radioButton, mode === 'classic' && styles.radioButtonSelected]}>
              {mode === 'classic' && <View style={styles.radioButtonInner} />}
            </View>
            <View style={styles.radioTextContainer}>
              <Text style={styles.radioLabel}>Classic</Text>
              <Text style={styles.radioDescription}>See front of flashcard and tap to reveal the back</Text>
            </View>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.radioOption} 
            onPress={() => setMode('test')}
          >
            <View style={[styles.radioButton, mode === 'test' && styles.radioButtonSelected]}>
              {mode === 'test' && <View style={styles.radioButtonInner} />}
            </View>
            <View style={styles.radioTextContainer}>
              <Text style={styles.radioLabel}>Test</Text>
              <Text style={styles.radioDescription}>See front of flashcard and type your answer</Text>
            </View>
          </TouchableOpacity>
        </View>
      </View>

      {/* Timer Option */}
      <View style={styles.section}>
        <View style={styles.timerOption}>
          <View>
            <Text style={styles.sectionTitle}>Timer</Text>
            <Text style={styles.timerDescription}>Set time limit for your learning session</Text>
          </View>
          <Switch
            value={timerEnabled}
            onValueChange={setTimerEnabled}
            trackColor={{ false: '#767577', true: '#AFD3F7' }}
            thumbColor={timerEnabled ? '#007AFF' : '#f4f3f4'}
          />
        </View>
        
        {timerEnabled && (
          <View style={styles.timerSettings}>
            <Text style={styles.timerSettingsText}>
              Timer options would appear here
            </Text>
          </View>
        )}
      </View>

      {/* Topic Selection Placeholder */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Select Topics</Text>
        <Text style={styles.topicDescription}>Choose at least one topic for your learning session</Text>
        
        {/* Placeholder for topic selection */}
        <View style={styles.topicPlaceholder}>
          <Text style={styles.placeholderText}>
            Topic selection will be implemented later
          </Text>
        </View>
      </View>

      {/* Start Button */}
      <TouchableOpacity
        style={styles.startButton}
        onPress={startSession}
      >
        <Text style={styles.startButtonText}>Start Session</Text>
      </TouchableOpacity>

      <View style={styles.spacer}></View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 20,
    paddingHorizontal: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
  },
  section: {
    backgroundColor: '#fff',
    padding: 20,
    marginTop: 20,
    borderRadius: 10,
    marginHorizontal: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 15,
    color: '#333',
  },
  radioGroup: {
    marginTop: 10,
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  radioButton: {
    height: 24,
    width: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#007AFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  radioButtonSelected: {
    borderColor: '#007AFF',
  },
  radioButtonInner: {
    height: 12,
    width: 12,
    borderRadius: 6,
    backgroundColor: '#007AFF',
  },
  radioTextContainer: {
    marginLeft: 10,
    flex: 1,
  },
  radioLabel: {
    fontSize: 18,
    fontWeight: '500',
    color: '#333',
  },
  radioDescription: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  timerOption: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  timerDescription: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  timerSettings: {
    marginTop: 15,
    padding: 15,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
  },
  timerSettingsText: {
    color: '#666',
    textAlign: 'center',
  },
  topicDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 15,
  },
  topicPlaceholder: {
    padding: 20,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    alignItems: 'center',
  },
  placeholderText: {
    color: '#666',
    fontSize: 16,
  },
  startButton: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 10,
    alignItems: 'center',
    marginHorizontal: 15,
    marginTop: 30,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  startButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  },
  spacer: {
    height: 100, // Extra space at the bottom for better scrolling
  }
});