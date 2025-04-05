// editFlashcard.tsx
import React, { useState, useEffect } from 'react';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Flashcard } from '../../database/flashcardDB';
import { saveFlashcard, getFlashcard, deleteFlashcard, getAllFlashcards } from '../../database/flashcardDB';
import ParallaxScrollView from '@/components/ParallaxScrollView';


export default function EditFlashcardScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const id = params.id as string;
  const topicId = params.topicId as string;

  // Initialize state with function to handle prop changes
  const [flashcard, setFlashcard] = useState({
    id: parseInt(id || '0'),
    topicId: parseInt(topicId || '0'),
    front: '',
    frontHint: '',
    back: '',
    backInfo: ''
  });

  const [allFlashcards, setAllFlashcards] = useState<Flashcard[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Reset form when ID changes to 0 (new flashcard)
  useEffect(() => {
    if (parseInt(id) === 0) {
      setFlashcard({
        id: 0,
        topicId: parseInt(topicId || '0'),
        front: '',
        frontHint: '',
        back: '',
        backInfo: ''
      });
    }
  }, [id, topicId]);

  // Load data when component mounts or ID changes
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        // Load existing flashcard if editing
        if (id && id !== '0') {
          const loadedFlashcard = await getFlashcard(parseInt(id));
          if (loadedFlashcard) {
            setFlashcard({
              id: loadedFlashcard.id,
              topicId: loadedFlashcard.topicId,
              front: loadedFlashcard.front,
              frontHint: loadedFlashcard.frontHint || '',
              back: loadedFlashcard.back,
              backInfo: loadedFlashcard.backInfo || ''
            });
          }
        }

        // Always load all flashcards
        const flashcards = await getAllFlashcards();
        setAllFlashcards(flashcards);
      } catch (err) {
        setError('Failed to load data');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [id]);

  const handleChange = (field: keyof typeof flashcard, value: string) => {
    setFlashcard(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!flashcard.front.trim() || !flashcard.back.trim()) {
      setError('Front and back content are required');
      return;
    }

    setIsLoading(true);
    try {
      // Create new object to avoid state mutation
      const flashcardToSave = { ...flashcard };

      // Generate new ID only for new flashcards
      if (flashcardToSave.id === 0) {
        flashcardToSave.id = Date.now();
      }

      await saveFlashcard(flashcardToSave);
      
      // Refresh the list and clear form for new entries
      if (flashcard.id === 0) {
        setFlashcard(prev => ({
          ...prev,
          id: 0,
          front: '',
          frontHint: '',
          back: '',
          backInfo: ''
        }));
      }

      const updatedFlashcards = await getAllFlashcards();
      setAllFlashcards(updatedFlashcards);
    } catch (err) {
      setError('Failed to save flashcard');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (cardId: number) => {
    setIsLoading(true);
    try {
      await deleteFlashcard(cardId);
      const updatedFlashcards = await getAllFlashcards();
      setAllFlashcards(updatedFlashcards);
      if (cardId === flashcard.id) {
        router.back();
      }
    } catch (err) {
      setError('Failed to delete flashcard');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <ThemedView style={styles.container}><ThemedText>Loading...</ThemedText></ThemedView>;

  return (
    <ParallaxScrollView 
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }} headerImage={<></>}   >
      {error && <ThemedText style={styles.error}>{error}</ThemedText>}

      {/* Input Fields (existing code) */}
      <ThemedText style={styles.label}>Front (Question)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.front}
        onChangeText={(text) => handleChange('front', text)}
        placeholder="Enter question"
        multiline
      />
      
      <ThemedText style={styles.label}>Front Hint (Optional)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.frontHint || ''}
        onChangeText={(text) => handleChange('frontHint', text)}
        placeholder="Enter hint"
        multiline
      />
      
      <ThemedText style={styles.label}>Back (Answer)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.back}
        onChangeText={(text) => handleChange('back', text)}
        placeholder="Enter answer"
        multiline
      />
      
      <ThemedText style={styles.label}>Additional Info (Optional)</ThemedText>
      <TextInput
        style={styles.input}
        value={flashcard.backInfo || ''}
        onChangeText={(text) => handleChange('backInfo', text)}
        placeholder="Enter additional information"
        multiline
      />
      
      <View style={styles.buttonContainer}>
        <Button title="Save" onPress={handleSave} disabled={isLoading} />
      </View>

      {/* Flashcards List */}
      <ThemedText style={styles.sectionTitle}>All Flashcards</ThemedText>
      {allFlashcards.length === 0 ? (
        <ThemedText style={styles.noCardsText}>No flashcards found</ThemedText>
      ) : (
        allFlashcards.map((card) => (
          <View key={card.id} style={styles.cardContainer}>
            <View style={styles.cardContent}>
              <Text style={styles.cardText}>Front: {card.front}</Text>
              <Text style={styles.cardText}>Back: {card.back}</Text>
            </View>
            <TouchableOpacity
              style={styles.deleteButton}
              onPress={() => handleDelete(card.id)}
            >
              <Text style={styles.deleteButtonText}>Delete</Text>
            </TouchableOpacity>
          </View>
        ))
      )}
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 12,
    marginBottom: 4,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4,
    padding: 10,
    fontSize: 16,
    minHeight: 80,
    marginBottom: 12,
    color: '#f8f8f8',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginVertical: 24,
  },
  error: {
    color: 'red',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 24,
    marginBottom: 12,
  },
  cardContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#f8f8f8',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
  },
  cardContent: {
    flex: 1,
    marginRight: 12,
  },
  cardText: {
    fontSize: 14,
    color: '#333',
    marginBottom: 4,
  },
  deleteButton: {
    backgroundColor: '#ff4444',
    borderRadius: 4,
    paddingVertical: 6,
    paddingHorizontal: 12,
  },
  deleteButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  noCardsText: {
    color: '#666',
    textAlign: 'center',
    marginVertical: 16,
  },
});