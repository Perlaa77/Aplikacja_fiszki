import { useState } from 'react';
import { StyleSheet, Image, Platform, Button, TextInput } from 'react-native';
import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function EditFlashcardsScreen() {
  const [topic, setTopic] = useState('');
  const [description, setDescription] = useState('');

  const addFlashCard = async () => {
    try {
      const newCard = {
        id: Date.now().toString(),
        topic,
        description,
      };

      // Get existing cards
      const existingCards = await AsyncStorage.getItem('flashcards');
      const cardsArray = existingCards ? JSON.parse(existingCards) : [];

      // Add new card
      cardsArray.push(newCard);

      // Save back to storage
      await AsyncStorage.setItem('flashcards', JSON.stringify(cardsArray));

      // Clear inputs
      setTopic('');
      setDescription('');
    } catch (e) {
      console.error('Error saving card:', e);
    }
  };

  const getFlashcards = async () => {
    try {
      const cards = await AsyncStorage.getItem('flashcards');
      console.log(cards);
      return cards ? JSON.parse(cards) : [];
    } catch (e) {
      console.error('Error loading cards:', e);
      return [];
    }
  };

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }}
      headerImage={
        <IconSymbol
          size={310}
          color="#808080"
          name="chevron.left.forwardslash.chevron.right"
          style={styles.headerImage}
        />
      }>
      <ThemedView style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Topic"
          value={topic}
          onChangeText={setTopic}
        />
        <TextInput
          style={[styles.input, styles.descriptionInput]}
          placeholder="Description"
          value={description}
          onChangeText={setDescription}
          multiline
        />
        <Button title="Dodaj fiszkę" onPress={addFlashCard} />
        <Button title="Wyświetl fiszkę" onPress={getFlashcards} />
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  headerImage: {
    color: '#808080',
    bottom: -90,
    left: -35,
    position: 'absolute',
  },
  inputContainer: {
    padding: 20,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  descriptionInput: {
    height: 100,
    textAlignVertical: 'top',
  },
  titleContainer: {
    flexDirection: 'row',
    gap: 8,
  },
});