import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { saveFlashcard, getFlashcard, deleteFlashcard } from '../../database/flashcardDB';
import { getAllFlashcards } from '../../database/flashcardDB';

interface Flashcard {
  id: number;
  topicId: number;
  front: string;
  frontHint?: string;
  back: string;
  backInfo?: string;
}

export default function EditFlashcardScreen() {
  const router = useRouter();
  const { id, topicId } = useLocalSearchParams<{ id: string; topicId: string }>();
  
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [flashcard, setFlashcard] = useState<Flashcard>({
    id: 0,
    topicId: topicId ? parseInt(topicId) : 0,
    front: '',
    frontHint: '',
    back: '',
    backInfo: ''
  });

  const getFlashcards = async () => {
    try {
      const loadedFlashcards = await getAllFlashcards();
      setFlashcards(loadedFlashcards);
      console.log(flashcards);
      return loadedFlashcards;
    } catch (e) {
      console.error('Error loading cards:', e);
      return [];
    }
  };

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Load existing flashcard if editing
  useEffect(() => {
    const loadFlashcard = async () => {
      if (id && id !== '0') {
        setIsLoading(true);
        try {
          const loadedFlashcard = await getFlashcard(parseInt(id));
          if (loadedFlashcard) {
            setFlashcard({
              ...loadedFlashcard,
              frontHint: loadedFlashcard.frontHint || '',
              backInfo: loadedFlashcard.backInfo || ''
            });
          }
        } catch (err) {
          setError('Failed to load flashcard');
          console.error(err);
        } finally {
          setIsLoading(false);
        }
      }
    };
    
    loadFlashcard();
  }, [id]);

  const handleChange = (field: keyof Flashcard, value: string) => {
    setFlashcard(prev => ({ 
      ...prev, 
      [field]: value 
    }));
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      // If it's a new flashcard, generate a new ID
      const flashcardToSave = {
        ...flashcard,
        id: flashcard.id === 0 ? Date.now() : flashcard.id
      };
      
      await saveFlashcard(flashcardToSave);
      router.back(); // Navigate back after saving
    } catch (err) {
      setError('Failed to save flashcard');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleDelete = async () => {
    if (flashcard.id === 0) {
      router.back(); // Just go back if it's a new unsaved flashcard
      return;
    }
    
    setIsLoading(true);
    try {
      await deleteFlashcard(flashcard.id);
      router.back();
    } catch (err) {
      setError('Failed to delete flashcard');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  if (isLoading) return <View style={styles.container}><Text>Loading...</Text></View>;
  
  return (
    <ScrollView style={styles.container}>
      {error && <Text style={styles.error}>{error}</Text>}
      
      <Text style={styles.label}>Front (Question)</Text>
      <TextInput
        style={styles.input}
        value={flashcard.front}
        onChangeText={(text) => handleChange('front', text)}
        placeholder="Enter question"
        multiline
      />
      
      <Text style={styles.label}>Front Hint (Optional)</Text>
      <TextInput
        style={styles.input}
        value={flashcard.frontHint || ''}
        onChangeText={(text) => handleChange('frontHint', text)}
        placeholder="Enter hint"
        multiline
      />
      
      <Text style={styles.label}>Back (Answer)</Text>
      <TextInput
        style={styles.input}
        value={flashcard.back}
        onChangeText={(text) => handleChange('back', text)}
        placeholder="Enter answer"
        multiline
      />
      
      <Text style={styles.label}>Additional Info (Optional)</Text>
      <TextInput
        style={styles.input}
        value={flashcard.backInfo || ''}
        onChangeText={(text) => handleChange('backInfo', text)}
        placeholder="Enter additional information"
        multiline
      />
      
      <View style={styles.buttonContainer}>
        <Button title="Save" onPress={handleSave} disabled={isLoading} />
        <Button title="Read Cards" onPress={getFlashcards} disabled={isLoading}/>
        {flashcard.id !== 0 && (
          <Button 
            title="Delete" 
            onPress={handleDelete} 
            disabled={isLoading}
            color="red"
          />
        )}
      </View>
    </ScrollView>
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
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 24,
    marginBottom: 40,
  },
  error: {
    color: 'red',
    marginBottom: 12,
  }
});